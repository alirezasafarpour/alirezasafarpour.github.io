/* Offline cache for Nederlands Lab.
 *
 * App shell is cache-first (it changes only on deploy); the vocabulary JSON is
 * stale-while-revalidate so a study session still works on a train with no
 * signal, but picks up new words as soon as there is a connection.
 */

const VERSION = 'nl-lab-v2';
const SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './assets/css/app.css',
  './assets/js/main.js',
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;          // never cache Supabase or fonts

  const isData = url.pathname.includes('/data/');
  e.respondWith(
    caches.open(VERSION).then(async (cache) => {
      const cached = await cache.match(req);
      const network = fetch(req)
        .then((res) => { if (res && res.ok) cache.put(req, res.clone()); return res; })
        .catch(() => null);
      if (isData) return cached || (await network) || Response.error();
      return cached || (await network) || Response.error();
    })
  );
});
