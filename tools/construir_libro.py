"""Construye PDF, EPUB3 y contenido web desde una fuente única verificable."""
from pathlib import Path
import re,json,hashlib,html,zipfile,shutil,textwrap,uuid,datetime,sys
import markdown
from figuras_en_texto import decorar
from lectura_curvas import parrafos as lectura_de_curvas
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
EDITION_CONFIG=json.loads((DATA/'edition.json').read_text(encoding='utf8')) if (DATA/'edition.json').exists() else {}
if not EDITION_CONFIG and (WORK/'fundamentos.json').exists():
    chapters=[];refs=[]
    for name in ['fundamentos','programacion','dinamica','inferencia','plantas','apendices']:
        chapters+=json.loads((WORK/(name+'.json')).read_text(encoding='utf-8-sig'))
        r=WORK/('refs_'+name+'.json')
        if r.exists():refs+=json.loads(r.read_text(encoding='utf-8-sig'))
    chapters.sort(key=lambda c:int(c['number']))
    assert [c['id'] for c in chapters]==[f'c{i:02}' for i in range(38)]
    ids={r['id'] for r in refs}
    assert len(ids)==len(refs)
    for c in chapters:
        assert set(re.findall(r'\[([FPDIR]\d+)\]',c['body'])) <= ids, c['id']
else:
    chapters=json.loads((DATA/'chapters.json').read_text(encoding='utf8'))
    refs=json.loads((DATA/'references.json').read_text(encoding='utf8'))
visual_path=DATA/'visuals.json'
visuals=json.loads(visual_path.read_text(encoding='utf8')) if visual_path.exists() else []
visual_refs=DATA/'visual_references.json'
if visual_refs.exists():
    existing_ids={r['id'] for r in refs}
    refs.extend(r for r in json.loads(visual_refs.read_text(encoding='utf8')) if r['id'] not in existing_ids)
for visual in visuals:
    for chapter_id in visual['chapters'][:1]:
        chapter=next(c for c in chapters if c['id']==chapter_id)
        start='<!-- VISUAL:'+visual['code']+' START -->'
        end='<!-- VISUAL:'+visual['code']+' END -->'
        section=start+'\n'+visual['section']+'\n'+end+'\n\n'
        if start in chapter['body']:
            chapter['body']=re.sub(re.escape(start)+'.*?'+re.escape(end)+'\n*',lambda m:section,chapter['body'],flags=re.S)
        else:
            headings=list(re.finditer(r'(?m)^#{2,3} ',chapter['body']))
            at=headings[1].start() if len(headings)>1 else len(chapter['body'])
            chapter['body']=chapter['body'][:at]+section+chapter['body'][at:]
        chapter['refs']=list(dict.fromkeys(chapter.get('refs',[])+visual.get('refs',[])))
refs_by_id={r['id']:r for r in refs}
for chapter in chapters:
    assert set(re.findall(r'\[([A-Z]\d{2})\]',chapter['body'])) <= set(refs_by_id),chapter['id']
