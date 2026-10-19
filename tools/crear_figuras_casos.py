"""Figuras reproducibles para explicar construcción y verificación del código."""
from pathlib import Path
import json,sys,string
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import lectura_curvas
import ilustracion_molecular as art
from matplotlib.patches import PathPatch,FancyArrowPatch
from matplotlib.path import Path as PlotPath
from scipy.integrate import solve_ivp
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists():ROOT=BASE
sys.path.insert(0,str(ROOT/'python'))
import circuitos_casos as cc
OUT=ROOT/'docs'/'assets'/'figures';META=[]
colors=['#176d8b','#7c5ba1','#cc792c','#23816a']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.labelsize':9,'legend.fontsize':7,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7,'lines.linewidth':1.5,'savefig.facecolor':'white','svg.fonttype':'none','axes.prop_cycle':plt.cycler(color=colors)})
def grid():return plt.subplots(2,2,figsize=(7.5,5.4),layout='constrained')
def protein(ax,x,y,color,label,scale=.28):
    art.protein(ax,x,y,color,label,scale)

def arrow(ax,a,b,inhibit=False,rad=0,color='#56716b'):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-[' if inhibit else '-|>',mutation_scale=8,lw=1.1,color=color,connectionstyle=f'arc3,rad={rad}'))
def save(fig,slug,title,chapter,caption,tags,refs):
    for i,ax in enumerate(fig.axes[:4]):ax.text(-.13,1.10,string.ascii_uppercase[i],transform=ax.transAxes,fontsize=12,weight='bold')
    curves=lectura_curvas.extraer(fig,slug)
    for ext in ['png','svg']:fig.savefig(OUT/(slug+'.'+ext),dpi=240,bbox_inches='tight')
    caption+=' Fuentes de principios: '+', '.join('['+r+']' for r in refs)+'. Desarrollo y simulaciones docentes originales; no son datos ni parámetros ajustados de los artículos.'
    META.append(dict(id=slug,title=title,chapters=[chapter],caption=caption,alt=title+'. '+caption,tags=tags,refs=refs,png='assets/figures/'+slug+'.png',svg='assets/figures/'+slug+'.svg',kind='model',advanced=True,curve_guide=curves,source='Generada con tools/crear_figuras_casos.py y python/circuitos_casos.py.'))
    plt.close(fig)

fig,axes=grid();a,b,c,d=axes.flat
a.axis('off');a.set(xlim=(0,4.1),ylim=(0,3.1),title='Cada gen necesita ARN y proteína')
for i,y in enumerate([2.5,1.55,.6]):
    color=colors[i]
    art.dna(a,.1,y,f'gen {i}',width=.8)
    art.rna(a,1.3,y,f'm{i}',width=.7)
    art.ribosome(a,2.45,y,scale=.12)
    protein(a,3.05,y,color,f'p{i}')
    arrow(a,(.92,y),(1.2,y));arrow(a,(2.1,y),(2.75,y))
    a.text(2.1,y+.30,f'p{[2,0,1][i]} ⊣ gen {i}',ha='center',fontsize=7)
tau=np.linspace(0,180,1801);initial=np.array([.1,.2,.3,1,2,3.])
sol=solve_ivp(cc.represilador,(0,180),initial,t_eval=tau,rtol=1e-10,atol=1e-12)
assert sol.success
for i in range(3):b.plot(tau,sol.y[3+i],label=f'p{i}')
b.set(xlabel='Tiempo normalizado τ',ylabel='Proteína / K',title='Tres señales, seis balances');b.legend(ncol=3)
dim=solve_ivp(cc.represilador_dimensional,(0,360),cc.a_dimensional(initial),t_eval=tau/.5,rtol=1e-10,atol=1e-12)
assert dim.success
c.plot(tau,sol.y[3],label='Versión normalizada');c.plot(tau,cc.a_normalizado(dim.y)[3],'--',label='Dimensional convertida')
c.set(xlabel='τ = γm t',ylabel='p0 = P0 / K',title='Mismo mecanismo, otras unidades');c.legend()
s=cc.equilibrio_represilador();J=cc.jacobiano_represilador(np.full(6,s))
im=d.imshow(J,cmap='RdBu_r',vmin=-2,vmax=2);d.set(xticks=range(6),yticks=range(6),xticklabels=['m0','m1','m2','p0','p1','p2'],yticklabels=['m0′','m1′','m2′','p0′','p1′','p2′'],title='Cada columna mueve un estado')
fig.colorbar(im,ax=d,shrink=.8,label='Derivada de una tasa')
save(fig,'h01_bacteria','Del represilador a seis EDO y un programa verificable','caso-bacteriano','α=60, α₀=0,01, β=0,2, n=2; inicio normalizado (0,1;0,2;0,3;1;2;3). Equivalente dimensional: γm=0,5/h, γp=0,1/h, K=10 nM, kt=2/h, sv=15 nM/h, sb=0,0025 nM/h. A distingue ARN y proteína; B muestra proteínas; C convierte escalas; D es el Jacobiano en el equilibrio simétrico.',['bacterias','E. coli','represilador','seis EDO','normalización','Jacobiano'],['A01','D02','A27'])

fig,axes=grid();a,b,c,d=axes.flat
x=np.linspace(0,3.5,501)
a.plot(x,.02+3*x*x/(1+x*x),label='Producción');a.plot(x,x,label='Pérdida')
roots=cc.raices_autoactivacion();a.plot(roots,roots,'o',ms=4,color=colors[3])
a.set(xlabel='Activador normalizado x',ylabel='Tasa normalizada',title='Tres intersecciones, dos destinos');a.legend()
t=np.linspace(0,25,501)
for x0 in [.1,.8]:
    ss=solve_ivp(cc.autoactivacion,(0,25),[x0],t_eval=t,rtol=1e-10,atol=1e-12)
    b.plot(t,ss.y[0],label=f'x₀={x0}')
b.set(xlabel='Tiempo normalizado',ylabel='Activador x',title='El estado inicial elige la cuenca');b.legend()
t=np.linspace(0,20,401);exact=cc.adaptacion_exacta(t)
c.plot(t,exact[0],label='Desviación h');c.plot(t,exact[1],label='Compensación g')
c.axhline(0,color='gray',lw=.6);c.set(xlabel='Tiempo docente',ylabel='Estado normalizado',title='Otro mecanismo: adaptación');c.legend()
for fuga in [0,.1,.3]:
    ss=solve_ivp(cc.adaptacion,(0,20),[0,0],t_eval=t,args=(1,1,1,1,fuga),rtol=1e-10,atol=1e-12)
    d.plot(t,ss.y[0],label=f'Fuga={fuga}')
d.set(xlabel='Tiempo docente',ylabel='Desviación h',title='Perder memoria deja error');d.legend()
save(fig,'h02_levadura','Levadura como ejemplo: memoria de estado y adaptación','caso-levadura','A–B: autoactivación x′=0,02+3x²/(1+x²)−x. C–D son otro modelo: h′=(1−g)−h, g′=h−fuga·g, inicio cero, entrada uno. h es una desviación que puede cambiar de signo; no una concentración de Hog1. Las redes publicadas motivan las preguntas, sin identificar estas simulaciones con sus datos.',['levadura','autoactivación','adaptación','Hog1','integral','bistabilidad'],['A01','A25','A26'])

fig,axes=grid();a,b,c,d=axes.flat
t=np.linspace(0,20,101);y=cc.primer_orden(t)
a.plot(t,y);a.axhline(40,ls='--',color=colors[1]);a.set(xlabel='Tiempo (h)',ylabel='x (nM)',title='Balance con solución conocida')
steps=np.array([.05,.1,.2,.4,.8]);errors=[]
for step in steps:
    tt=np.arange(0,20+step/2,step);xx=np.empty(tt.size);xx[0]=5
    for i in range(tt.size-1):xx[i+1]=xx[i]+step*(12-.3*xx[i])
    errors.append(np.max(np.abs(xx-cc.primer_orden(tt))))
b.loglog(steps,errors,'o-');b.set(xlabel='Paso Euler h (h)',ylabel='Error máximo (nM)',title='Menor paso, menor discrepancia')
JJ=np.array([[-.5,0],[2,-.2]])
im=c.imshow(JJ,cmap='RdBu_r',vmin=-2,vmax=2);c.set(xticks=[0,1],yticks=[0,1],xticklabels=['m','p'],yticklabels=['m′','p′'],title='Derivar cada salida por entrada')
for i in range(2):
    for j in range(2):c.text(j,i,f'{JJ[i,j]:g}',ha='center',va='center',color='white' if abs(JJ[i,j])>1 else '#17373d')
fig.colorbar(im,ax=c,shrink=.8,label='Derivada parcial')
hh=np.logspace(-8,-1,80);err=[]
z=np.array([.1,.3,.5,1,2,4.])
for step in hh:err.append(np.max(np.abs(cc.diferencia_central(lambda zz:cc.represilador(0,zz),z,step)-cc.jacobiano_represilador(z))))
d.loglog(hh,err);d.set(xlabel='Paso de perturbación (adim.)',ylabel='Error máximo de derivadas',title='Demasiado pequeño también falla')
save(fig,'h03_codigo','Aprender a comprobar ecuaciones y líneas de programa','c08','A–B: x′=12−0,3x, x(0)=5 nM; Euler usa los pasos indicados, frente a la solución analítica. C corresponde a otro modelo de ARN y proteína, J=[[-0,5;0],[2;−0,2]]. D compara Jacobiano analítico del represilador con diferencias centrales en (0,1;0,3;0,5;1;2;4); el redondeo limita pasos diminutos.',['código','Euler','error','Jacobiano','derivada parcial','Python'],['A01','A17','A27','R05'])

p=ROOT/'docs'/'figures.json';old=json.loads(p.read_text(encoding='utf8'))
replacement={f['id']:f for f in META};known={f['id'] for f in old}
result=[replacement.get(f['id'],f) for f in old]+[f for f in META if f['id'] not in known]
p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print('Figuras explicativas:',len(META),'Total:',len(result))
