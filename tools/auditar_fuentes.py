"""Auditoría reproducible de procedencia, citas y metadatos, no fact-check total."""
from pathlib import Path
import time,json,re,urllib.request,urllib.parse,concurrent.futures,datetime,html,difflib
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'outputs/atlas-circuitos-genicos'
if not ROOT.exists():ROOT=BASE
refs=json.loads((ROOT/'book/references.json').read_text(encoding='utf8'))
chapters=json.loads((ROOT/'book/chapters.json').read_text(encoding='utf8'))
DOMAINS={'openstax.org','ocw.mit.edu','python.org','docs.python.org','numpy.org','matplotlib.org','docs.scipy.org','jupyter.org','docs.sciml.ai','cran.r-project.org','mathworks.com','copasi.org','cobrapy.readthedocs.io','tellurium.readthedocs.io','pubmed.ncbi.nlm.nih.gov','pmc.ncbi.nlm.nih.gov','nature.com','portlandpress.com','journals.plos.org','doi.org','link.springer.com','sbml.org','sed-ml.org','pure.ed.ac.uk','math.uwaterloo.ca','mat.univie.ac.at','sites.stat.columbia.edu','bipm.org','math.mit.edu','research-figure-guide.nature.com'}
BAD=['wikipedia.org','wikimedia.org','wikibooks.org','fandom.com','reddit.com','scribd.com','blogspot.com']
def normalize(s):return re.sub('[^a-z0-9]','',html.unescape(s).lower())
cached={}
prior=ROOT/'book/source-audit.json'
if prior.exists():cached={r['id']:r for r in json.loads(prior.read_text(encoding='utf8'))['references']}
def metadata(ref):
    old=cached.get(ref['id'],{})
    if old.get('metadata_checked') is True and old.get('title')==ref['title'] and old.get('url')==ref['url']:return old
    result=dict(id=ref['id'],title=ref['title'],url=ref['url'])
    domain=urllib.parse.urlparse(ref['url']).netloc.lower().removeprefix('www.')
    result['domain']=domain;result['primary_publisher_or_official_host']=domain in DOMAINS
    assert result['primary_publisher_or_official_host'],(ref['id'],domain)
    doi=ref.get('doi')
    if not doi:
        match=re.search(r'doi.org/(.+)',ref['url']);doi=match[1] if match else None
    if doi:
        time.sleep(.8)
        try:
            req=urllib.request.Request('https://api.crossref.org/works/'+urllib.parse.quote(doi,safe=''),headers={'User-Agent':'CircuitosAtlas/2.3 academic-source-audit','Accept':'application/json'})
            with urllib.request.urlopen(req,timeout=30) as response:message=json.load(response)['message']
            title=message.get('title',[''])[0]
            result.update(doi=doi,crossref_title=title,title_similarity=round(difflib.SequenceMatcher(None,normalize(ref['title']),normalize(title)).ratio(),3),metadata_checked=True,publication_type=message.get('type'),dates={k:message[k]['date-parts'] for k in ['published','published-online','published-print'] if k in message},updates=message.get('update-to',[]))
        except Exception as exc:result.update(metadata_checked=False,error=type(exc).__name__+': '+str(exc)[:160])
    else:result['metadata_checked']='sin DOI; fuente institucional o documentación identificada'
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:rows=list(pool.map(metadata,refs))
scans=[]
for path in [ROOT/'book/chapters.json',ROOT/'book/references.json',ROOT/'book/preface.md',ROOT/'book/visuals.json',ROOT/'book/notation.json']:
    if path.exists():
        text=path.read_text(encoding='utf8').lower()
        for domain in BAD:
            if domain in text:scans.append(dict(file=path.name,domain=domain))
assert not scans,scans
sections=[]
for ch in chapters:
    for section in re.split(r'(?m)(?=^#{2,3} )',ch['body']):
        if not section.strip():continue
        cited=list(dict.fromkeys(re.findall(r'\[([A-Z]\d{2})\]',section)))
        sections.append(dict(chapter=ch['id'],heading=section.splitlines()[0].lstrip('# '),references=cited))
report=dict(manual_reviews=[dict(id='A28',resolution='Título ampliado para identificar actualización 2026, verificada en BIPM; el DOI identifica la edición base de 2019.'),dict(id='A06',resolution='Publicación en línea de 2025 y volumen editorial de 2026; se conservan ambas fechas en la referencia.')],edition='2.3',date='2026-10-19',references=rows,disallowed_sources_found=scans,source_policy='Publicaciones científicas, libros universitarios y documentación primaria oficial. Los ejemplos originales son derivaciones o simulaciones identificadas, no datos experimentales atribuidos a artículos.',sections=sections,scope='Inspección de procedencia y citas de todos los apartados; contraste de metadatos de DOI con Crossref y revisión de pasajes seleccionados con sus fuentes primarias. No es una verificación independiente, frase por frase, de toda la obra.')
(ROOT/'book/source-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('Fuentes:',len(rows),'sin dominios prohibidos; DOI contrastados:',sum(r.get('metadata_checked') is True for r in rows))
for r in rows:
    if r.get('metadata_checked') is False or (isinstance(r.get('title_similarity'),float) and r['title_similarity']<.8):print('REVISAR',r)
for r in rows:
    if r['id'] in ['A06','P06','P12']:print('FECHAS',r)