(DATA/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2),encoding='utf8')
(DATA/'references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),encoding='utf8')
figures=json.loads((DOCS/'figures.json').read_text(encoding='utf8'))
for figure in figures:
    if figure.get('curve_guide'):figure['curve_guide']['readings']=lectura_de_curvas(figure['curve_guide'])
(DOCS/'figures.json').write_text(json.dumps(figures,ensure_ascii=False,indent=2),encoding='utf8')
def figure_label(f):return 'Lámina '+f['code'] if f.get('kind')=='mechanism' else 'Figura '+str(figures.index(f)+1)
PARTS=EDITION_CONFIG.get('parts') or ['I · Matemáticas desde cero','II · Del mecanismo al programa','III · Dinámica de circuitos','IV · Ruido, datos e inferencia','V · Plantas y literatura','VI · De estudiante a investigador']
for i,c in enumerate(chapters):
    c['number']=c.get('number',f'{i:02}')
    if not EDITION_CONFIG:
        c['part']=PARTS[0 if i<=7 else 1 if i<=10 else 2 if i<=18 else 3 if i<=24 else 4 if i<=31 else 5]
equations={}
def eq_replace(m,chapter_id="intro"):
    tex=re.sub(r'\s+',' ',m.group(1).strip())
    tex=re.sub(r'\\frac(\d)(\d)',r'\\frac{\1}{\2}',tex)
    key=hashlib.sha256(tex.encode()).hexdigest()[:18]
    path=EQ/(key+'.png')
    if not path.exists():
        math_to_image('$'+tex+'$',str(path),dpi=220,color='#17373d')
    equations.setdefault(key,dict(tex=tex,path='assets/equations/'+path.name,number=len(equations)+1))
    return '\n\n<div class="equation" id="eq-'+chapter_id+'-'+key+'" data-equation-number="'+str(equations[key]['number'])+'"><img src="assets/equations/'+path.name+'" alt="'+html.escape(tex,quote=True)+'" /></div>\n\n'
def render(body,chapter_id=None):
    # Desigualdades como g<n son texto, no etiquetas HTML. Conservar código y TeX.
    body=re.sub(r'<!-- VISUAL:.*?-->','',body)
    pieces=re.split(r'(```.*?```|\$\$.*?\$\$)',body,flags=re.S)
    body=''.join(piece if i%2 else piece.replace('<','&lt;') for i,piece in enumerate(pieces))
    body=re.sub(r'\$\$\s*\n?(.*?)\n?\s*\$\$',eq_replace,body,flags=re.S)
    result=markdown.markdown(body,extensions=['fenced_code','tables','sane_lists'])
    result=re.sub(r'<!-- VISUAL:.*?-->','',result)
    result=re.sub(r'\[([A-Z]\d{2})\]',lambda m:'<a class="citation" href="'+html.escape(refs_by_id[m[1]]['url'],quote=True)+'" target="_blank" rel="noopener">['+m[1]+']</a>',result)
    return decorar(result,chapter_id,figures,figure_label,refs_by_id) if chapter_id else result

app_chapters=[]
for c in chapters:
    obj=dict(c)
    obj['html']=render(c['body'],c['id'])
    obj['text']=BeautifulSoup(obj['html'],'html.parser').get_text(' ',strip=True)
    obj['minutes']=max(3,round(len(c['body'].split())/160))
    obj['figures']=[f['id'] for f in figures if c['id'] in f['chapters']]
    app_chapters.append(obj)
    (SOURCE/(c['id']+'.md')).write_text(('# '+c['title']+'\n\n'+'\n'.join('- '+o for o in c['objectives'])+'\n\n'+c['body']).rstrip()+'\n',encoding='utf8')
(DOCS/'chapters.json').write_text(json.dumps(app_chapters,ensure_ascii=False),encoding='utf8')
(DOCS/'references.json').write_text(json.dumps(refs,ensure_ascii=False),encoding='utf8')
(DATA/'equations.json').write_text(json.dumps(equations,ensure_ascii=False,indent=2),encoding='utf8')
words=sum(len(c['body'].split()) for c in chapters)
stats=dict(chapters=len(chapters),words=words,figures=len(figures),mechanisms=len(visuals),equations=sum(len(re.findall(r'\$\$',c['body']))//2 for c in chapters),unique_equations=len(equations),references=len(refs),notebooks=len(list((ROOT/'python'/'cuadernos').glob('*.ipynb'))),edition=EDITION_CONFIG.get('edition','1.1' if visuals else '1.0'),review_date=EDITION_CONFIG.get('review_date','2026-10-18'),parts=PARTS,first_chapter=chapters[0]['id'],chapter_aliases=EDITION_CONFIG.get('chapter_aliases',{}))
(DOCS/'meta.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf8')

# Una portada original reutilizable en EPUB y en el repositorio.
cover=DOCS/'assets'/'cover.png'
fig=plt.figure(figsize=(6,8.5),facecolor='#eef2e9')
ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
ax.text(.1,.91,'ATLAS DE ESTUDIO  /  '+stats['edition'],fontsize=12,color='#25685d')
ax.text(.1,.79,'Modelado\nmatemático de\ncircuitos génicos',fontsize=30,color='#17373d',weight='bold',va='top',linespacing=1.15)
ax.text(.1,.48,'De las ecuaciones diferenciales al código\nBacterias, levaduras y plantas',fontsize=13,color='#46605c',va='top')
cover_art=DOCS/'assets'/'figures'/'m01_expresion_plana.png'
if cover_art.exists():
    inset=fig.add_axes([.1,.115,.8,.31]);inset.imshow(PILImage.open(cover_art));inset.axis('off')
ax.text(.1,.055,'ESPAÑOL  ·  PYTHON  ·  MODELOS BIOLÓGICOS\nEdición de estudio · 19 de octubre de 2026',fontsize=10,color='#17373d',linespacing=1.7)
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
        elif n=='p':
            if el.get_text().lstrip().startswith('Fuentes') and out and isinstance(out[-1],Paragraph):
                out[-1].keepWithNext=True
            out.append(Paragraph(inline(el),S['TextBook']))
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
        elif n=='figure':
            im=el.find('img');cap=el.find('figcaption')
            anchor='<a name="'+el.get('id','')+'"/>'
            out.append(KeepTogether([image_flow(DOCS/im['src'],maxh=112*mm),Spacer(1,5),Paragraph(anchor+inline(cap),S['CaptionBook'])]))
            for guide in el.find_all('details'):
                for child in guide.children:
                    if getattr(child,'name',None)=='p':out.append(Paragraph(inline(child),S['CaptionBook']))
                    elif getattr(child,'name',None)=='a' and child.find('img'):
                        out.extend([Spacer(1,5),image_flow(DOCS/child.find('img')['src'],maxh=170*mm),Spacer(1,6)])
        elif n=='div' and 'equation' in el.get('class',[]):
            label=el.find('p',class_='equation-label')
            anchor='<a name="'+el.get('id','')+'"/>'
            items=[image_flow(DOCS/el.find('img')['src']),Spacer(1,3)]
            items.append(Paragraph(anchor+inline(label),S['SmallBook']))
            out.append(KeepTogether(items))
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
cover_figure=DOCS/next((f['png'] for f in figures if f.get('code')=='M01'),'assets/figures/f21_raices.png')
story=[Spacer(1,13*mm),Paragraph('ATLAS DE ESTUDIO · EDICIÓN '+stats['edition'],S['ObjectiveBook']),Spacer(1,7*mm),Paragraph('Modelado matemático<br/>de circuitos génicos',ParagraphStyle('CoverTitle',fontName='Sans-Bold',fontSize=32,leading=37,textColor=HexColor('#173f42'))),Spacer(1,8*mm),Paragraph('De las ecuaciones diferenciales al código: bacterias, levaduras y plantas',S['SubBook']),Spacer(1,6*mm),image_flow(cover_figure,maxh=65*mm),Spacer(1,8*mm),Paragraph(f'{len(chapters)} capítulos · {len(figures)} figuras originales · {stats["notebooks"]} cuadernos de Python',S['ObjectiveBook']),Paragraph('Español · modelos y programas explicados paso a paso<br/>Corte bibliográfico: 19 de octubre de 2026',S['TextBook']),PageBreak()]
story.extend([Paragraph('Antes de empezar',S['ChapterBook'])])
if (DATA/'preface.md').exists():story.extend(flow_html(render((DATA/'preface.md').read_text(encoding='utf8'))))
story.extend([PageBreak(),Paragraph('Contenido',S['ChapterBook'])])
toc=TableOfContents();toc.levelStyles=[ParagraphStyle('TOC0',fontName='Sans',fontSize=9.4,leading=14,spaceBefore=2,textColor=HexColor('#173f42'),leftIndent=0,firstLineIndent=0)]
story.extend([toc,PageBreak()]);used_figs=set()
if visuals:
    story.extend([Paragraph('Cómo leer las láminas moleculares',S['ChapterBook']),Paragraph('Las láminas M01–M12 conectan las reacciones con el modelo. Una forma lobulada representa una proteína; una doble hélice representa ADN; una hebra flexible representa ARN. Son ilustraciones conceptuales planas, generadas con una herramienta de imágenes y revisadas para comprobar relaciones y etiquetas. Las formas no son estructuras atomísticas ni están a escala.',S['TextBook']),Paragraph('Lee primero los objetos y después las conexiones. Una flecha de producción indica aparición de una especie; no significa que el molde de ADN o ARN se consuma. Una barra perpendicular indica inhibición. Dos flechas opuestas representan procesos reversibles. Una flecha entre compartimentos indica transporte. El recambio elimina moléculas de la especie contada, aunque su materia continúe en otros productos.',S['TextBook']),Paragraph('Cada lámina tiene una lectura por paneles, una limitación y una conexión con las ecuaciones. Los gráficos cuantitativos existentes complementan estos mecanismos: muestran la respuesta temporal, las distribuciones o la relación entre entradas y salidas. Las curvas esquemáticas dentro de las láminas son cualitativas y no son datos medidos.',S['TextBook']),Paragraph('En el móvil, abre la figura y usa la vista de alta resolución para inspeccionar etiquetas. El repositorio guarda también los textos de los prompts y la procedencia de cada imagen. Las figuras son originales y no reutilizan activos de BioRender ni figuras de revistas.',S['TextBook']),PageBreak()])
for c,app in zip(chapters,app_chapters):
    story.extend([Paragraph(pdf_text(c['part']),S['SmallBook']),Paragraph(c['number']+' · '+pdf_text(c['title']),S['ChapterBook'])])
    for ob in c['objectives']:story.append(Paragraph('• '+pdf_text(ob),S['ObjectiveBook']))
    story.append(Spacer(1,8))
    story+=flow_html(app['html'])
    if c.get('refs'):
        # La lista de fuentes debe acompañar al cierre del capítulo.
        if isinstance(story[-1],Paragraph):story[-1].keepWithNext=True
        story.append(Paragraph('Fuentes del capítulo: '+', '.join('['+x+']' for x in c['refs']),S['SmallBook']))
    story.append(PageBreak())
story.append(Paragraph('Referencias y trazabilidad',S['ChapterBook']))
story.append(Paragraph('Fecha de consulta: 19 de octubre de 2026. Se conservan identificadores por módulo aunque una obra pueda aparecer en más de un módulo. Las notas distinguen consulta de resumen, texto completo, documentación y revisión. Los enlaces permiten verificar la fuente y sus posibles correcciones posteriores.',S['TextBook']))
for r in refs:
    authors=r.get('authors','');authors='; '.join(authors) if isinstance(authors,list) else authors
    txt='<b>['+r['id']+'] '+pdf_text(r['title'])+'</b><br/>'+pdf_text(str(authors))+'. '+str(r['year'])+'. '+pdf_text(r['type'])+'.'
    if r.get('doi'):txt+='<br/>DOI: <a href="https://doi.org/'+r['doi']+'" color="#167d7c">'+html.escape(r['doi'])+'</a>'
    txt+='<br/><a href="'+html.escape(r['url'],quote=True)+'" color="#167d7c">Abrir fuente</a>. '+pdf_text(r.get('note',''))
    story.append(Paragraph(txt,S['SmallBook']));story.append(Spacer(1,5))
if '--epub-only' not in sys.argv:book.multiBuild(story)

# EPUB3 refluible: imágenes locales, navegación y capítulos semánticos.
epub=DOWNLOADS/'modelado-circuitos-genicos.epub'
epub_css='''body{font-family:serif;line-height:1.6;margin:5%;color:#203936}h1,h2,h3{font-family:sans-serif;color:#205d51;line-height:1.25}h1{font-size:1.8em}p{margin:.7em 0}img{max-width:100%;height:auto}.equation{text-align:center;overflow:auto;margin:1em 0}.equation img{max-height:5em;width:auto;vertical-align:middle}figure{margin:1.2em 0}figcaption{font-size:.85em;line-height:1.45}pre{white-space:pre-wrap;font-size:.8em;padding:.8em;background:#edf1ed}code{font-family:monospace}table{border-collapse:collapse;width:100%;font-size:.85em}td,th{border-bottom:1px solid #bbc9c1;padding:.4em;vertical-align:top}a{color:#236b60}.part{font-family:sans-serif;font-size:.85em;color:#6b7a70}'''
def xhtml(title,body):
    soup=BeautifulSoup(body,'html.parser')
    for button in soup.select('button[data-figure]'):button.unwrap()
    for a in soup.find_all('a'):
        a.attrs.pop('target',None);a.attrs.pop('rel',None)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" lang="es" xml:lang="es"><head><title>'+html.escape(title)+'</title><meta charset="utf-8"/><link rel="stylesheet" type="text/css" href="style.css"/></head><body>'+str(soup)+'</body></html>'
manifest=[('css','style.css','text/css',''),('nav','nav.xhtml','application/xhtml+xml','nav'),('ncx','toc.ncx','application/x-dtbncx+xml',''),('cover','assets/cover.png','image/png','cover-image'),('intro','intro.xhtml','application/xhtml+xml',''),('refs','references.xhtml','application/xhtml+xml','')]
spine=['intro'];nav=[];uid='urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'https://github.com/camilo31-svg/modelado-circuitos-genicos/edition'+stats['edition']))
with zipfile.ZipFile(epub,'w') as z:
    z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
    def put(p,s):z.writestr(p,s,compress_type=zipfile.ZIP_DEFLATED)
    put('META-INF/container.xml','<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
    put('OEBPS/style.css',epub_css)
    put('OEBPS/intro.xhtml',xhtml('Antes de empezar','<img src="assets/cover.png" alt="Portada del Atlas"/><h1>Antes de empezar</h1>'+render((DATA/'preface.md').read_text(encoding='utf8'))))
    seen=set()
    for c in app_chapters:
        prefix='<p class="part">'+html.escape(c['part'])+'</p><h1>'+c['number']+' · '+html.escape(c['title'])+'</h1><ul>'+''.join('<li>'+html.escape(o)+'</li>' for o in c['objectives'])+'</ul>'
        body=prefix+c['html']
        put('OEBPS/'+c['id']+'.xhtml',xhtml(c['title'],body));manifest.append((c['id'],c['id']+'.xhtml','application/xhtml+xml',''));spine.append(c['id']);nav.append((c['id']+'.xhtml',c['number']+' · '+c['title']))
    refbody='<h1>Referencias y trazabilidad</h1>'
    for r in refs:refbody+='<p id="'+r['id']+'"><b>['+r['id']+'] '+html.escape(r['title'])+'</b> ('+str(r['year'])+'). '+html.escape(r['type'])+'. <a href="'+html.escape(r['url'],quote=True)+'">Fuente</a>. '+html.escape(r.get('note',''))+'</p>'
    put('OEBPS/references.xhtml',xhtml('Referencias',refbody));spine.append('refs')
    navbody='<h1>Contenido</h1><nav epub:type="toc" id="toc" xmlns:epub="http://www.idpf.org/2007/ops"><ol><li><a href="intro.xhtml">Antes de empezar</a></li>'+''.join('<li><a href="'+p+'">'+html.escape(t)+'</a></li>' for p,t in nav)+'<li><a href="references.xhtml">Referencias</a></li></ol></nav>'
    put('OEBPS/nav.xhtml',xhtml('Contenido',navbody))
    ncx='<?xml version="1.0" encoding="UTF-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="'+uid+'"/></head><docTitle><text>Modelado matemático de circuitos génicos</text></docTitle><navMap>'+''.join('<navPoint id="nav'+str(i)+'" playOrder="'+str(i)+'"><navLabel><text>'+html.escape(t)+'</text></navLabel><content src="'+p+'"/></navPoint>' for i,(p,t) in enumerate([('intro.xhtml','Antes de empezar')]+nav+[('references.xhtml','Referencias')],1))+'</navMap></ncx>'
    put('OEBPS/toc.ncx',ncx)
    image_paths=[cover]+[DOCS/e['path'] for e in equations.values()]+[DOCS/f['png'] for f in figures]+[DOCS/p['visual_png'] for f in figures if f.get('curve_guide') for p in f['curve_guide']['panels'] if p.get('visual_png')]
    for p in dict.fromkeys(image_paths):
        rel=p.relative_to(DOCS).as_posix();put('OEBPS/'+rel,p.read_bytes())
        if p!=cover:manifest.append(('im'+hashlib.md5(rel.encode()).hexdigest(),rel,'image/png',''))
    opf='<?xml version="1.0" encoding="UTF-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="es"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="bookid">'+uid+'</dc:identifier><dc:title>Modelado matemático de circuitos génicos</dc:title><dc:language>es</dc:language><dc:creator>Atlas de estudio · generado con Codex</dc:creator><dc:description>Formación en español desde ecuaciones diferenciales, con análisis detallado, circuitos complejos, ejemplos de distintos organismos y Python explicado.</dc:description><meta property="dcterms:modified">2026-10-19T12:00:00Z</meta><meta name="cover" content="cover"/></metadata><manifest>'+''.join('<item id="'+i+'" href="'+p+'" media-type="'+m+'"'+(' properties="'+pr+'"' if pr else '')+'/>' for i,p,m,pr in manifest)+'</manifest><spine toc="ncx">'+''.join('<itemref idref="'+i+'"/>' for i in spine)+'</spine></package>'
    put('OEBPS/content.opf',opf)
from pypdf import PdfReader
stats['pages']=len(PdfReader(pdf).pages)
(DOCS/'meta.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf8')
deliver=BASE/'outputs';deliver.mkdir(exist_ok=True)
for p in [pdf,epub]:shutil.copy2(p,deliver/p.name)
print(json.dumps(stats,ensure_ascii=False,indent=2))
