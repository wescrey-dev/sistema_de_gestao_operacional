const CACHE_NAME = "sgo-cache-v1";

// Assets estáticos que raramente mudam - cache-first
const ASSETS_ESTATICOS = [
  "/static/style.css",
  "/static/icons/icon-192x192.png",
  "/static/icons/icon-512x512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_ESTATICOS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((nomes) =>
      Promise.all(
        nomes
          .filter((nome) => nome !== CACHE_NAME)
          .map((nome) => caches.delete(nome))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const { request } = event;

  // Nunca interceptar métodos que alteram dados (POST/PUT/DELETE) - eles
  // precisam de uma conexão real com o servidor para fazer sentido.
  // Deixa o navegador tratar normalmente, sem passar pelo cache.
  if (request.method !== "GET") {
    return;
  }

  const url = new URL(request.url);

  // Assets estáticos: cache-first (raramente mudam, prioriza velocidade)
  if (url.pathname.startsWith("/static/")) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached;
        return fetch(request).then((resposta) => {
          const copia = resposta.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copia));
          return resposta;
        });
      })
    );
    return;
  }

  // Páginas HTML: network-first, cai para o cache se estiver offline.
  // Assim o usuário sempre vê a versão mais nova quando há conexão,
  // mas ainda consegue abrir a última versão vista quando está offline.
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
