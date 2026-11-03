self.addEventListener("install",e=>{self.skipWaiting()});
self.addEventListener("activate",e=>e.waitUntil(clients.claim()));
function openShareDB(){return new Promise((resolve,reject)=>{const q=indexedDB.open("wm",2);q.onupgradeneeded=()=>{const d=q.result;if(!d.objectStoreNames.contains("f"))d.createObjectStore("f");if(!d.objectStoreNames.contains("inbox"))d.createObjectStore("inbox",{keyPath:"id",autoIncrement:true});if(!d.objectStoreNames.contains("conQueue"))d.createObjectStore("conQueue",{keyPath:"id",autoIncrement:true})};q.onsuccess=()=>resolve(q.result);q.onerror=()=>reject(q.error)})}
async function saveIncoming(files){const db=await openShareDB();for(const f of files){if(!f||typeof f.arrayBuffer!=="function")continue;await new Promise((resolve,reject)=>{const tx=db.transaction("inbox","readwrite");tx.objectStore("inbox").add({file:f,name:f.name||"shared.xlsx",receivedAt:Date.now()});tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error)})}}
self.addEventListener("fetch",e=>{
 const u=new URL(e.request.url);
 if(e.request.method==="POST"&&u.pathname.endsWith("/share-target")){
  e.respondWith((async()=>{
   try{const fd=await e.request.formData();let files=fd.getAll("file").filter(x=>x&&typeof x.arrayBuffer==="function");if(!files.length){for(const v of fd.values())if(v&&typeof v.arrayBuffer==="function")files.push(v)}await saveIncoming(files)}catch(err){return new Response("تعذر استلام الملف. افتح التطبيق وحاول المشاركة مرة أخرى.",{status:500,headers:{"Content-Type":"text/plain;charset=utf-8"}})}
   return Response.redirect(self.registration.scope+"index.html?shared=1",303);
  })());
 }
});
