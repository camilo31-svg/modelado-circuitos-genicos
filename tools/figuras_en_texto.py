"""Una colocación compartida de referencias, ecuaciones y figuras para tres formatos."""
import html,re,unicodedata
from bs4 import BeautifulSoup
from lectura_curvas import parrafos

def normalizar(text):
    return ''.join(c for c in unicodedata.normalize('NFD',text.lower()) if not unicodedata.combining(c))

def citar(text,refs):
    safe=html.escape(text)
    return re.sub(r'\[([A-Z]\d{2})\]',lambda m:'<a class="citation" href="'+html.escape(refs[m[1]]['url'],quote=True)+'">['+m[1]+']</a>',safe)

def decorar(raw,chapter_id,figures,label,refs):
    soup=BeautifulSoup(raw,'html.parser')
    # Cada fórmula tiene llamada en la prosa y un destino único por capítulo.
    for eq in soup.select('div.equation[data-equation-number]'):
        number=eq['data-equation-number'];target=eq['id']
        previous=next((p for p in eq.find_all_previous('p') if not p.find_parent('figure') and not p.find_parent('div',class_='equation')),None)
        ref=BeautifulSoup(' <a class="local-ref equation-ref" href="#'+target+'">[ecuación ('+number+')]</a>','html.parser')
        if previous and not previous.find_parent('figure'):
            previous.append(' ')
            previous.append(ref.a)
        else:
            p=soup.new_tag('p');p['class']='equation-reference';p.append(ref.a);eq.insert_before(p)
        cap=soup.new_tag('p');cap['class']='equation-label';cap.string='Ecuación ('+number+')';eq.append(cap)
    last_at={}
    for f in figures:
        if chapter_id not in f['chapters']:continue
        target_id='fig-'+chapter_id+'-'+f['id']
        f_label=label(f)
        guide=''
        if f.get('kind')=='mechanism':
            guide='<details class="panel-guide"><summary>Leer la lámina por paneles</summary>'+''.join('<p><strong>'+html.escape(p['label']+' · '+p['title'])+'.</strong> '+citar(p['text'],refs)+'</p>' for p in f.get('panels',[]))+'<p>'+citar(f.get('limitation',''),refs)+'</p></details>'
        if f.get('curve_guide'):
            readings=parrafos(f['curve_guide']);panels=f['curve_guide']['panels']
            guide+='<details class="curve-guide"><summary>Valores y condiciones de la figura integrada</summary>'
            for i,(title,text) in enumerate(readings):
                guide+='<p><strong>'+html.escape(title)+'.</strong> '+citar(text,refs)+'</p>'
            guide+='</details>'
        content='<p class="figure-reference">La <a class="local-ref" href="#'+target_id+'">'+html.escape(f_label)+'</a> acompaña este paso: '+html.escape(f['title'])+'.</p><figure id="'+target_id+'" class="figure-in-lesson"><button data-figure="'+f['id']+'" aria-label="Ampliar: '+html.escape(f['title'],quote=True)+'"><img src="'+f['png']+'" alt="'+html.escape(f['alt'],quote=True)+'" loading="lazy"/></button><figcaption><strong>'+html.escape(f_label+'. '+f['title'])+'.</strong> '+citar(f['caption'],refs)+'</figcaption>'+guide+'</figure>'
        nodes=list(BeautifulSoup(content,'html.parser').contents)
        hint=f.get('after_heading')
        anchor=None;before=False
        if hint:
            heading=next((h for h in soup.find_all(['h2','h3']) if normalizar(hint) in normalizar(h.get_text(' ',strip=True))),None)
            if heading:
                anchor=heading;level=int(heading.name[1])
                for sibling in heading.next_siblings:
                    if getattr(sibling,'name',None) in ['h2','h3'] and int(sibling.name[1])<=level:break
                    if getattr(sibling,'name',None):anchor=sibling
        if anchor is None and f.get('kind')=='mechanism':
            anchor=next((h for h in soup.find_all(['h2','h3']) if f.get('code','NONE') in h.get_text()),None)
            before=anchor is not None
        if anchor is None:
            anchor=soup.select_one('div.equation')
        if anchor is None:
            headings=soup.find_all(['h2','h3'])
            if len(headings)>1:anchor=headings[1];before=True
            else:anchor=soup.find('p') or soup.find()
        key=id(anchor)
        if key in last_at:anchor=last_at[key];before=False
        for node in nodes:
            if before:anchor.insert_before(node)
            elif anchor:anchor.insert_after(node);anchor=node
            else:soup.append(node)
        last_at[key]=nodes[-1]
    return str(soup)
