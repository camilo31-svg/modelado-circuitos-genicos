"""Integra las lecturas en el lienzo vectorial de cada figura original."""
import textwrap
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle
import ilustracion_molecular as art

def envolver(s,n):
    return '\n'.join(textwrap.wrap(s,n))

def instantaneas(ax,panel,numero):
    """Una fila por serie; misma escala vertical en los tres indicadores."""
    rows=panel['series'];n=len(rows)
    ax.set(xlim=(0,10),ylim=(0,n+.72));ax.axis('off')
    ax.text(.08,n+.55,'LECTURA '+panel['panel']+' · '+('tiempo' if panel['temporal'] else 'eje x; no es tiempo'),fontsize=7,weight='bold',color='#315e54')
    for x,marker,title in zip([3.35,5.9,8.45],['o','s','D'],['Inicio','Intermedio','Final mostrado']):
        ax.plot(x-.62,n+.27,marker=marker,ms=3.6,color='#41695d')
        ax.text(x-.44,n+.27,title,fontsize=6.8,va='center',color='#41695d')
    name=panel['y_label'].lower()
    molecular=any(w in name for w in ['arn','proteína','proteina','enzima','moléculas','moleculas','concentración','concentracion','complejo','sensor','represor','abundancia'])
    for i,row in enumerate(rows):
        y=n-i-.72;color=row['color'];scale=max(abs(row['minimum']),abs(row['maximum']),1e-15)
        ax.text(.08,y+.38,envolver(row['label'],17),fontsize=6.7,color=color,weight='bold',va='center')
        for x,point in zip([3.35,5.9,8.45],row['points']):
            value=point['y'];ratio=min(1,abs(value)/scale)
            ax.add_patch(FancyBboxPatch((x-.98,y+.15),1.96,.62,boxstyle='round,pad=.035,rounding_size=.10',facecolor='#f2f6f2',edgecolor='#c6d8ce',lw=.65))
            if molecular and row['minimum']>=-1e-10:
                count=int(np.ceil(ratio*6-1e-10)) if ratio>1e-10 else 0
                for j in range(count):
                    xx=x-.52+(j%3)*.42; yy=y+.62-(j//3)*.26
                    if 'arn' in name:art.rna(ax,xx-.12,yy,'',width=.24)
                    else:art.protein(ax,xx,yy,color,'',scale=.115)
                if not count:ax.text(x-.1,y+.4,'0',fontsize=8,color='#83988b',ha='center')
            else:
                ax.text(x-.3,y+.45,'−' if value<0 else '+',fontsize=13,color=color,ha='center',va='center')
            # Indicador vertical: no se confunde una tasa con un número de moléculas.
            gx=x+.64;gy=y+.20;gh=.48
            ax.add_patch(FancyBboxPatch((gx-.095,gy),.19,gh,boxstyle='round,pad=.015,rounding_size=.06',facecolor='#dce7df',edgecolor='#9bb6a6',lw=.55))
            if ratio>0:ax.add_patch(Rectangle((gx-.075,gy),.15,gh*ratio,facecolor=color,alpha=.85))
            for tick in [0,.5,1]:ax.plot([gx+.12,gx+.19],[gy+gh*tick]*2,color='#7a9888',lw=.5)
            xx=('t=' if panel['temporal'] else 'x=')+numero(point['x'])
            ax.text(x,y+.005,xx+'\n'+numero(value),fontsize=6.8,ha='center',va='center',linespacing=1.12,color='#264f46')
        if i<n-1:ax.plot([.07,9.65],[y-.21]*2,color='#e5ece7',lw=.6)
    ax.text(.08,-.33,envolver(panel['x_label']+'  |  '+panel['y_label']+'\nIndicador vertical relativo a cada serie; signo explícito.',53),fontsize=5.9,color='#587365',va='top')

def integrar(fig,axes,panels,numero,key,conditions):
    """Reserva franjas bajo cada fila de ejes, sin rasterizar ni copiar imágenes."""
    fig.canvas.draw()
    fig.set_layout_engine(None)
    oldw,oldh=fig.get_size_inches()
    for ax in axes:
        if len(ax.get_title())>39:ax.set_title(envolver(ax.get_title(),39))
    pos={ax:ax.get_position().frozen() for ax in fig.axes}
    # Filas del diseño original (incluye ejes sin curvas y sus barras de color).
    groups=[]
    for ax in axes:
        p=pos[ax];center=(p.y0+p.y1)/2
        group=next((g for g in groups if abs(g['center']-center)<.13),None)
        if group is None:group={'center':center,'axes':[]};groups.append(group)
        group['axes'].append(ax)
    groups.sort(key=lambda g:g['center'],reverse=True)
    mapping={p['axis_index']:p for p in panels}
    for g in groups:
        g['panels']=[(ax,mapping[axes.index(ax)]) for ax in g['axes'] if axes.index(ax) in mapping]
        g['extra']=max([1.35+.62*len(p['series']) for ax,p in g['panels']]+[0])
    # El pie documenta escalas y cambios: todo pertenece a la misma imagen.
    footer=.78;newh=oldh+sum(g['extra'] for g in groups)+footer
    fig.set_size_inches(oldw,newh)
    def below(g):return footer+sum(h['extra'] for h in groups if h['center']<=g['center'])
    for ax,p in pos.items():
        group=min(groups,key=lambda g:abs(g['center']-(p.y0+p.y1)/2))
        shift=below(group)
        ax.set_position([p.x0,(p.y0*oldh+shift)/newh,p.width,p.height*oldh/newh])
    for text in list(fig.texts):
        x,y=text.get_position();group=min(groups,key=lambda g:abs(g['center']-y))
        text.set_position((x,(y*oldh+below(group))/newh))
    for g in groups:
        if not g['panels']:continue
        low=min(pos[a].y0*oldh for a in g['axes'])
        # La etiqueta x del gráfico termina antes de la franja de instantáneas.
        base=low+below(g)-g['extra']+.24
        for ax,p in g['panels']:
            po=pos[ax]
            inset=fig.add_axes([po.x0,base/newh,po.width,(g['extra']-.84)/newh])
            instantaneas(inset,p,numero)
            p['integrated']=True;p['visual_layout']='misma figura; franja bajo el panel; indicadores verticales'
            p.pop('axis_index',None)
    fig.text(.065,.055/newh,'● inicio   ■ intermedio   ◆ final mostrado. Iconos = abundancia relativa, nunca conteos. Último punto ≠ equilibrio.',fontsize=6.4,color='#355e50',va='bottom')
    fig.text(.065,.54/newh,envolver(conditions,135),fontsize=6.6,color='#355e50',va='top')
