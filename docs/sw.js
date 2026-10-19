const VERSION="c2153df0a12cb8";
const PREFIX='atlas-circuitos:'+self.registration.scope+':';
const CACHE=PREFIX+VERSION;
const CORE=['./','index.html','style.css','molecules.css','edition2.css','app.js','chapters.json','figures.json','references.json','meta.json','labs.json','glossary.json','assets.json','manifest.webmanifest','assets/icon.svg'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET'||new URL(event.request.url).origin!==self.location.origin)return;
  event.respondWith(caches.open(CACHE).then(async cache=>{
    const cached=await cache.match(event.request);if(cached)return cached;
    try{const response=await fetch(event.request);if(response.ok&&!event.request.url.includes('/downloads/'))await cache.put(event.request,response.clone());return response;}catch(e){if(event.request.mode==='navigate')return (await cache.match('index.html'))||Response.error();return Response.error();}
  }));
});
let loading=false;
self.addEventListener('message',event=>{
  if(event.data.type!=='CACHE_ALL'||loading)return;
  loading=true;
  event.waitUntil((async()=>{
    const cache=await caches.open(CACHE),files=await (await fetch('assets.json')).json();let done=0,failed=0;
    const say=msg=>{if(event.source)event.source.postMessage(msg);};
    for(let start=0;start<files.length;start+=6){
      await Promise.all(files.slice(start,start+6).map(async file=>{
        try{const response=await fetch(file);if(!response.ok)throw Error(file);await cache.put(file,response);}catch(e){failed++;}done++;
      }));
      say({type:'CACHE_PROGRESS',done,total:files.length});
    }
    say({type:'CACHE_DONE',failed,total:files.length});
  })().catch(()=>{if(event.source)event.source.postMessage({type:'CACHE_DONE',failed:1});}).finally(()=>{loading=false;}));
});
