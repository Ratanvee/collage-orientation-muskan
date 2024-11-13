// Cache name
const CACHE_NAME = "chatbot-cache-v1";

// Files to cache
const urlsToCache = [
  "/",
  "/static/style.css",
  "/static/manifest.json"
];

// Install the service worker and cache the files
self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

// Serve cached content when offline
self.addEventListener("fetch", function (event) {
  event.respondWith(
    caches.match(event.request)
      .then(function (response) {
        return response || fetch(event.request);
      })
  );
});



