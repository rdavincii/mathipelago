/* sw.js: makes the game work offline. Same-origin GET requests only: the optional online-friends calls go straight to the network.
 * Bump CACHE whenever you ship (it must contain MP.config.version; the unit tests check this). */
var CACHE = 'mathipelago-0.11.0';
var SHELL = [
  './',
  'index.html',
  'manifest.webmanifest',
  'css/style.css',
  'js/config.js',
  'js/core.js',
  'js/i18n.js',
  'js/locales/en.js',
  'js/locales/ms.js',
  'js/storage.js',
  'js/audio.js',
  'js/streak.js',
  'js/changelog.js',
  'js/friends.js',
  'js/art.js',
  'js/validators.js',
  'js/adaptive.js',
  'js/packs.js',
  'js/entitlements.js',
  'js/levels/registry.js',
  'js/levels/meadow.js',
  'js/levels/forest.js',
  'js/levels/cove.js',
  'js/ui.js',
  'js/puzzles.js',
  'js/app.js',
  'js/main.js',
  'icons/icon-192.png',
  'icons/icon-512.png',
  'icons/icon-maskable-512.png',
  'icons/apple-touch-icon.png'
];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(SHELL); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (ks) { return Promise.all(ks.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); })); }).then(function () { return self.clients.claim(); }));
});
// Cache first, refresh in the background: instant and offline-safe; a new version shows on the next open.
self.addEventListener('fetch', function (e) {
  var req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== self.location.origin) return;
  e.respondWith(caches.open(CACHE).then(function (c) {
    return c.match(req, { ignoreSearch: true }).then(function (hit) {
      var net = fetch(req).then(function (res) { if (res && res.ok) c.put(req, res.clone()); return res; });
      if (hit) { net.catch(function () {}); return hit; }
      return net.catch(function () { return req.mode === 'navigate' ? c.match('index.html') : Response.error(); });
    });
  }));
});
