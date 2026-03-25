const CACHE_NAME = 'estoque-bar-v2'
const urlsToCache = [
    '/',
    '/home',
    '/static/style.css',
    '/static/script.js',
    '/static/contagem.js',
    '/static/historico.js',
    '/static/manifest.json'
]

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(urlsToCache)
        })
    )
})

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request).then(function(response) {
            if(response) {
                return response
            }
            return fetch(event.request)
        })
    )
})