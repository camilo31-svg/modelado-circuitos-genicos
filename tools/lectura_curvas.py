"""Lecturas verificables extraídas de los datos realmente dibujados.

Los marcadores indican orden de muestreo, nunca cambios de parámetros implícitos.
"""
import string,unicodedata,colorsys,textwrap
from pathlib import Path
import numpy as np
from matplotlib.colors import to_hex,to_rgb
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Rectangle
import ilustracion_molecular as art

EVENTOS={
 'f01_unidades':'En A aumenta el volumen prescrito V/V₀=exp(0,2t); la cantidad se conserva y la concentración disminuye. La tasa de crecimiento 0,2/h permanece constante.',
 'f11_logica':'En A la entrada u pasa de 0 a 1 en t=2 h. Cambia esa entrada; las constantes cinéticas permanecen fijas. La rama lenta y la salida son estados que responden después.',
 'f12_retrasos':'En A cada curva tiene un retraso fijo distinto (1, 3 o 6 h). En B la entrada cambia de 0 a 1 en t=2 h; las tres constantes de relajación siguen en 2/h.',
 'f16_rafagas':'El promotor alterna aleatoriamente entre 0 y 1 y cambia la producción efectiva. Es un estado discreto variable; kon, koff y las tasas declaradas no cambian durante esta realización.',
 'g06_rafagas':'El estado discreto del promotor y el número de ARN fluctúan. Las constantes de conmutación, producción en ON y pérdida se mantienen; los parámetros barridos en otros paneles corresponden a simulaciones diferentes.',
 'f22_memoria':'En A la entrada pasa de 0 a 1 en t=3 h y vuelve a 0 tras t=6 h. La tasa de registro durante la exposición es 0,6/h. La probabilidad acumulada permanece después del pulso.',
 'g04_control':'En t=30 h se modifica deliberadamente la pérdida de Y: γ pasa de 1 a 2/h. μ, θ, k y η permanecen constantes. Cada curva tiene una dilución de control δc fija (0 o 0,05/h), distinta entre simulaciones.',
 'q15_dos_vias':'La entrada se fija a u=1 desde el inicio mostrado. Las constantes permanecen en uno; cambian los estados y y z y, por ello, los flujos que dependen de ellos.',
 'q16_sensor':'Desde t=0 la entrada A se mantiene en 5. s=1, γ₀=0,1 y k=0,02 permanecen constantes. Cambia el sensor S; la estimación estática varía porque omite su pendiente.',
 'q17_represion':'En t=5 h cambia la entrada represora R de 1 a 10 nM. La capacidad smax=12 nM/h, K=5 nM, n=2 y δ=0,3/h permanecen constantes. Cambia la tasa efectiva s(R) y después cambia la concentración de enzima E.',
}

def limpio(s):
    return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if not unicodedata.combining(c))

def numero(v):
    if abs(v)<1e-13:v=0.
    return f'{v:.4g}'.replace('.',',')

def nombre_color(color):
    h,s,v=colorsys.rgb_to_hsv(*to_rgb(color))
    if s<.17:return 'negro' if v<.3 else ('gris' if v<.88 else 'blanco')
    if h<.04 or h>=.95:return 'rojo'
    if h<.12:return 'naranja'
    if h<.20:return 'amarillo'
    if h<.44:return 'verde'
    if h<.54:return 'turquesa'
    if h<.70:return 'azul'
    if h<.85:return 'violeta'
    return 'rosa'

