from pathlib import Path
import shutil,json,hashlib,zipfile,platform,sys,importlib.metadata
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists():ROOT=BASE
DOCS=ROOT/'docs';TOOLS=ROOT/'tools';TOOLS.mkdir(exist_ok=True)
for size in [180,192,512]:
    im=Image.new('RGB',(size,size),'#164b43');draw=ImageDraw.Draw(im)
    points=[(.23,.65),(.5,.25),(.78,.63),(.43,.78)]
    for a,b in [(0,1),(1,2),(2,3),(3,0)]:
        draw.line([(int(points[j][0]*size),int(points[j][1]*size)) for j in [a,b]],fill='#a5c6a6',width=max(2,size//35))
    for x,y in points:
        r=size*.067;draw.ellipse((x*size-r,y*size-r,x*size+r,y*size+r),fill='#f0f2df')
    im.save(DOCS/'assets'/f'icon-{size}.png')
manifest=json.loads((DOCS/'manifest.webmanifest').read_text(encoding='utf8'))
manifest['icons']=[dict(src=f'assets/icon-{n}.png',sizes=f'{n}x{n}',type='image/png',purpose='any') for n in [192,512]]
(DOCS/'manifest.webmanifest').write_text(json.dumps(manifest,ensure_ascii=False),encoding='utf8')
for name in ['crear_figuras.py','construir_libro.py','crear_cuadernos.py','validar_material.py','empaquetar.py']:
    src=BASE/'work'/name
    if src.exists() and src.resolve()!=(TOOLS/name).resolve():shutil.copy2(src,TOOLS/name)
(TOOLS/'requirements-build.txt').write_text('numpy>=2.0,<3\nscipy>=1.14,<2\nmatplotlib>=3.9,<4\nreportlab>=4,<5\npypdf>=5,<7\nmarkdown>=3.7,<4\nbeautifulsoup4>=4.12,<5\npillow>=11,<13\nnbformat>=5,<6\n',encoding='utf8')
versions=['# Entorno validado el 18-10-2026; no sustituye requirements.txt.','Python=='+platform.python_version()]
for pkg in ['numpy','scipy','matplotlib','reportlab','pypdf','markdown','beautifulsoup4','pillow']:
    versions.append(pkg+'=='+importlib.metadata.version(pkg))
(ROOT/'python'/'entorno-validado.txt').write_text('\n'.join(versions)+'\n',encoding='utf8')
practicas=DOCS/'practicas';practicas.mkdir(exist_ok=True)
for p in (ROOT/'python'/'cuadernos').glob('*'):
    if p.is_file() and p.suffix in ['.py','.ipynb']:shutil.copy2(p,practicas/p.name)
for p in ['circuitos.py','requirements.txt']:
    shutil.copy2(ROOT/'python'/p,practicas/p)
zip_path=DOCS/'downloads'/'practicas-python.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    z.write(ROOT/'LEEME.md','LEEME.md')
    for p in (ROOT/'python').rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT).as_posix())
shutil.copy2(ROOT/'LEEME.md',ROOT/'README.md')
assets=[p.relative_to(DOCS).as_posix() for p in DOCS.rglob('*') if p.is_file() and p.name not in ['sw.js','assets.json'] and 'downloads' not in p.parts]
assets.sort();digest=hashlib.sha256()
for p in assets:digest.update(p.encode());digest.update((DOCS/p).read_bytes())
version=digest.hexdigest()[:14]
(DOCS/'assets.json').write_text(json.dumps(assets,ensure_ascii=False),encoding='utf8')
sw=r'''const VERSION="__VERSION__";
const PREFIX='atlas-circuitos:'+self.registration.scope+':';
const CACHE=PREFIX+VERSION;
const CORE=['./','index.html','style.css','molecules.css','app.js','chapters.json','figures.json','references.json','meta.json','assets.json','manifest.webmanifest','assets/icon.svg'];
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
'''.replace('__VERSION__',version)
(DOCS/'sw.js').write_text(sw,encoding='utf8')
out=BASE/'outputs';out.mkdir(exist_ok=True)
shutil.copy2(zip_path,out/'practicas-python.zip')
bundle=out/'atlas-circuitos-genicos-completo.zip'
with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
    for p in ROOT.rglob('*'):
        if p.is_file() and not any(x in p.relative_to(ROOT).parts for x in ['.git','__pycache__','.venv','outputs','work']):
            z.write(p,'atlas-circuitos-genicos/'+p.relative_to(ROOT).as_posix())
print('Cache:',version,'Recursos offline:',len(assets),'Paquete completo MB:',round(bundle.stat().st_size/1e6,2))
