self.addEventListener("install", () => self.skipWaiting());

self.addEventListener("activate", event => {
  event.waitUntil(clients.claim());
});

self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);

  // Keep the existing Excel/CSV share-target handling unchanged.
  if (event.request.method === "POST" && url.pathname.endsWith("/share-target")) {
    event.respondWith((async () => {
      try {
        const formData = await event.request.formData();
        const file = formData.get("file");

        if (file) {
          const cache = await caches.open("shared");
          await cache.put(
            self.registration.scope + "shared-file",
            new Response(file, {
              headers: {
                "x-name": encodeURIComponent(file.name || "shared.xlsx")
              }
            })
          );
        }
      } catch (error) {}

      return Response.redirect(self.registration.scope + "index.html?shared=1", 303);
    })());
    return;
  }

  // Explicitly pass through normal page navigations within this app.
  if (
    event.request.method === "GET" &&
    event.request.mode === "navigate" &&
    url.origin === self.location.origin
  ) {
    event.respondWith(fetch(event.request));
  }
})
