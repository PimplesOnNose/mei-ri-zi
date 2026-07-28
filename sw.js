/* ============================================================
   Service Worker — 每日字 Offline Support
   ============================================================ */

const CACHE = 'mei-ri-zi-v1';
const STATIC_CACHE = 'mei-ri-zi-static-v1';

/* Assets to pre-cache on install — the app shell */
// Use relative paths so they work on both root and subpath deployments
const PRECACHE = [
  './',
  './index.html',
  './css/app.css',
  './js/app.js',
  './js/progress.js',
  './js/srs.js',
  './js/celebrations.js',
  './manifest.json',
  './icon-192.svg',
  './icon-512.svg',
];

/* CDN resources to cache */
const CDN_CACHE = 'mei-ri-zi-cdn-v1';
const CDN_RESOURCES = [
  'https://cdn.jsdelivr.net/npm/hanzi-writer@3.5/dist/hanzi-writer.min.js',
  'https://cdn.jsdelivr.net/npm/pako@2.1.0/dist/pako.min.js',
  'https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@300;400;500;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@400;500;600&display=swap',
];

/* ---- Install: pre-cache app shell ---- */
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      return cache.addAll(PRECACHE);
    })
  );
  // Activate immediately — don't wait for page reload
  self.skipWaiting();
});

/* ---- Activate: clean old caches ---- */
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys
          .filter((key) => key !== STATIC_CACHE && key !== CDN_CACHE)
          .map((key) => caches.delete(key))
      );
    })
  );
  // Take control of all clients immediately
  self.clients.claim();
});

/* ---- Fetch: serve from cache or network ---- */
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Handle CDN resources
  if (url.hostname === 'cdn.jsdelivr.net' || url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(
      caches.open(CDN_CACHE).then((cache) => {
        return cache.match(event.request).then((cached) => {
          const fetched = fetch(event.request).then((response) => {
            if (response && response.ok) {
              cache.put(event.request, response.clone());
            }
            return response;
          }).catch(() => cached);
          return cached || fetched;
        });
      })
    );
    return;
  }

  // Handle data requests (vocabulary JSON, audio) — cache on access
  if (url.pathname.includes('/data/') || url.pathname.includes('/audio/')) {
    event.respondWith(
      caches.open(CACHE).then((cache) => {
        return cache.match(event.request).then((cached) => {
          const fetched = fetch(event.request).then((response) => {
            if (response && response.ok) {
              cache.put(event.request, response.clone());
            }
            return response;
          }).catch(() => {
            // If offline and we have cached data, serve it
            if (cached) return cached;
            // For audio specifically — return a silent fallback
            if (url.pathname.endsWith('.mp3')) {
              return new Response('', { status: 200, headers: { 'Content-Type': 'audio/mpeg' } });
            }
            throw new Error('Offline and no cached data');
          });
          return cached || fetched;
        });
      })
    );
    return;
  }

  // App shell — cache-first for everything else
  event.respondWith(
    caches.match(event.request).then((cached) => {
      const fetched = fetch(event.request).then((response) => {
        if (response && response.ok && response.type === 'basic') {
          caches.open(STATIC_CACHE).then((cache) => cache.put(event.request, response.clone()));
        }
        return response;
      }).catch(() => cached);
      return cached || fetched;
    })
  );
});
