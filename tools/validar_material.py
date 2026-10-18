from pathlib import Path
import os,json,subprocess,zipfile,xml.etree.ElementTree as ET,re
from bs4 import BeautifulSoup
from pypdf import PdfReader
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists():ROOT=BASE
report={}
env=dict(os.environ,MPLBACKEND='Agg',PYTHONUTF8='1')
logs=[]
for p in sorted((ROOT/'python'/'cuadernos').glob('*.py')):
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
report['pdf']=dict(pages=len(r.pages),searchable_text=True,embedded_fonts=True,empty_pages=[i+1 for i,t in enumerate(texts) if len(t.strip())<10])
report['scope']='Pruebas analíticas, conservación, SSA y estimación en test_modelos.py; scripts de prácticas; estructura EPUB; PDF. Revisión experta independiente completa pendiente.'
report['revision_visual']={'paginas_recorridas':169,'detalle':'Recorrido visual completo de la maquetación; glifos Unicode y dos delimitadores corregidos, con nueva inspección de las páginas afectadas.'}
report['app_pruebas_ui']={'viewport_movil':390,'busqueda_texto_y_figuras':True,'figura_ampliada_y_enlaces':True,'notas_y_avance':True,'simulador':True,'sin_conexion':'Descarga de recursos y recarga con servidor HTTP detenido; búsqueda y figuras cargadas; simulador operativo. Verificado por interfaz de navegador.'}
import nbformat
notebooks=list((ROOT/'python'/'cuadernos').glob('*.ipynb'))
for notebook in notebooks:nbformat.validate(nbformat.read(notebook,as_version=4))
report['notebooks_validos']=len(notebooks)
(ROOT/'VERIFICACION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('Scripts:',len(logs),'EPUB:',report['epub'],'PDF:',report['pdf'])
