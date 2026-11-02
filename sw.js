self.addEventListener("install",()=>self.skipWaiting());
self.addEventListener("activate",e=>e.waitUntil(clients.claim()));
self.addEventListener("fetch",e=>{
  const u=new URL(e.request.url);
  if(e.request.method==="POST"&&u.pathname.endsWith("/share-target")){
    e.respondWith((async()=>{
      try{
        const fd=await e.request.formData(),f=fd.get("file");
        if(f){const c=await caches.open("shared");
          await c.put(self.registration.scope+"shared-file",new Response(f,{headers:{"x-name":encodeURIComponent(f.name||"shared.xlsx")}}));}
      }catch(err){}
      return Response.redirect(self.registration.scope+"index.html?shared=1",303);
    })());
  }
});
