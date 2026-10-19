"""Una guía por práctica, compartida por libro, app y cuadernos."""
from pathlib import Path
import json,re
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists():ROOT=BASE
guides=json.loads((ROOT/'book'/'practice-guides.json').read_text(encoding='utf8'))
p=ROOT/'docs'/'labs.json';labs=json.loads(p.read_text(encoding='utf8'))
sections=['## Lectura guiada de las 25 prácticas\n\nEstas fichas explican objetos, índices, cálculos y límites de cada programa. Se utilizan junto a las derivaciones del capítulo y al código ejecutable, con una guía común de sintaxis y arrays. [R20] [R21] [R05]']
for lab in labs:
    slug,title,intro,sources,lessons=lab[:5]
    assert slug in guides
    guide=guides[slug]
    if len(lab)==5:lab.append(guide)
    else:lab[5]=guide
    sections.append('### Práctica '+slug[:2]+': '+title+'\n\n'+guide+'\n\nFuentes de los principios: '+' '.join('['+r+']' for r in sources)+'.')
    path=ROOT/'python'/'cuadernos'/(slug+'.ipynb')
    nb=json.loads(path.read_text(encoding='utf8'))
    nb['cells']=[c for c in nb['cells'] if c.get('id')!=slug+'-lectura']
    nb['cells'].insert(1,{'cell_type':'markdown','metadata':{},'id':slug+'-lectura','source':('## Lectura del código\n\n'+guide).splitlines(True)})
    path.write_text(json.dumps(nb,ensure_ascii=False,indent=2),encoding='utf8')
p.write_text(json.dumps(labs,ensure_ascii=False),encoding='utf8')
p=ROOT/'book'/'chapters.json';cs=json.loads(p.read_text(encoding='utf8'))
c=next(c for c in cs if c['id']=='c34')
c['body']=c['body'].split('\n## Lectura guiada de las 25 prácticas')[0].rstrip()+'\n\n'+'\n\n'.join(sections)+'\n'
c['refs']=list(dict.fromkeys(re.findall(r'\[([A-Z]\d{2})\]',c['body'])))
p.write_text(json.dumps(cs,ensure_ascii=False,indent=2),encoding='utf8')
print('Guías de código integradas:',len(guides))
