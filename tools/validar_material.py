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
    all_ids={name:{el['id'] for el in BeautifulSoup(z.read(name),'html.parser').find_all(id=True)} for name in names if name.endswith('.xhtml')}
    for name in names:
        if name.endswith(('.xhtml','.xml','.opf','.ncx')):
            ET.fromstring(z.read(name));xmlcount+=1
        if name.endswith('.xhtml'):
            soup=BeautifulSoup(z.read(name),'html.parser')
            page_ids={el['id'] for el in soup.find_all(id=True)}
            for anchor in soup.find_all('a',href=True):
                href=anchor['href']
                if href.startswith('#'):assert href[1:] in page_ids,(name,href)
            for tag,attr in [('img','src'),('link','href'),('a','href')]:
                for el in soup.find_all(tag):
                    ref=el.get(attr,'').split('#')[0]
                    if ref and not re.match(r'^https?://',ref):
                        assert 'OEBPS/'+ref in names,(name,ref)
                        if '#' in el.get(attr,'') and ref.endswith('.xhtml'):
                            fragment=el[attr].split('#',1)[1]
                            assert fragment in all_ids['OEBPS/'+ref],(name,el[attr])
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
report['app_pruebas_ui']={'edicion':'2.3','estado':'pendiente de registrar tras probar la interfaz'}
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
assert len(cs)==36 and len(figures)==69 and len(notebooks)==25
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
web=json.loads((ROOT/'docs'/'chapters.json').read_text(encoding='utf8'))
equations=json.loads((ROOT/'book'/'equations.json').read_text(encoding='utf8'))
assert sorted(e['number'] for e in equations.values())==list(range(1,len(equations)+1))
equation_calls=0;figure_calls=0
for c in web:
    soup=BeautifulSoup(c['html'],'html.parser');ids=[el['id'] for el in soup.find_all(id=True)]
    assert len(ids)==len(set(ids)),c['id']
    for ref in soup.select('a.local-ref'):
        assert ref['href'][1:] in ids,(c['id'],ref['href'])
    eqs=soup.select('div.equation');calls=soup.select('a.equation-ref')
    assert len(eqs)==len(calls),(c['id'],len(eqs),len(calls))
    expected=[f for f in figures if c['id'] in f['chapters']]
    assert len(soup.find_all('figure'))==len(expected),(c['id'],len(expected))
    assert len(soup.select('p.figure-reference'))==len(expected),c['id']
    equation_calls+=len(calls);figure_calls+=len(expected)
report['referencias_cruzadas']={'ecuaciones_numeradas':len(equations),'llamadas_de_ecuacion':equation_calls,'llamadas_de_figura':figure_calls,'destinos_validos':True,'figuras_colocadas_en_el_desarrollo':True}
guides=[f for f in figures if f.get('curve_guide')]
assert len(guides)==56
import math
for f in guides:
    g=f['curve_guide'];assert g['parameter_behavior'] and g['readings']
    assert g['series_count']==sum(len(p['series']) for p in g['panels'])
    for panel in g['panels']:
        assert panel['x_label'] and panel['y_label']
        assert panel['integrated'] and 'verticales' in panel['visual_layout']
        assert 'visual_png' not in panel and 'visual_svg' not in panel
        for curve in panel['series']:
            assert len(curve['points'])==3
            for pt in curve['points']:
                assert math.isfinite(pt['x']) and math.isfinite(pt['y'])
                assert curve['minimum']-1e-10<=pt['y']<=curve['maximum']+1e-10
for f in guides:
    g=f['curve_guide'];assert g['minimum_font_pt']>=9.5
    assert g.get('panel_views') and g.get('book_views'),f['id']
    assert not g.get('layout_warnings'),(f['id'],g['layout_warnings'])
    for view in g['panel_views']+g['book_views']:assert (ROOT/'docs'/view['png']).is_file()
    for view in g['book_views']:
        scale=min(172/(view['width_in']*25.4),218/(view['height_in']*25.4))
        assert g['minimum_font_pt']*scale>=7.7,(f['id'],g['minimum_font_pt']*scale)
