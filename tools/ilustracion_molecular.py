"""Ilustración vectorial original: formas planas con dominios y detalle molecular.

No usa activos de BioRender ni representa estructuras atomísticas específicas.
Las formas distinguen ADN, ARN, complejos, dominios proteicos y maquinaria.
"""
import numpy as np
from matplotlib.patches import PathPatch,Polygon,FancyArrowPatch,Ellipse
from matplotlib.path import Path
from matplotlib.colors import to_rgb

def light(color,amount=.3):
    c=np.asarray(to_rgb(color));return tuple(c+(1-c)*amount)

def protein(ax,x,y,color,label,scale=.28):
    angle=np.linspace(0,2*np.pi,180)
    radius=scale*(1+.16*np.sin(3*angle+.5)+.10*np.sin(5*angle)-.06*np.cos(2*angle))
    xy=np.c_[x+radius*np.cos(angle),y+.78*radius*np.sin(angle)]
    ax.add_patch(PathPatch(Path(xy,closed=True),facecolor=color,edgecolor='#34565c',lw=.8,zorder=5))
    # Dominios suaves y una hendidura de unión: detalle conceptual, no estructura.
    ax.add_patch(Ellipse((x-.18*scale,y+.20*scale),.98*scale,.62*scale,angle=22,facecolor=light(color,.5),edgecolor='none',alpha=.8,zorder=6))
    ax.add_patch(Ellipse((x+.35*scale,y-.16*scale),.72*scale,.65*scale,angle=-25,facecolor=light(color,.18),edgecolor='none',zorder=6))
    t=np.linspace(-.65,.65,50)
    ax.plot(x+scale*t,y+scale*(-.38+.12*np.sin(7*t)),color=light(color,.7),lw=.8,alpha=.9,zorder=7)
    if label:ax.text(x,y-.03*scale,label,ha='center',va='center',color='white',fontsize=8,weight='bold',zorder=9)

def dna(ax,x,y,label,width=1.):
    xx=np.linspace(x,x+width,220);phase=(xx-x)/width*4*np.pi
    amp=.075
    ax.plot(xx,y+amp*np.sin(phase),color='#447d9f',lw=1.7,zorder=3)
    ax.plot(xx,y-amp*np.sin(phase),color='#7fa7a6',lw=1.7,zorder=3)
    for j in range(19):
        px=x+width*j/18;py=amp*np.sin(j/18*4*np.pi)
        ax.plot([px,px],[y-py,y+py],color='#aabec1' if j%2 else '#d3b9a4',lw=.65,zorder=2)
    # Caja promotora y dirección de transcripción sobre la doble hélice.
    ax.add_patch(Polygon([[x+.09*width,y-.1],[x+.09*width,y+.1],[x+.28*width,y+.1],[x+.28*width,y-.1]],closed=True,facecolor='#bdcdbb',edgecolor='#688976',lw=.6,alpha=.9,zorder=4))
    ax.add_patch(FancyArrowPatch((x+.15*width,y+.20),(x+.88*width,y+.20),arrowstyle='-|>',mutation_scale=7,color='#31836c',lw=1,zorder=8))
    # Polimerasa en la salida: cuerpo y canal que aloja el ADN.
    protein(ax,x+.69*width,y+.09,'#9c89a5','',scale=.16)
    ax.add_patch(Ellipse((x+.69*width,y+.05),.14,.07,facecolor='#f7f6ec',edgecolor='#7a6a85',lw=.5,zorder=8))
    if label:ax.text(x+width*.5,y-.30,label,ha='center',fontsize=8,zorder=10)

def rna(ax,x,y,label,width=.65):
    xx=np.linspace(x,x+width,180);yy=y+.065*np.sin((xx-x)/width*5*np.pi)
    ax.plot(xx,yy,color='#7b5b9b',lw=1.8,zorder=4)
    for j in range(12):
        px=x+width*(j+.3)/12;py=y+.065*np.sin((px-x)/width*5*np.pi)
        ax.plot([px,px+.015],[py,py-.065],color=['#b99ac5','#87adb1','#d7b38e'][j%3],lw=.9,zorder=3)
    if label:ax.text(x+width*.5,y-.25,label,ha='center',fontsize=8,zorder=9)

def ribosome(ax,x,y,scale=.18,label=False):
    # Dos subunidades alrededor de un canal de ARN.
    ax.add_patch(Ellipse((x,y+.06),2*scale,1.25*scale,facecolor='#b8bd8c',edgecolor='#6f8467',lw=.7,zorder=8))
    ax.add_patch(Ellipse((x,y-.07),1.65*scale,.9*scale,facecolor='#8fa18a',edgecolor='#60765e',lw=.7,zorder=8))
    ax.plot([x-1.1*scale,x+1.1*scale],[y,y],color='#7b5b9b',lw=1.25,zorder=10)
    # Cadena naciente con eslabones de péptido, distinta de la hebra de ARN.
    for j in range(5):
        ax.add_patch(Ellipse((x+.05*np.sin(j),y+.16+j*.045),.045,.035,facecolor='#daae7b',edgecolor='#ab845f',lw=.35,zorder=9))
    if label:ax.text(x,y-.31,'ribosoma',ha='center',fontsize=6.5,zorder=11)
