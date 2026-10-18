"""Construye PDF, EPUB3 y contenido web desde una fuente única verificable."""
from pathlib import Path
import re,json,hashlib,html,zipfile,shutil,textwrap,uuid,datetime
import markdown
from bs4 import BeautifulSoup, NavigableString
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import findfont,FontProperties
from fontTools.ttLib import TTFont as FontToolsFont
from reportlab.platypus import (BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,
    Image,KeepTogether,Table,TableStyle,Preformatted)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor,white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists():ROOT=BASE
SOURCE=ROOT/'book'/'source'
SOURCE.mkdir(parents=True,exist_ok=True)
DOCS=ROOT/'docs';EQ=DOCS/'assets'/'equations';EQ.mkdir(parents=True,exist_ok=True)
DATA=ROOT/'book';DOWNLOADS=DOCS/'downloads';DOWNLOADS.mkdir(exist_ok=True)
WORK=BASE/'work' if (BASE/'work').exists() else ROOT/'work'
if (WORK/'fundamentos.json').exists():
    chapters=[];refs=[]
    for name in ['fundamentos','programacion','dinamica','inferencia','plantas','apendices']:
        chapters+=json.loads((WORK/(name+'.json')).read_text(encoding='utf-8-sig'))
        r=WORK/('refs_'+name+'.json')
        if r.exists():refs+=json.loads(r.read_text(encoding='utf-8-sig'))
    chapters.sort(key=lambda c:int(c['id'][1:]))
    assert [c['id'] for c in chapters]==[f'c{i:02}' for i in range(38)]
    ids={r['id'] for r in refs}
    assert len(ids)==len(refs)
    for c in chapters:
        assert set(re.findall(r'\[([FPDIR]\d+)\]',c['body'])) <= ids, c['id']
    (DATA/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2),encoding='utf8')
    (DATA/'references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),encoding='utf8')
else:
    chapters=json.loads((DATA/'chapters.json').read_text(encoding='utf8'))
    refs=json.loads((DATA/'references.json').read_text(encoding='utf8'))
refs_by_id={r['id']:r for r in refs}
figures=json.loads((DOCS/'figures.json').read_text(encoding='utf8'))
PARTS=['I · Matemáticas desde cero','II · Del mecanismo al programa','III · Dinámica de circuitos','IV · Ruido, datos e inferencia','V · Plantas y literatura','VI · De estudiante a investigador']
def part(i):return PARTS[0 if i<=7 else 1 if i<=10 else 2 if i<=18 else 3 if i<=24 else 4 if i<=31 else 5]
for i,c in enumerate(chapters):c['part']=part(i)
equations={}
def eq_replace(m):
    tex=m.group(1).strip()
    key=hashlib.sha256(tex.encode()).hexdigest()[:18]
    path=EQ/(key+'.png')
    if not path.exists():
        math_to_image('$'+tex+'$',str(path),dpi=220,color='#17373d')
    equations[key]=dict(tex=tex,path='assets/equations/'+path.name)
    return '\n\n<div class="equation"><img src="assets/equations/'+path.name+'" alt="'+html.escape(tex,quote=True)+'" /></div>\n\n'
def render(body):
    body=re.sub(r'\$\$\s*\n?(.*?)\n?\s*\$\$',eq_replace,body,flags=re.S)
    result=markdown.markdown(body,extensions=['fenced_code','tables','sane_lists'])
    return re.sub(r'\[([FPDIR]\d+)\]',lambda m:'<a class="citation" href="'+html.escape(refs_by_id[m[1]]['url'],quote=True)+'" target="_blank" rel="noopener">['+m[1]+']</a>',result)

app_chapters=[]
for c in chapters:
    obj=dict(c)
    obj['html']=render(c['body'])
    obj['text']=BeautifulSoup(obj['html'],'html.parser').get_text(' ',strip=True)
    obj['minutes']=max(3,round(len(c['body'].split())/160))
    obj['figures']=[f['id'] for f in figures if c['id'] in f['chapters']]
    app_chapters.append(obj)
    (SOURCE/(c['id']+'.md')).write_text('# '+c['title']+'\n\n'+'\n'.join('- '+o for o in c['objectives'])+'\n\n'+c['body'],encoding='utf8')
(DOCS/'chapters.json').write_text(json.dumps(app_chapters,ensure_ascii=False),encoding='utf8')
(DOCS/'references.json').write_text(json.dumps(refs,ensure_ascii=False),encoding='utf8')
(DATA/'equations.json').write_text(json.dumps(equations,ensure_ascii=False,indent=2),encoding='utf8')
words=sum(len(c['body'].split()) for c in chapters)
stats=dict(chapters=len(chapters),words=words,figures=len(figures),equations=sum(len(re.findall(r'\$\$',c['body']))//2 for c in chapters),unique_equations=len(equations),references=len(refs),notebooks=10,edition='1.0',review_date='2026-10-18',parts=PARTS)
(DOCS/'meta.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf8')

# Una portada original reutilizable en EPUB y en el repositorio.
cover=DOCS/'assets'/'cover.png'
fig=plt.figure(figsize=(6,8.5),facecolor='#eef2e9')
ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
ax.text(.1,.91,'ATLAS DE ESTUDIO  /  01',fontsize=12,color='#25685d')
ax.text(.1,.79,'Modelado\nmatemático de\ncircuitos génicos',fontsize=30,color='#17373d',weight='bold',va='top',linespacing=1.15)
ax.text(.1,.48,'De las primeras ecuaciones\na la investigación en biología sintética',fontsize=13,color='#46605c',va='top')
coords=np.array([[.2,.2],[.43,.31],[.7,.21],[.79,.38],[.48,.13]])
for a,b in [(0,1),(1,2),(2,3),(1,4),(4,2)]:ax.plot(coords[[a,b],0],coords[[a,b],1],color='#81a798',lw=2)
for j,(x,y) in enumerate(coords):ax.scatter([x],[y],s=1400 if j==1 else 700,color='#236c5c' if j%2 else '#c77542',edgecolor='#eef2e9',lw=2,zorder=3)
ax.text(.1,.055,'ESPAÑOL  ·  PYTHON  ·  PLANTAS\nEdición de estudio · 18 de octubre de 2026',fontsize=10,color='#17373d',linespacing=1.7)
fig.savefig(cover,dpi=180);plt.close(fig)

# PDF: tipografía incrustada, índice navegable y ecuaciones en alta resolución.
FONT=Path('C:/Windows/Fonts')
PDF_COMMON=None
for name,file in [('Body','georgia.ttf'),('Body-Bold','georgiab.ttf'),('Body-Italic','georgiai.ttf'),('Body-BoldItalic','georgiaz.ttf'),('Sans','arial.ttf'),('Sans-Bold','arialbd.ttf'),('Mono','consola.ttf')]:
    fontpath=FONT/file
    if not fontpath.exists():
        family='DejaVu Sans Mono' if name=='Mono' else 'DejaVu Sans' if name.startswith('Sans') else 'DejaVu Serif'
        fontpath=Path(findfont(FontProperties(family=family,weight='bold' if 'Bold' in name else 'normal',style='italic' if 'Italic' in name else 'normal')))
    pdfmetrics.registerFont(TTFont(name,str(fontpath)))
    coverage=set(FontToolsFont(fontpath).getBestCmap())
    PDF_COMMON=coverage if PDF_COMMON is None else PDF_COMMON & coverage
fallback_path=findfont('DejaVu Sans')
pdfmetrics.registerFont(TTFont('Fallback',fallback_path))
def pdf_text(value):
    return ''.join(html.escape(ch) if ord(ch) in PDF_COMMON or ord(ch)<32 else '<font name="Fallback">'+html.escape(ch)+'</font>' for ch in str(value))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Body-Bold',italic='Body-Italic',boldItalic='Body-BoldItalic')
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='Sans-Bold',italic='Sans',boldItalic='Sans-Bold')
S=getSampleStyleSheet()
S.add(ParagraphStyle(name='TextBook',fontName='Body',fontSize=10.4,leading=15.4,spaceAfter=8,textColor=HexColor('#233638'),allowWidows=0,allowOrphans=0))
S.add(ParagraphStyle(name='ChapterBook',fontName='Sans-Bold',fontSize=24,leading=29,spaceAfter=18,textColor=HexColor('#173f42'),keepWithNext=True))
S.add(ParagraphStyle(name='SubBook',fontName='Sans-Bold',fontSize=13,leading=17,spaceBefore=12,spaceAfter=8,textColor=HexColor('#25685d'),keepWithNext=True))
S.add(ParagraphStyle(name='SmallBook',fontName='Sans',fontSize=8.2,leading=11.5,spaceAfter=6,textColor=HexColor('#4c5e5b')))
S.add(ParagraphStyle(name='CaptionBook',parent=S['SmallBook'],fontSize=8.3,leading=12,spaceAfter=12))
S.add(ParagraphStyle(name='ObjectiveBook',fontName='Sans',fontSize=9.5,leading=13,spaceAfter=5,textColor=HexColor('#25685d'),leftIndent=10))
S.add(ParagraphStyle(name='QuoteBook',parent=S['TextBook'],fontName='Body-Italic',leftIndent=14,borderColor=HexColor('#b5d0c5'),borderPadding=7,borderWidth=.5))
S.add(ParagraphStyle(name='CodeBook',fontName='Mono',fontSize=7.1,leading=10,spaceBefore=5,spaceAfter=10,leftIndent=7,backColor=HexColor('#f0f3f2'),borderPadding=7))
W,H=180*mm,250*mm;M=19*mm;CONTENT=W-2*M
def inline(node):
    if isinstance(node,NavigableString):return pdf_text(str(node))
    name=node.name
    inner=''.join(inline(n) for n in node.children)
    if name in ['b','strong']:return '<b>'+inner+'</b>'
    if name in ['i','em']:return '<i>'+inner+'</i>'
    if name=='code':return '<font name="Mono" size="8.7">'+inner+'</font>'
    if name=='a':return '<a href="'+html.escape(node.get('href',''),quote=True)+'" color="#167d7c">'+inner+'</a>'
    if name=='br':return '<br/>'
    if name=='sup':return '<super>'+inner+'</super>'
    if name=='sub':return '<sub>'+inner+'</sub>'
    return inner
def image_flow(path,maxw=CONTENT,maxh=120*mm):
    w,h=PILImage.open(path).size
    if 'equations' in str(path):
        scale=min(72/220,maxw/w,maxh/h)
    else:scale=min(maxw/w,maxh/h)
    return Image(str(path),width=w*scale,height=h*scale,hAlign='CENTER')
def flow_html(raw):
    soup=BeautifulSoup(raw,'html.parser');out=[]
    def walk(el):
        if isinstance(el,NavigableString):
            if str(el).strip():out.append(Paragraph(pdf_text(str(el)),S['TextBook']))
            return
        n=el.name
        if n in ['h1','h2','h3','h4','h5']:
            out.append(Paragraph(inline(el),S['SubBook']))
        elif n=='p':out.append(Paragraph(inline(el),S['TextBook']))
        elif n in ['ul','ol']:
            for j,li in enumerate(el.find_all('li',recursive=False)):
                bullet=str(j+1)+'.' if n=='ol' else '•'
                out.append(Paragraph(bullet+' '+inline(li),S['TextBook']))
        elif n=='pre':
            src=el.get_text().replace('\t','    ')
            lines=[]
            for line in src.splitlines():
                if len(line)<=87:lines.append(line)
                else:lines.extend(textwrap.wrap(line,87,subsequent_indent='    ',replace_whitespace=False,drop_whitespace=False,break_long_words=True))
            out.append(Preformatted('\n'.join(lines),S['CodeBook']))
        elif n=='div' and el.find('img'):
            for im in el.find_all('img'):out.extend([image_flow(DOCS/im['src']),Spacer(1,7)])
        elif n=='blockquote':out.append(Paragraph(inline(el),S['QuoteBook']))
        elif n=='table':
            rows=[]
            for tr in el.find_all('tr'):
                rows.append([Paragraph(inline(td),S['SmallBook']) for td in tr.find_all(['th','td'],recursive=False)])
            if rows:
                cols=max(map(len,rows));rows=[r+['']*(cols-len(r)) for r in rows]
                table=Table(rows,colWidths=[CONTENT/cols]*cols,repeatRows=1,hAlign='LEFT')
                table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#e4eee8')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4),('LINEBELOW',(0,0),(-1,0),.5,HexColor('#98b1a9')),('LINEBELOW',(0,1),(-1,-1),.3,HexColor('#d6dfdb'))]))
                out.extend([table,Spacer(1,8)])
        elif n=='hr':out.append(Spacer(1,10))
        else:
            for child in el.children:walk(child)
    for el in soup.contents:walk(el)
    return out
class Book(BaseDocTemplate):
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and f.style.name=='ChapterBook':
            key='b'+str(self.seq.nextf('bookmark'))
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(f.getPlainText(),key,0,False)
            self.notify('TOCEntry',(0,f.getPlainText(),self.page,key))
def page(canvas,doc):
    canvas.saveState()
    if doc.page>1:
        canvas.setStrokeColor(HexColor('#c3d1c9'));canvas.setLineWidth(.4)
        canvas.line(M,H-14*mm,W-M,H-14*mm)
        canvas.setFont('Sans',7.2);canvas.setFillColor(HexColor('#657670'))
        canvas.drawString(M,H-11*mm,'ATLAS · MODELADO MATEMÁTICO DE CIRCUITOS GÉNICOS')
        canvas.drawRightString(W-M,11*mm,str(doc.page))
    canvas.restoreState()
pdf=DOWNLOADS/'modelado-circuitos-genicos.pdf'
book=Book(str(pdf),pagesize=(W,H),rightMargin=M,leftMargin=M,topMargin=21*mm,bottomMargin=18*mm,title='Modelado matemático de circuitos génicos',author='Atlas de estudio · material educativo generado con Codex',lang='es-ES',allowSplitting=1)
book.addPageTemplates(PageTemplate(id='main',frames=[Frame(M,18*mm,CONTENT,H-39*mm,id='normal',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=page))
story=[Spacer(1,16*mm),Paragraph('ATLAS DE ESTUDIO · EDICIÓN 1.0',S['ObjectiveBook']),Spacer(1,8*mm),Paragraph('Modelado matemático<br/>de circuitos génicos',ParagraphStyle('CoverTitle',fontName='Sans-Bold',fontSize=32,leading=37,textColor=HexColor('#173f42'))),Spacer(1,10*mm),Paragraph('De las primeras ecuaciones a la investigación en biología sintética',S['SubBook']),Spacer(1,8*mm),image_flow(DOCS/'assets'/'figures'/'f21_raices.png',maxh=55*mm),Spacer(1,10*mm),Paragraph(f'{len(chapters)} capítulos · {len(figures)} figuras originales · 10 cuadernos de Python',S['ObjectiveBook']),Paragraph('Español · especial atención a plantas<br/>Corte bibliográfico: 18 de octubre de 2026',S['TextBook']),PageBreak()]
story.extend([Paragraph('Antes de empezar',S['ChapterBook']),Paragraph('Este libro está pensado para una persona que conoce las biopartes y empieza de cero en matemáticas. Lee con papel, lápiz y un intérprete de Python. Una ecuación se aprende al explicar sus términos, cambiar un supuesto y comprobar una predicción.',S['TextBook']),Paragraph('Alcance y procedencia',S['SubBook']),Paragraph('Es una formación extensa y una selección bibliográfica razonada; no una revisión sistemática de toda la literatura ni una garantía de dominio experto. Los temas avanzados abren rutas de profundización. Las referencias indican qué se verificó y cuándo solo se consultaron metadatos o resúmenes. Las revisiones de 2025–2026 orientan el estado del campo, mientras los casos experimentales se apoyan en artículos primarios.',S['TextBook']),Paragraph('Todas las figuras y los ejemplos numéricos son originales y didácticos. Sus parámetros no son calibraciones de los artículos citados. No se reproducen figuras de revistas. El estilo gráfico usa convenciones de publicación científica: paneles, ejes con unidades, leyendas y supuestos explícitos.',S['TextBook']),Paragraph('Material generado con Codex y sometido a comprobaciones numéricas, bibliográficas y de formato. Todavía no cuenta con una revisión independiente completa por especialistas. Usa el registro de limitaciones como parte del aprendizaje de la lectura crítica.',S['TextBook']),Paragraph('Cómo se conectan los formatos',S['SubBook']),Paragraph('El PDF, el EPUB y la app se construyen con los mismos capítulos. El repositorio contiene los Markdown, los modelos, scripts de figuras y cuadernos. La app permite buscar texto y descripciones de figuras, guardar progreso en el dispositivo, ajustar letra y descargar los materiales. El uso sin conexión requiere descargar antes los recursos desde la propia app.',S['TextBook']),Paragraph('Convención de capítulos',S['SubBook']),Paragraph('La numeración empieza en 00: es una introducción que también funciona como lección. Los identificadores c00–c37 son los mismos en el código y en la app. Las referencias entre corchetes enlazan a fuentes y se desarrollan al final con una nota de verificación.',S['TextBook']),PageBreak(),Paragraph('Contenido',S['ChapterBook'])])
toc=TableOfContents();toc.levelStyles=[ParagraphStyle('TOC0',fontName='Sans',fontSize=9.4,leading=14,spaceBefore=4,textColor=HexColor('#173f42'),leftIndent=0,firstLineIndent=0)]
story.extend([toc,PageBreak()]);used_figs=set()
for c,app in zip(chapters,app_chapters):
    story.extend([Paragraph(pdf_text(c['part']),S['SmallBook']),Paragraph(c['id'][1:]+' · '+pdf_text(c['title']),S['ChapterBook'])])
    for ob in c['objectives']:story.append(Paragraph('• '+pdf_text(ob),S['ObjectiveBook']))
    story.append(Spacer(1,8))
    # La figura se sitúa tras el primer apartado: primero una pregunta, luego la imagen.
    raw=app['html'];spl=re.split(r'(?=<h[23]>)',raw)
    first=spl.pop(0) if spl else raw
    if not first and spl:first=spl.pop(0)
    story+=flow_html(first)
    for f in figures:
        if c['id'] in f['chapters'] and f['id'] not in used_figs:
            used_figs.add(f['id']);n=figures.index(f)+1
            story.append(KeepTogether([image_flow(DOCS/f['png'],maxh=91*mm),Spacer(1,5),Paragraph('<b>Figura '+str(n)+'. '+pdf_text(f['title'])+'.</b> '+pdf_text(f['caption']),S['CaptionBook'])]))
    story+=flow_html(''.join(spl))
    if c.get('refs'):
        story.append(Paragraph('Fuentes del capítulo: '+', '.join('['+x+']' for x in c['refs']),S['SmallBook']))
    story.append(PageBreak())
story.append(Paragraph('Referencias y trazabilidad',S['ChapterBook']))
story.append(Paragraph('Fecha de consulta: 18 de octubre de 2026. Se conservan identificadores por módulo aunque una obra pueda aparecer en más de un módulo. Las notas distinguen consulta de resumen, texto completo, documentación y revisión. Los enlaces permiten verificar la fuente y sus posibles correcciones posteriores.',S['TextBook']))
for r in refs:
    authors=r.get('authors','');authors='; '.join(authors) if isinstance(authors,list) else authors
    txt='<b>['+r['id']+'] '+pdf_text(r['title'])+'</b><br/>'+pdf_text(str(authors))+'. '+str(r['year'])+'. '+pdf_text(r['type'])+'.'
    if r.get('doi'):txt+='<br/>DOI: <a href="https://doi.org/'+r['doi']+'" color="#167d7c">'+html.escape(r['doi'])+'</a>'
    txt+='<br/><a href="'+html.escape(r['url'],quote=True)+'" color="#167d7c">Abrir fuente</a>. '+pdf_text(r.get('note',''))
    story.append(Paragraph(txt,S['SmallBook']));story.append(Spacer(1,5))
book.multiBuild(story)

# EPUB3 refluible: imágenes locales, navegación y capítulos semánticos.
epub=DOWNLOADS/'modelado-circuitos-genicos.epub'
epub_css='''body{font-family:serif;line-height:1.6;margin:5%;color:#203936}h1,h2,h3{font-family:sans-serif;color:#205d51;line-height:1.25}h1{font-size:1.8em}p{margin:.7em 0}img{max-width:100%;height:auto}.equation{text-align:center;overflow:auto;margin:1em 0}.equation img{max-height:5em;width:auto;vertical-align:middle}figure{margin:1.2em 0}figcaption{font-size:.85em;line-height:1.45}pre{white-space:pre-wrap;font-size:.8em;padding:.8em;background:#edf1ed}code{font-family:monospace}table{border-collapse:collapse;width:100%;font-size:.85em}td,th{border-bottom:1px solid #bbc9c1;padding:.4em;vertical-align:top}a{color:#236b60}.part{font-family:sans-serif;font-size:.85em;color:#6b7a70}'''
def xhtml(title,body):
    soup=BeautifulSoup(body,'html.parser')
    for a in soup.find_all('a'):
        a.attrs.pop('target',None);a.attrs.pop('rel',None)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" lang="es" xml:lang="es"><head><title>'+html.escape(title)+'</title><meta charset="utf-8"/><link rel="stylesheet" type="text/css" href="style.css"/></head><body>'+str(soup)+'</body></html>'
manifest=[('css','style.css','text/css',''),('nav','nav.xhtml','application/xhtml+xml','nav'),('ncx','toc.ncx','application/x-dtbncx+xml',''),('cover','assets/cover.png','image/png','cover-image'),('intro','intro.xhtml','application/xhtml+xml',''),('refs','references.xhtml','application/xhtml+xml','')]
spine=['intro'];nav=[];uid='urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'https://github.com/camilo31-svg/modelado-circuitos-genicos/edition1'))
with zipfile.ZipFile(epub,'w') as z:
    z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
    def put(p,s):z.writestr(p,s,compress_type=zipfile.ZIP_DEFLATED)
    put('META-INF/container.xml','<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
    put('OEBPS/style.css',epub_css)
    put('OEBPS/intro.xhtml',xhtml('Antes de empezar','<img src="assets/cover.png" alt="Portada del Atlas"/><h1>Antes de empezar</h1><p>Formación desde cero, con una selección bibliográfica razonada hasta el 18 de octubre de 2026. Ejemplos y figuras originales; parámetros didácticos, sin reconstruir datos de artículos. Revisión especialista independiente pendiente.</p><p>La numeración comienza en 00. Avanza con papel, lápiz y los cuadernos del repositorio. El PDF y la app contienen las mismas lecciones. Los temas avanzados exigen profundizar en las referencias.</p>'))
    seen=set()
    for c in app_chapters:
        body='<p class="part">'+html.escape(c['part'])+'</p><h1>'+c['id'][1:]+' · '+html.escape(c['title'])+'</h1><ul>'+''.join('<li>'+html.escape(o)+'</li>' for o in c['objectives'])+'</ul>'+c['html']
        for f in figures:
            if c['id'] in f['chapters'] and f['id'] not in seen:
                seen.add(f['id']);body+='<figure><img src="'+f['png']+'" alt="'+html.escape(f['alt'],quote=True)+'"/><figcaption>Figura '+str(figures.index(f)+1)+'. '+html.escape(f['title'])+'. '+html.escape(f['caption'])+'</figcaption></figure>'
        put('OEBPS/'+c['id']+'.xhtml',xhtml(c['title'],body));manifest.append((c['id'],c['id']+'.xhtml','application/xhtml+xml',''));spine.append(c['id']);nav.append((c['id']+'.xhtml',c['id'][1:]+' · '+c['title']))
    refbody='<h1>Referencias y trazabilidad</h1>'
    for r in refs:refbody+='<p id="'+r['id']+'"><b>['+r['id']+'] '+html.escape(r['title'])+'</b> ('+str(r['year'])+'). '+html.escape(r['type'])+'. <a href="'+html.escape(r['url'],quote=True)+'">Fuente</a>. '+html.escape(r.get('note',''))+'</p>'
    put('OEBPS/references.xhtml',xhtml('Referencias',refbody));spine.append('refs')
    navbody='<h1>Contenido</h1><nav epub:type="toc" id="toc" xmlns:epub="http://www.idpf.org/2007/ops"><ol><li><a href="intro.xhtml">Antes de empezar</a></li>'+''.join('<li><a href="'+p+'">'+html.escape(t)+'</a></li>' for p,t in nav)+'<li><a href="references.xhtml">Referencias</a></li></ol></nav>'
    put('OEBPS/nav.xhtml',xhtml('Contenido',navbody))
    ncx='<?xml version="1.0" encoding="UTF-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="'+uid+'"/></head><docTitle><text>Modelado matemático de circuitos génicos</text></docTitle><navMap>'+''.join('<navPoint id="nav'+str(i)+'" playOrder="'+str(i)+'"><navLabel><text>'+html.escape(t)+'</text></navLabel><content src="'+p+'"/></navPoint>' for i,(p,t) in enumerate([('intro.xhtml','Antes de empezar')]+nav+[('references.xhtml','Referencias')],1))+'</navMap></ncx>'
    put('OEBPS/toc.ncx',ncx)
    for p in [cover]+list(EQ.glob('*.png'))+list((DOCS/'assets'/'figures').glob('*.png')):
        rel=p.relative_to(DOCS).as_posix();put('OEBPS/'+rel,p.read_bytes())
        if p!=cover:manifest.append(('im'+hashlib.md5(rel.encode()).hexdigest(),rel,'image/png',''))
    opf='<?xml version="1.0" encoding="UTF-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="es"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="bookid">'+uid+'</dc:identifier><dc:title>Modelado matemático de circuitos génicos</dc:title><dc:language>es</dc:language><dc:creator>Atlas de estudio · generado con Codex</dc:creator><dc:description>Formación en español desde cero, con énfasis vegetal, figuras originales y Python.</dc:description><meta property="dcterms:modified">2026-10-18T12:00:00Z</meta><meta name="cover" content="cover"/></metadata><manifest>'+''.join('<item id="'+i+'" href="'+p+'" media-type="'+m+'"'+(' properties="'+pr+'"' if pr else '')+'/>' for i,p,m,pr in manifest)+'</manifest><spine toc="ncx">'+''.join('<itemref idref="'+i+'"/>' for i in spine)+'</spine></package>'
    put('OEBPS/content.opf',opf)
from pypdf import PdfReader
stats['pages']=len(PdfReader(pdf).pages)
(DOCS/'meta.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf8')
deliver=BASE/'outputs';deliver.mkdir(exist_ok=True)
for p in [pdf,epub]:shutil.copy2(p,deliver/p.name)
print(json.dumps(stats,ensure_ascii=False,indent=2))
