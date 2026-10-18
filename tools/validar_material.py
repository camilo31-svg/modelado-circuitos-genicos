from pathlib import Path
import os,json,subprocess,zipfile,xml.etree.ElementTree as ET,re,sys,hashlib
from bs4 import BeautifulSoup
from pypdf import PdfReader
from pypdf.generic import ContentStream
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists():ROOT=BASE
skip_scripts='--artifacts-only' in sys.argv
previous=ROOT/'VERIFICACION.json'
report=json.loads(previous.read_text(encoding='utf8')) if skip_scripts and previous.exists() else {}
env=dict(os.environ,MPLBACKEND='Agg',PYTHONUTF8='1')
logs=report.get('scripts',[]) if skip_scripts else []
for p in ([] if skip_scripts else sorted((ROOT/'python'/'cuadernos').glob('*.py'))):
    r=subprocess.run(['python',str(p.resolve())],cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
    logs.append(dict(file=p.name,exit_code=r.returncode,output=r.stdout.strip(),errors=r.stderr.strip()))
    assert r.returncode==0,(p,r.stderr)
report['scripts']=logs
epub=ROOT/'docs'/'downloads'/'modelado-circuitos-genicos.epub'
with zipfile.ZipFile(epub) as z:
    assert z.infolist()[0].filename=='mimetype'
    assert z.infolist()[0].compress_type==zipfile.ZIP_STORED
    names=set(z.namelist());xmlcount=0;internal=0
    for name in names:
        if name.endswith(('.xhtml','.xml','.opf','.ncx')):
            ET.fromstring(z.read(name));xmlcount+=1
        if name.endswith('.xhtml'):
            soup=BeautifulSoup(z.read(name),'html.parser')
            for tag,attr in [('img','src'),('link','href'),('a','href')]:
                for el in soup.find_all(tag):
                    ref=el.get(attr,'').split('#')[0]
                    if ref and not re.match(r'^https?://',ref):
                        assert 'OEBPS/'+ref in names,(name,ref)
                        internal+=1
    opf=ET.fromstring(z.read('OEBPS/content.opf'));ns={'o':'http://www.idpf.org/2007/opf'}
    items=opf.findall('o:manifest/o:item',ns);ids={x.attrib['id'] for x in items}
    assert len(ids)==len(items)
    for item in items:assert 'OEBPS/'+item.attrib['href'] in names
    for ref in opf.findall('o:spine/o:itemref',ns):assert ref.attrib['idref'] in ids
    report['epub']=dict(xml_files_valid=xmlcount,internal_links_valid=internal,manifest_items=len(items),note='Validación estructural XML y vínculos; no es una certificación EPUBCheck externa.')
pdf=ROOT/'docs'/'downloads'/'modelado-circuitos-genicos.pdf';r=PdfReader(pdf)
texts=[p.extract_text() for p in r.pages]
assert len(texts)==json.loads((ROOT/'docs'/'meta.json').read_text(encoding='utf8'))['pages']
assert all('\ufffd' not in t for t in texts)
used_fonts={}
for page in r.pages:
    names=set();current=None;stack=[]
    for args,op in ContentStream(page.get_contents(),r).operations:
        if op==b'q':stack.append(current)
        elif op==b'Q':current=stack.pop() if stack else None
        elif op==b'Tf':current=str(args[0])
        elif op in [b'Tj',b'TJ',b"'",b'"'] and current:
            if any(isinstance(v,(str,bytes)) and len(v)>0 for v in (args[0] if op==b'TJ' else args)):names.add(current)
    for name in names:
        font=page['/Resources']['/Font'][name].get_object()
        if font.get('/Subtype')=='/Type0':font=font['/DescendantFonts'][0].get_object()
        descriptor=font.get('/FontDescriptor');descriptor=descriptor.get_object() if descriptor else {}
        used_fonts[str(font.get('/BaseFont',name))]=any(k in descriptor for k in ['/FontFile','/FontFile2','/FontFile3'])
assert used_fonts and all(used_fonts.values()),used_fonts
report['pdf']=dict(pages=len(r.pages),searchable_text=all(t.strip() for t in texts),embedded_fonts=all(used_fonts.values()),fuentes_utilizadas_incrustadas=used_fonts,empty_pages=[i+1 for i,t in enumerate(texts) if len(t.strip())<10])
report['scope']='Pruebas analíticas, conservación, SSA, estabilidad, sensibilidad y estimación; scripts de prácticas; estructura EPUB y PDF. Revisión experta independiente completa pendiente.'
report['revision_visual']={'estado':'pendiente de registrar tras la inspección de PNG','paginas':len(r.pages)}
figures=json.loads((ROOT/'docs'/'figures.json').read_text(encoding='utf8'))
plates=[f for f in figures if f.get('kind')=='mechanism']
assert len(plates)==12
for plate in plates:
    path=ROOT/'docs'/plate['png'];assert path.exists()
    assert hashlib.sha256(path.read_bytes()).hexdigest()==plate['sha256']
    assert plate.get('panels') and plate.get('limitation')
report['laminas']=dict(count=len(plates),style='Ilustración científica plana con sombreado limitado',files_and_hashes_valid=True,caption_and_panel_guide=True)
report['app_pruebas_ui']={'edicion':'2.0','estado':'pendiente de registrar tras probar la interfaz'}
import nbformat
notebooks=list((ROOT/'python'/'cuadernos').glob('*.ipynb'))
for notebook in notebooks:nbformat.validate(nbformat.read(notebook,as_version=4))
report['notebooks_validos']=len(notebooks)
tests=subprocess.run(['python','-X','utf8','-m','unittest','discover','-s',str((ROOT/'python').resolve()),'-p','test*.py'],env=env,capture_output=True,text=True,timeout=90)
assert tests.returncode==0,tests.stderr
report['pruebas_modelos']={'exit_code':tests.returncode,'output':tests.stdout+tests.stderr}
cs=json.loads((ROOT/'book'/'chapters.json').read_text(encoding='utf8'))
refs={ref['id']:ref for ref in json.loads((ROOT/'book'/'references.json').read_text(encoding='utf8'))}
assert cs[0]['id']=='edo'
assert len(cs)==34 and len(figures)==49 and len(notebooks)==22
assert len({c['id'] for c in cs})==len(cs)
assert [c['number'] for c in cs]==[f'{i:02}' for i in range(len(cs))]
sections=[]
for c in cs:
    cited=set(re.findall(r'\[([A-Z]\d{2})\]',c['body']))
    assert cited<=refs.keys(),(c['id'],cited-refs.keys())
    for section in re.split(r'(?m)(?=^## )',c['body']):
        if not section.strip():continue
        lines=section.splitlines()
        content='\n'.join(lines[1:]).strip()
        if not content:continue
        ids=list(dict.fromkeys(re.findall(r'\[([A-Z]\d{2})\]',section)))
        assert ids,(c['id'],lines[0])
        sections.append({'chapter':c['id'],'number':c['number'],'section':lines[0].lstrip('# '),'references':ids})
for f in figures:
    assert all(any(c['id']==id for c in cs) for id in f['chapters'])
    assert f.get('refs') and set(f['refs'])<=refs.keys(),f['id']
    assert (ROOT/'docs'/f['png']).exists()
(ROOT/'book'/'source-map.json').write_text(json.dumps(sections,ensure_ascii=False,indent=2),encoding='utf8')
report['cobertura_bibliografica']={'secciones_con_fuentes':len(sections),'referencias':len(refs),'ids_validos':True,'nota':'Cobertura formal de secciones y figuras; no sustituye revisión independiente de cada interpretación.'}
(ROOT/'VERIFICACION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('Scripts:',len(logs),'EPUB:',report['epub'],'PDF:',report['pdf'])