def crear_grafiquito(key,panel):
    """Tres instantáneas por serie, con cantidades relativas y valores exactos."""
    base=Path(__file__).resolve().parents[1];root=base/'outputs/atlas-circuitos-genicos'
    if not root.exists():root=base
    out=root/'docs/assets/curvas';out.mkdir(parents=True,exist_ok=True)
    rows=panel['series'];n=len(rows)
    fig,axes=plt.subplots(n+1,1,figsize=(7.4,1.05+.87*n),height_ratios=[.7]+[1]*n,layout='constrained')
    header=axes[0];header.axis('off')
    header.text(.005,.88,'Panel '+panel['panel']+' · '+panel['title'],fontsize=9,weight='bold',color='#244e49',va='top')
    label='Momentos del recorrido' if panel['temporal'] else 'Puntos del eje horizontal: no son momentos sucesivos'
    header.text(.005,.40,label,fontsize=8,color='#4a6d62')
    for x,title in [(3.3,'● Inicio'),(6.2,'■ Intermedio'),(9.1,'◆ Final mostrado')]:header.text(x/10,.02,title,ha='center',fontsize=8,weight='bold',color='#315e54')
    name=limpio(panel['y_label'])
    molecular=any(word in name for word in ['arn','proteina','enzima','moleculas','concentracion','complejo','sensor','represor','abundancia'])
    for ax,row in zip(axes[1:],rows):
        ax.axis('off');ax.set(xlim=(0,10),ylim=(0,1.15));color=row['color']
        ax.text(.02,.76,'\n'.join(textwrap.wrap(row['label'],24)),ha='left',va='center',fontsize=8,color=color,weight='bold')
        ax.text(.02,.26,nombre_color(color),fontsize=7,color='#5a756b')
        scale=max(abs(row['minimum']),abs(row['maximum']),1e-15)
        for xpos,point in zip([3.3,6.2,9.1],row['points']):
            val=point['y'];ratio=abs(val)/scale;is_molecular=molecular and row['minimum']>=-1e-10
            ax.add_patch(FancyBboxPatch((xpos-.78,.40),1.56,.64,boxstyle='round,pad=.03,rounding_size=.1',facecolor='#f2f6f0',edgecolor='#b7cec2',lw=.7))
            if is_molecular:
                count=int(np.ceil(ratio*8-1e-10)) if ratio>1e-10 else 0
                for j in range(count):
                    px=xpos-.53+(j%4)*.35;py=.86-(j//4)*.29
                    if 'arn' in name:art.rna(ax,px-.10,py,'',width=.23)
                    else:art.protein(ax,px,py,color,'',scale=.105)
                if count==0:ax.text(xpos,.72,'vacío / cero',ha='center',fontsize=7,color='#7a9184')
            else:
                # Una probabilidad, error, fase o tasa se representa por una escala;
                # nunca se inventan moléculas negativas ni identidades químicas.
                ax.plot([xpos-.57,xpos+.57],[.66,.66],color='#b9cbbf',lw=1)
                ax.add_patch(Rectangle((xpos-.57,.59),1.14*ratio,.15,facecolor=color,alpha=.8))
                if val<0:ax.text(xpos,.85,'valor negativo',ha='center',fontsize=6.5,color='#9b5046')
            ax.text(xpos,.18,'x='+numero(point['x'])+'\ny='+numero(val),ha='center',va='center',fontsize=8.8,color='#244e49')
        for x in [4.55,7.45]:ax.add_patch(FancyArrowPatch((x,.71),(x+.38,.71),arrowstyle='-|>',mutation_scale=8,color='#819e8c',lw=.9))
    note='Iconos: abundancia relativa, sin contar moléculas. Barras: magnitudes abstractas, tasas o valores con signo. x e y conservan las unidades de los ejes.'
    fig.text(.5,-.015,note,ha='center',fontsize=6.5,color='#4d6b60')
    slug=key+'_'+panel['panel']
    for ext in ['png','svg']:fig.savefig(out/(slug+'.'+ext),dpi=200,bbox_inches='tight')
    plt.close(fig)
    panel['visual_png']='assets/curvas/'+slug+'.png';panel['visual_svg']='assets/curvas/'+slug+'.svg'
    panel['visual_alt']='Lectura gráfica con tres instantáneas del panel '+panel['panel']+'. '+panel['y_label']+'. Los iconos indican abundancia relativa, no conteos moleculares.'

def extraer(fig,key):
    panels=[];total=0
    axes=[a for a in fig.axes if a.get_label()!='<colorbar>']
    for ai,ax in enumerate(axes):
        if not ax.axison:continue
        xlabel=ax.get_xlabel();ylabel=ax.get_ylabel()
        if not xlabel or not ylabel:continue
        xname=limpio(xlabel)
        temporal=('tiempo' in xname or xname.startswith(('τ','tau'))) and not any(w in xname for w in ['espera','duracion','paso'])
        series=[]
        for line in list(ax.lines):
            if line.get_transform()!=ax.transData:continue
            x=np.asarray(line.get_xdata(),dtype=float);y=np.asarray(line.get_ydata(),dtype=float)
            if x.shape!=y.shape or x.ndim!=1 or len(x)<2:continue
            good=np.isfinite(x)&np.isfinite(y)
            if good.sum()<2:continue
            x=x[good];y=y[good]
            if np.ptp(x)==0:continue # segmentos de residuos o referencias verticales
            # Una nube de puntos observados no se convierte en trayectoria.
            if str(line.get_linestyle()).lower() in ['none',''] and len(x)<4:continue
            label=line.get_label()
            if not label or label.startswith('_'):label=(ylabel if len(ax.lines)==1 else 'Serie '+str(len(series)+1))
            color=to_hex(line.get_color());indices=[0,len(x)//2,len(x)-1]
            xl=sorted(ax.get_xlim());yl=sorted(ax.get_ylim())
            points=[dict(x=float(x[i]),y=float(y[i]),visible=bool(xl[0]<=x[i]<=xl[1] and yl[0]<=y[i]<=yl[1] and (ax.get_xscale()!='log' or x[i]>0) and (ax.get_yscale()!='log' or y[i]>0))) for i in indices]
            dy=np.diff(y);tol=max(1.,np.max(np.abs(y)))*1e-7
            if np.max(y)-np.min(y)<=tol:trend='se mantiene'
            elif np.all(dy>=-tol):trend='aumenta'
            elif np.all(dy<=tol):trend='disminuye'
            else:trend='cambia de sentido; los extremos no describen todo el recorrido'
            series.append(dict(label=label,color=color,points=points,minimum=float(y.min()),maximum=float(y.max()),trend=trend))
            for i,marker in zip(indices,['o','s','D']):
                ax.plot([x[i]],[y[i]],marker=marker,ms=3.8,mew=.6,mec='white',mfc=color,ls='none',zorder=20,clip_on=True)
        if series:
            total+=len(series)
            panel=dict(panel=string.ascii_uppercase[ai],title=ax.get_title(),x_label=xlabel,y_label=ylabel,temporal=temporal,series=series)
            crear_grafiquito(key,panel)
            panels.append(panel)
    if panels:
        fig.text(.5,-.025,'● primer punto   ■ punto intermedio   ◆ último punto · valores y condiciones bajo la figura',ha='center',fontsize=6.7,color='#355c55')
    if not panels:return None
    guide=dict(panels=panels,series_count=total,parameter_behavior=EVENTOS.get(key,'Las constantes se mantienen durante cada simulación. Cuando distintas curvas comparan valores de un parámetro, ese valor cambia entre simulaciones; no está variando a lo largo de una misma trayectoria.'),caution='Los valores se extraen de los puntos dibujados y están redondeados a cuatro cifras significativas. El último punto es el final del intervalo mostrado: no demuestra equilibrio. En ejes que no representan tiempo, el orden de puntos no es una evolución temporal.')
    guide['readings']=parrafos(guide)
    return guide

def parrafos(guide):
    if not guide:return []
    result=[('Condiciones y parámetros',guide['parameter_behavior'])]
    for panel in guide['panels']:
        mode='recorrido temporal' if panel['temporal'] else 'recorrido del eje horizontal; no es tiempo'
        text=f"{panel['title']}. {mode}. Coordenadas: ({panel['x_label']}; {panel['y_label']}). "
        for row in panel['series']:
            coords=['('+numero(p['x'])+'; '+numero(p['y'])+')'+(' [fuera de la escala visible]' if not p.get('visible',True) else '') for p in row['points']]
            text+=row['label']+' ('+nombre_color(row['color'])+'): inicio '+coords[0]+', intermedio '+coords[1]+', final '+coords[2]+'. '+row['trend'].capitalize()+'. Rango vertical '+numero(row['minimum'])+' a '+numero(row['maximum'])+'. '
        result.append(('Panel '+panel['panel'],text.strip()))
    result.append(('Cómo interpretarlo',guide['caution']))
    return result