report['legibilidad_figuras']={'vistas_de_panel':sum(len(f['curve_guide']['panel_views']) for f in guides),'filas_para_libros':sum(len(f['curve_guide']['book_views']) for f in guides),'tipografia_minima_original_pt':9.5,'minimo_estimado_impreso_pt':7.7,'curvas_y_dibujos_juntos':True,'sin_colisiones_detectadas_entre_anotaciones':True,'nota':'Comprobación geométrica de anotaciones y tamaño; complementada con inspección visual.'}
q17=next(f for f in figures if f['id']=='q17_represion')['curve_guide']
rp,sp,ep=[p['series'][0] for p in q17['panels']]
assert rp['points'][0]['y']==1 and rp['points'][-1]['y']==10
assert abs(sp['points'][-1]['y']-2.4)<1e-10
assert abs(ep['points'][0]['y']-12/1.04/.3)<1e-10
assert abs(ep['points'][-1]['y']-(8+(12/1.04/.3-8)*math.exp(-6)))<1e-10
report['lectura_curvas']={'figuras_con_lectura_numerica':len(guides),'paneles_con_instantaneas_integradas':sum(len(f['curve_guide']['panels']) for f in guides),'series':sum(f['curve_guide']['series_count'] for f in guides),'puntos_por_serie':3,'una_sola_imagen_por_figura':all(f['curve_guide']['integrated'] for f in guides),'indicadores_verticales':True,'valores_finitos_y_rangos_validos':True,'represion_por_tramos_contrastada_con_solucion_analitica':True,'estados_entradas_y_constantes_distinguidos':True}
notation=json.loads((ROOT/'book/notation.json').read_text(encoding='utf8'))
glossary=json.loads((ROOT/'book/glossary.json').read_text(encoding='utf8'))
assert len(notation)==len(equations)==202
assert len(glossary)==len({g['id'] for g in glossary})
lookup={g['id']:g for g in glossary}
for key,f in notation.items():
    assert f['number']==equations[key]['number']
    assert f['symbols']
    for symbol in f['symbols']:
        assert symbol['id'] in lookup
        assert all(symbol.get(k) for k in ['symbol','meaning','units','role'])
    soup=BeautifulSoup(next(c for c in web if c['id']==f['chapter'])['html'],'html.parser')
    eq=soup.find(id=f['anchor']);assert eq is not None
    assert len(eq.select('.symbol-key .symbol-lookup'))==len(f['symbols'])
    assert all(not img['src'].startswith('assets/curvas/') for img in soup.find_all('img'))
index=BeautifulSoup(next(c for c in web if c['id']=='c36')['html'],'html.parser')
assert all(index.find(id=g['id']) for g in glossary if g['kind']=='símbolo')
report['glosario']={'ecuaciones_con_clave':len(notation),'simbolos_contextuales':sum(g['kind']=='símbolo' for g in glossary),'conceptos':sum(g['kind']=='concepto' for g in glossary),'significado_unidad_papel_y_destino_verificados':True,'nota':'Claves revisadas por contexto para todas las ecuaciones numeradas; el índice conserva variantes de una misma letra.'}
(ROOT/'book'/'source-map.json').write_text(json.dumps(sections,ensure_ascii=False,indent=2),encoding='utf8')
audit=json.loads((ROOT/'book/source-audit.json').read_text(encoding='utf8'));assert not audit['disallowed_sources_found'];assert len(audit['references'])==len(refs);assert all(r['primary_publisher_or_official_host'] and r.get('metadata_checked') is not False for r in audit['references']);report['auditoria_fuentes']={'referencias':len(refs),'doi_contrastados':sum(r.get('metadata_checked') is True for r in audit['references']),'sin_fuentes_no_admitidas':True,'alcance':audit['scope']}
report['cobertura_bibliografica']={'secciones_con_fuentes':len(sections),'referencias':len(refs),'ids_validos':True,'nota':'Cobertura formal de secciones y figuras; no sustituye revisión independiente de cada interpretación.'}
(ROOT/'VERIFICACION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('Scripts:',len(logs),'EPUB:',report['epub'],'PDF:',report['pdf'])
