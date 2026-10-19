"""Curva, especie e indicador comparten un panel legible y ampliable.

Las ampliaciones son recortes vectoriales del mismo lienzo, con curva y
lectura juntas. En el libro, las láminas largas continúan por filas completas.
"""
from pathlib import Path
import re,textwrap
import numpy as np
from matplotlib.patches import FancyBboxPatch,Rectangle
from matplotlib.transforms import Bbox,Affine2D
import ilustracion_molecular as art

INK='#203e45';MUTED='#4a6268';LINE='#cddcdd';BG='#f3f7f6';FONT=9.5
def envolver(s,n):return '\n'.join(textwrap.wrap(str(s),n,break_long_words=False))

def especie(ax,x,y,name,color):
    """El icono identifica, no cuenta ni mide; el indicador lleva el valor."""
    s=name.lower();before=set(ax.get_children())
    if 'arn' in s:art.rna(ax,-.25,0,'',width=.50)
    elif any(w in s for w in ['prote','enzima','represor','sensor','complejo']):art.protein(ax,0,0,color,'',scale=.20)
    else:
        ax.text(x,y,'valor',fontsize=FONT,color=MUTED,ha='center',va='center');return
    w,h=ax.figure.get_size_inches();p=ax.get_position()
    correction=(p.width*w/3)/(p.height*h/(ax.get_ylim()[1]-ax.get_ylim()[0]))
    transform=Affine2D().scale(1,correction).translate(x,y)+ax.transData
    for item in set(ax.get_children())-before:item.set_transform(transform)

def instantaneas(ax,panel,numero):
    rows=panel['series'];n=len(rows)
    ax.set(xlim=(0,3),ylim=(0,n*2+.70));ax.axis('off')
    for x,marker,title in zip([.5,1.5,2.5],['o','s','D'],['Inicio','Intermedio','Final']):
        ax.plot(x-.29,n*2+.43,marker=marker,ms=4.8,color=MUTED)
        ax.text(x-.18,n*2+.43,title,fontsize=FONT,color=INK,va='center')
    for i,row in enumerate(rows):
        top=(n-i)*2+.18;col=row['color'];label=row['label']
        if label.startswith('Serie '):label=panel['y_label']+' · '+label
        ax.text(.04,top,envolver(label,42),fontsize=FONT,weight='bold',color=col,va='top',linespacing=1.05)
        maximum=max(abs(row['minimum']),abs(row['maximum']),1e-15);signed=row['minimum']< -1e-10
        for x,point in zip([.5,1.5,2.5],row['points']):
            y=top-1.35;value=point['y']
            ax.add_patch(FancyBboxPatch((x-.43,y+.30),.86,.70,boxstyle='round,pad=.018,rounding_size=.065',facecolor=BG,edgecolor=LINE,lw=.8))
            especie(ax,x-.09,y+.65,panel['y_label'],col)
            gx=x+.28;gy=y+.40;gh=.43
            ax.add_patch(FancyBboxPatch((gx-.045,gy),.09,gh,boxstyle='round,pad=.007,rounding_size=.025',facecolor='#dce8e7',edgecolor='#95b2b3',lw=.7))
            if signed:
                zero=gy+gh/2;fill=.5*gh*abs(value)/maximum
                ax.add_patch(Rectangle((gx-.033,zero if value>=0 else zero-fill),.066,fill,facecolor=col))
                ax.plot([gx-.08,gx+.08],[zero]*2,color=MUTED,lw=.8)
            else:
                ax.add_patch(Rectangle((gx-.033,gy),.066,gh*max(0,value)/maximum,facecolor=col))
                ax.plot([gx-.08,gx+.08],[gy]*2,color=MUTED,lw=.8)
            dagger='†' if not point.get('visible',True) else ''
            ax.text(x,y+.15,numero(value)+dagger,fontsize=11,weight='bold',ha='center',va='center',color=INK)
            xx=('t = ' if panel['temporal'] else 'x = ')+numero(point['x'])
            ax.text(x,y-.10,xx,fontsize=FONT,ha='center',va='center',color=MUTED)
        lo=-maximum if signed else 0
        ax.text(.04,top-1.64,'Indicador: '+numero(lo)+' a '+numero(maximum),fontsize=FONT,color=MUTED,va='top')

