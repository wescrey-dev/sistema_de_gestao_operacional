const CACHE_NAME = "sgo-cache-v6";

// Só cacheia o CSS no install — robusto, sem risco de falhar por ícone ausente
const ASSETS_CORE = ["/static/style.css"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_CORE))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((nomes) =>
      Promise.all(
        nomes.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const { request } = event;

  // Nunca intercepta POST/PUT/DELETE — formulários sempre precisam de conexão
  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // Assets estáticos: cache-first (CSS, ícones, JS)
  if (url.pathname.startsWith("/static/")) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached;
        return fetch(request).then((resposta) => {
          const copia = resposta.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copia));
          return resposta;
        }).catch(() => cached);
      })
    );
    return;
  }

  // Páginas HTML: network-first, fallback para cache se offline
  event.respondWith(
    fetch(request)
      .then((resposta) => {
        const copia = resposta.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(request, copia));
        return resposta;
      })
      .catch(() => caches.match(request))
  );
});