def integrar(fig,axes,panels,numero,key,conditions):
    fig.canvas.draw();fig.set_layout_engine(None)
    original={a:a.get_position().frozen() for a in fig.axes};groups=[]
    for ax in axes:
        center=(original[ax].y0+original[ax].y1)/2
        g=next((g for g in groups if abs(g['center']-center)<.13),None)
        if g is None:g=dict(center=center,axes=[]);groups.append(g)
        g['axes'].append(ax)
    groups.sort(key=lambda g:g['center'],reverse=True);byaxis={p['axis_index']:p for p in panels}
    for g in groups:
        g['axes'].sort(key=lambda a:original[a].x0)
        count=max([len(byaxis[axes.index(a)]['series']) for a in g['axes'] if axes.index(a) in byaxis]+[0])
        g['reading']=.52+1.30*count if count else 0;g['height']=3.40+g['reading']
    lines=textwrap.wrap(conditions,102,break_long_words=False);foot=.65+.16*len(lines)
    width=8.;height=sum(g['height'] for g in groups)+.28*(len(groups)-1)+foot+.18
    fig.set_size_inches(width,height)
    for txt in list(fig.texts):txt.remove()
    ytop=height-.12;views=[];book=[];colorbars=[a for a in fig.axes if a not in axes]
    for gi,g in enumerate(groups):
        bottom=ytop-g['height'];rowletters=[]
        for ci,ax in enumerate(g['axes']):
            ai=axes.index(ax);letter=chr(65+ai);rowletters.append(letter);left=.30+ci*3.86;cw=3.54
            title=re.sub(r'^[A-Z]\s*[·:–-]\s*','',ax.get_title()).strip();ax.set_title('')
            for txt in list(ax.texts):
                if re.fullmatch('[A-Z]',txt.get_text().strip()) and txt.get_transform()==ax.transAxes and txt.get_position()[1]>1:txt.remove()
                else:
                    txt.set_fontsize(max(FONT,txt.get_fontsize()))
                    if txt.get_text()=='ribosoma':
                        px,py=txt.get_position();txt.set_position((px,py+.75))
            fig.text(left/width,(ytop-.04)/height,letter+'  '+envolver(title,37),fontsize=10.5,weight='bold',va='top',color=INK,linespacing=1.15)
            associates=[bar for bar in colorbars if min(axes,key=lambda a:abs((original[a].y0+original[a].y1)/2-(original[bar].y0+original[bar].y1)/2)+abs(original[a].x1-original[bar].x0)) is ax]
            # Las etiquetas categóricas largas y las escalas de color necesitan
            # espacio propio; nunca invaden la columna contigua.
            ytick_length=max([len(t.get_text()) for t in ax.get_yticklabels()]+[0])
            xpad=.85 if ytick_length>9 else .55
            xplot=left+xpad if ax.axison else left+.03;pwidth=cw-xpad-.07-(.75 if associates else 0) if ax.axison else cw-.06;yplot=ytop-2.73
            ax.set_position([xplot/width,yplot/height,pwidth/width,2.15/height])
            if ax.axison:
                ax.xaxis.label.set_size(10);ax.yaxis.label.set_size(10);ax.tick_params(labelsize=FONT);ax.xaxis.labelpad=6;ax.yaxis.labelpad=5
                legend=ax.get_legend()
                if legend:
                    for txt in legend.get_texts():txt.set_fontsize(FONT)
                    legend.get_frame().set_linewidth(.6)
            for bar in associates:
                bar.set_position([(xplot+pwidth+.10)/width,yplot/height,.10/width,2.15/height]);bar.tick_params(labelsize=FONT);bar.yaxis.label.set_size(FONT)
            p=byaxis.get(ai)
            if p:
                rh=.52+1.30*len(p['series']);rbase=ytop-3.28-rh
                inset=fig.add_axes([left/width,rbase/height,cw/width,rh/height]);instantaneas(inset,p,numero)
                p['integrated']=True;p['visual_layout']='curva e instantáneas en el mismo panel; indicadores verticales con cero';p.pop('axis_index',None)
            vh=3.28+(.52+1.30*len(p['series']) if p else 0)+.15
            views.append(dict(panel=letter,title=title,bounds=[left-.16,ytop-vh,cw+.32,vh]))
        book.append(dict(panels=rowletters,bounds=[.05,bottom,width-.10,g['height']]))
        ytop=bottom-.28
    fig.text(.035,(foot-.05)/height,'CONDICIONES  '+'\n'.join(lines),fontsize=FONT,color=INK,va='top',linespacing=1.2)
    fig.text(.035,.37/height,'Un icono identifica la especie; la barra indica el valor. Cada serie tiene su escala. † Fuera del encuadre.',fontsize=FONT,color=MUTED,va='top')
    fig.text(.035,.16/height,'● primer punto   ■ punto intermedio   ◆ último punto. El último punto mostrado no demuestra equilibrio.',fontsize=FONT,color=MUTED,va='top')
    base=Path(__file__).resolve().parents[1];root=base/'outputs/atlas-circuitos-genicos'
    if not root.exists():root=base
    out=root/'docs/assets/paneles';out.mkdir(exist_ok=True)
    for view in views:
        name=key+'_'+view['panel']+'.png';fig.savefig(out/name,dpi=220,bbox_inches=Bbox.from_bounds(*view['bounds']),pad_inches=0)
        view['png']='assets/paneles/'+name;view.pop('bounds')
    for i,view in enumerate(book):
        name=key+'_fila'+str(i+1)+'.png';fig.savefig(out/name,dpi=220,bbox_inches=Bbox.from_bounds(*view['bounds']),pad_inches=0)
        view['png']='assets/paneles/'+name;view['width_in']=width-.10;view['height_in']=view['bounds'][3];view.pop('bounds')
    fig.canvas.draw();renderer=fig.canvas.get_renderer();warnings=[]
    for ai,ax in enumerate(axes):
        labels=[t for t in ax.texts if t.get_text().strip()]
        for i,a in enumerate(labels):
            aa=a.get_window_extent(renderer)
            for b in labels[i+1:]:
                bb=b.get_window_extent(renderer);ow=min(aa.x1,bb.x1)-max(aa.x0,bb.x0);oh=min(aa.y1,bb.y1)-max(aa.y0,bb.y0)
                if ow>3 and oh>3:warnings.append(dict(panel=chr(65+ai),a=a.get_text(),b=b.get_text()))
    return dict(layout_warnings=warnings,panel_views=views,book_views=book,minimum_font_pt=FONT,design='2.3 · paneles completos legibles')
