"""Doce figuras científicas originales de cuatro paneles, edición 2.0."""
from pathlib import Path
import sys,json,string,os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import lectura_curvas
import ilustracion_molecular as art
from matplotlib.patches import PathPatch,FancyArrowPatch
from matplotlib.path import Path as MPath
from scipy.optimize import brentq
from scipy.signal import find_peaks
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists():ROOT=BASE
sys.path.insert(0,str(ROOT/'python'))
import circuitos_avanzados as av
OUT=ROOT/'docs'/'assets'/'figures';META=[]
colors=['#176d8b','#7c5ba1','#cc792c','#23816a']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.labelsize':9,'legend.fontsize':7,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7,'lines.linewidth':1.6,'savefig.facecolor':'white','svg.fonttype':'none','axes.prop_cycle':plt.cycler(color=colors)})
def grid():return plt.subplots(2,2,figsize=(7.2,5.1),layout='constrained')
def protein(ax,x,y,color,label,scale=.28):
    art.protein(ax,x,y,color,label,scale)

def arrow(ax,a,b,inhibit=False,rad=0,color='#56716b'):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-[' if inhibit else '-|>',mutation_scale=10,lw=1.2,color=color,connectionstyle=f'arc3,rad={rad}'))
def save(fig,slug,title,chapter,caption,tags,refs):
    if os.environ.get('ATLAS_FIGURA') and os.environ['ATLAS_FIGURA']!=slug:
        plt.close(fig);return
    for i,a in enumerate(fig.axes[:4]):
        a.text(-.12,1.10,string.ascii_uppercase[i],transform=a.transAxes,weight='bold',fontsize=12)
        a.tick_params(labelsize=8,width=.6)
    curves=lectura_curvas.extraer(fig,slug)
    fig.savefig(OUT/(slug+'.png'),dpi=240,bbox_inches='tight')
    fig.savefig(OUT/(slug+'.svg'),bbox_inches='tight')
    caption+=' Fuentes de principios: '+', '.join('['+x+']' for x in refs)+'. Parámetros y simulaciones originales, sin datos de artículos.'
    META.append({'id':slug,'title':title,'chapters':[chapter],'caption':caption,'alt':title+'. '+caption,'tags':tags,'refs':refs,'png':'assets/figures/'+slug+'.png','svg':'assets/figures/'+slug+'.svg','kind':'model','advanced':True,'curve_guide':curves,'source':'Figura científica generada desde código reproducible; ver tools/crear_figuras_avanzadas.py y python/circuitos_avanzados.py.'})
    plt.close(fig)

# G01: unión y dominio.
fig,axes=grid();a,b,c,d=axes.flat
a.axis('off');a.set(xlim=(0,4),ylim=(0,2),title='Especies y proceso reversible')
protein(a,.6,1,colors[0],'A');a.text(1.12,1,'+',ha='center',va='center');protein(a,1.6,1,colors[1],'B');protein(a,3.2,1,colors[3],'C',.38)
arrow(a,(2.05,1.12),(2.7,1.12));arrow(a,(2.7,.87),(2.05,.87))
a.text(2.35,1.4,'k₊ab',ha='center',fontsize=8);a.text(2.35,.57,'k₋c',ha='center',fontsize=8)
a.text(2,.16,'A total = a+c   ·   B total = b+c',ha='center',fontsize=8)
t=np.linspace(0,1.5,301);y=av.integrar(av.union,[0],t,method='Radau')[0];ce=av.union_equilibrio()
b.plot(t,y);b.axhline(ce,color=colors[2],ls='--');b.set(xlabel='Tiempo (h)',ylabel='Complejo (nM)',title='Convergencia a la raíz física')
x=np.linspace(0,16,400);c.plot(x,(10-x)*(8-x)-2*x);c.axhline(0,color='gray',lw=.7);c.axvspan(0,8,color=colors[3],alpha=.10,label='Dominio físico');c.plot([ce,10+np.sqrt(20)],[0,0],'o');c.set(xlabel='Complejo c (nM)',ylabel='dc/dt (nM/h)',title='Dos raíces; una admisible');c.legend(loc='upper center')
d.plot(t,10-y+y,label='a+c');d.plot(t,8-y+y,label='b+c');d.plot(t,y,'--',label='c');d.set(xlabel='Tiempo (h)',ylabel='Concentración (nM)',title='Conservaciones diferentes');d.legend()
save(fig,'g01_union','Unión: balances, dominio y conservación','reacciones','A: A+B⇌C. B–D: k₊=1 nM⁻¹h⁻¹, k₋=2 h⁻¹, totales 10 y 8 nM, c(0)=0. La raíz 14,47 nM viola los totales; la raíz 5,53 nM es física. La suma a+b+c no se utiliza como conservación.',['unión','conservación','raíz física','masa de acción'],['A01'])

# G02: bifurcaciones.
fig,axes=grid();a,b,c,d=axes.flat
pars=np.linspace(2,5,301);lo=(pars-np.sqrt(pars*pars-4))/2;hi=(pars+np.sqrt(pars*pars-4))/2
a.plot(pars,hi,label='Estable');a.plot(pars,lo,'--',label='Inestable');a.plot([0,5],[0,0],color=colors[3]);a.set(xlabel='Producción a',ylabel='Equilibrio x*',title='Silla-nodo en a=2');a.legend()
x=np.linspace(0,3.5,300)
for ap in [1.5,2.,2.5]:b.plot(x,ap*x*x/(1+x*x)-x,label=f'a={ap}')
b.axhline(0,color='gray',lw=.7);b.set(xlabel='Estado x',ylabel='dx/dτ',title='Ceros y signo del campo');b.legend()
t=np.linspace(0,20,301)
for x0 in [.4,.6]:c.plot(t,av.integrar(av.autoactivacion,[x0],t,args=(2.5,))[0],label=f'x₀={x0}')
c.set(xlabel='Tiempo adimensional',ylabel='Estado x',title='Una frontera entre destinos');c.legend()
pa=np.linspace(2.001,3,200);xx=(pa+np.sqrt(pa*pa-4))/2;rate=(xx*xx-1)/(1+xx*xx)
d.plot(pa,1/rate);d.set(xlabel='Producción a',ylabel='Tiempo local de relajación',title='Enlentecimiento junto al pliegue')
save(fig,'g02_bifurcacion','Ramas y estabilidad de una autoactivación','bifurcaciones','Modelo adimensional x′=a x²/(1+x²)−x, sin fuga. A: ramas continuas estables y discontinua inestable. B: campo para tres a. C: a=2,5. D: inversa de la magnitud de la pendiente en la rama alta. No representa una concentración negativa ni una calibración de promotor.',['bifurcación','silla-nodo','continuación','cuenca'],['A01','A02'])

# G03: Goodwin.
fig,axes=grid();a,b,c,d=axes.flat;a.axis('off');a.set(xlim=(0,4),ylim=(0,2),title='Tres etapas y represión final')
rna=np.linspace(.23,.87,100);a.plot(rna,.9+.055*np.sin(30*rna),color=colors[0],lw=2.4);a.text(.55,.58,'x · ARN',ha='center',fontsize=8)
for xx,col,label in [(1.95,colors[3],'y'),(3.35,colors[1],'z')]:protein(a,xx,.9,col,label)
arrow(a,(.9,.9),(1.6,.9));arrow(a,(2.3,.9),(3.,.9));arrow(a,(3.35,1.18),(.55,1.18),True,rad=.48)
a.text(2,.20,'Producción de x: a/(1+zⁿ)',ha='center',fontsize=9)
t=np.linspace(0,100,2001)
for ap in [4.,8.]:b.plot(t,av.integrar(av.goodwin,[.1,.5,.7],t,args=(ap,10))[0],label=f'a={ap}')
b.set(xlabel='Tiempo adimensional',ylabel='Estado x',title='Relajación y oscilación');b.legend()
pars=np.linspace(1,15,200);gain=[];real=[]
for ap in pars:
    s=brentq(lambda z:z*(1+z**10)-ap,0,ap)
    g=10*s**10/(1+s**10);gain.append(g);real.append(-1+.5*g**(1/3))
c.plot(pars,gain);c.axhline(8,color=colors[2],ls='--');c.set(xlabel='a',ylabel='Ganancia local g',title='El umbral simétrico es g=8')
d.plot(pars,real);d.axhline(0,color='gray',lw=.7);d.set(xlabel='a',ylabel='Parte real crítica',title='Pérdida de estabilidad local')
save(fig,'g03_goodwin','De la topología al candidato de Hopf','c14','x′=a/(1+z¹⁰)−x; y′=x−y; z′=y−z. A: flechas de etapas y barra represora. B: estado inicial (0,1;0,5;0,7). C–D: equilibrio simétrico y polinomio (λ+1)³+g. g=8 da a≈5,743; no es una condición universal de todo oscilador.',['Goodwin','Hopf','ganancia','oscilación'],['A01'])

# G04: antitético.
fig,axes=grid();a,b,c,d=axes.flat;a.axis('off');a.set(xlim=(0,4),ylim=(0,2),title='Control: actuar, medir y comparar')
protein(a,.55,1.1,colors[0],'Z₁');protein(a,2,1.1,colors[3],'Y');protein(a,3.4,1.1,colors[1],'Z₂')
arrow(a,(.9,1.1),(1.65,1.1));arrow(a,(2.35,1.1),(3.05,1.1));a.text(.55,1.6,'μ',ha='center');a.text(2.7,1.38,'θY',ha='center',fontsize=8)
a.text(2,.3,'Z₁ + Z₂ → retirados juntos',ha='center',fontsize=8)
for leak in [0.,.05]:
    t1=np.linspace(0,30,301);t2=np.linspace(30,90,601)
    v1=av.integrar(av.antitetico,[0,0,0],t1,args=(2,.5,1,1,1,leak),method='Radau')
    v2=av.integrar(av.antitetico,v1[:,-1],t2,args=(2,.5,1,2,1,leak),method='Radau')
    tt=np.r_[t1,t2[1:]];vv=np.c_[v1,v2[:,1:]];lab=f'δc={leak}/h'
    b.plot(tt,vv[0],label=lab);c.plot(tt,vv[1]-vv[2],label=lab);d.plot(tt,2-.5*vv[0]-leak*(vv[1]-vv[2]),label=lab)
b.axhline(4,color='gray',ls='--');b.axvline(30,color='gray',ls=':');b.set(xlabel='Tiempo (h)',ylabel='Salida Y (nM)',title='Perturbación de pérdida');b.legend()
c.set(xlabel='Tiempo (h)',ylabel='Z₁−Z₂ (nM)',title='Estado integrador firmado');c.legend()
d.set(xlabel='Tiempo (h)',ylabel='d(Z₁−Z₂)/dt (nM/h)',title='Identidad con o sin fuga');d.axhline(0,color='gray',lw=.7)
save(fig,'g04_control','Control integral y efecto de la dilución','control','μ=2 nM/h, θ=0,5 h⁻¹, k=1 h⁻¹, η=1 nM⁻¹h⁻¹; inicio nulo. La pérdida de Y cambia de 1 a 2 h⁻¹ en 30 h. Las curvas comparan ausencia de recambio de control y dilución δc=0,05 h⁻¹. Modelo abstracto idealizado, no reproducción de la implementación experimental.',['control','antitético','adaptación','dilución'],['A04','I09'])

# G05: fases.
fig,axes=grid();a,b,c,d=axes.flat;t=np.linspace(0,800,2401);w1,w2=2*np.pi/24,2*np.pi/26
for K in [.005,.015]:
    phi=av.integrar(av.fases,[0,.2],t,args=(w1,w2,K));psi=phi[1]-phi[0]
    a.plot(t,psi,label=f'K={K}/h');b.plot(t[-350:],np.sin(phi[0,-350:]),label=f'1, K={K}',alpha=.8)
    b.plot(t[-350:],np.sin(phi[1,-350:]),'--',label=f'2, K={K}',alpha=.8)
a.set(xlabel='Tiempo (h)',ylabel='Fase relativa (rad)',title='Deriva frente a bloqueo');a.legend()
b.set(xlabel='Tiempo (h)',ylabel='Salida sinusoidal (u.a.)',title='Fase no equivale a amplitud');b.legend(ncol=2,fontsize=6)
psi=np.linspace(-np.pi,np.pi,301)
c.plot(psi,(w2-w1)-.03*np.sin(psi));c.axhline(0,color='gray',lw=.7);c.set(xlabel='Fase relativa (rad)',ylabel='dψ/dt (rad/h)',title='Equilibrios de fase, K=0,015')
Ks=np.linspace(.001,.025,150);dw=np.linspace(0,.04,150)
d.contourf(Ks,dw,(dw[:,None]<=2*Ks[None,:]).astype(int),levels=[-.5,.5,1.5],colors=['#f4ddce','#b7d8c9']);d.plot(Ks,2*Ks,color=colors[0]);d.set(xlabel='K (1/h)',ylabel='|Δω| (1/h)',ylim=(0,.04),title='Verde: bloqueo posible')
save(fig,'g05_fases','Sincronización: frecuencias, fase y dominio de bloqueo','acoplados','Períodos libres 24 y 26 h; fases iniciales (0;0,2) rad. Modelo φᵢ′=ωᵢ+Ksin(φⱼ−φᵢ). La reducción supone amplitud relajada y acoplamiento apropiadamente débil. La frontera |Δω|=2K pertenece a la interacción sinusoidal simétrica.',['fase','sincronización','acoplamiento','frecuencia'],['A01','A05'])

# G06: ruido de promotor.
fig,axes=grid();a,b,c,d=axes.flat;t=np.linspace(0,20,1001);path=av.telegr_ssa(t,seed=7)
a.step(t,path[0],where='post');a.set(xlabel='Tiempo (h)',ylabel='Estado G',yticks=[0,1],title='Promotor OFF/ON')
b.step(t,path[1],where='post');b.set(xlabel='Tiempo (h)',ylabel='ARN (moléculas)',title='Una realización discreta')
factors=np.logspace(-1,2,100);fan=[]
for q in factors:m,v=av.momentos_telegr(q,q);fan.append(v/m)
c.semilogx(factors,fan);c.set(xlabel='kon=koff (1/h)',ylabel='Factor de Fano',title='Igual media; distinta variación')
samples=np.array([av.telegr_ssa([0.,80.],seed=j)[1,-1] for j in range(128)])
d.hist(samples,bins=np.arange(0,max(samples)+2)-.5,density=True,color=colors[1],alpha=.7);d.axvline(10,color='black',ls='--');d.set(xlabel='ARN (moléculas)',ylabel='Frecuencia relativa',title='128 estados finales independientes')
save(fig,'g06_rafagas','Ráfagas: estado, trayectoria y momentos','c21','kon=koff=1 h⁻¹, producción ON=20 moléculas/h y pérdida=1 por molécula y hora. A–B: semilla 7, estado inicial OFF y ARN cero. C: kon y koff varían juntos. D: semillas 0–127, observación a 80 h. Media analítica 10 y varianza 43,33 para los valores base; la muestra finita fluctúa.',['ráfagas','Gillespie','Fano','momento'],['A20','I02','A07'])

# G07: sensibilidad.
fig,axes=grid();a,b,c,d=axes.flat;t=np.linspace(.02,20,301);S=av.sensibilidad_lineal(t);x=av.primer_orden(t)
a.plot(t,8*S[0]/x,label='α');a.plot(t,.4*S[1]/x,label='δ');a.set(xlabel='Tiempo (h)',ylabel='Elasticidad',title='El tiempo cambia la información');a.legend()
b.plot(t,S[0],label='∂x/∂α (h)');b.plot(t,S[1],label='∂x/∂δ (nM·h)');b.set(xlabel='Tiempo (h)',ylabel='Sensibilidad dimensional',title='Las unidades son distintas');b.legend()
hs=np.logspace(-6,-1,25);errors=[]
for h in hs:
    fd=(av.primer_orden(t,8,.4+h)-av.primer_orden(t,8,.4-h))/(2*h)
    errors.append(max(np.abs(fd-S[1])))
c.loglog(hs,errors);c.set(xlabel='Paso en δ (1/h)',ylabel='Error máximo (nM·h)',title='Comprobar una derivada numérica')
sigmas=np.array([[.5**2,.5*.04*.95],[.5*.04*.95,.04**2]]);rng=np.random.default_rng(13);pars=rng.multivariate_normal([8,.4],sigmas,150)
d.scatter(pars[:,0],pars[:,1],s=6,alpha=.45);d.set(xlabel='α (nM/h)',ylabel='δ (1/h)',title='Incertidumbre conjunta correlacionada')
save(fig,'g07_sensibilidad','Derivadas de predicción e incertidumbre conjunta','sensibilidad','Balance x′=α−δx desde cero, α=8 nM/h y δ=0,4 h⁻¹. A–C usan derivadas analíticas. D es una nube sintética con desviaciones 0,5 y 0,04, correlación 0,95 y semilla 13; no es una posterior ajustada. La escala dimensional de cada derivada se indica en la leyenda.',['sensibilidad','elasticidad','derivada','correlación'],['A01','I06'])

# G08: sensor.
fig,axes=grid();a,b,c,d=axes.flat;t=np.linspace(0,30,301);S=av.integrar(av.sensor,[10],t)[0];der=1-.2*S;static=5*(10/S-1);dyn=(1-.1*S-der)/(.02*S)
a.plot(t,S);a.axhline(5,color='gray',ls='--');a.set(xlabel='Tiempo (min)',ylabel='Sensor S (nM)',title='La pérdida tiene transitorio')
b.plot(t,static,label='Calibración estática');b.plot(t,dyn,'--',label='Identidad dinámica');b.set(xlabel='Tiempo (min)',ylabel='Entrada (u.a.)',title='Misma señal, dos inferencias');b.legend()
rng=np.random.default_rng(18);noisy=S+rng.normal(0,.08,len(t));inv=(1-.1*noisy-np.gradient(noisy,t))/(.02*noisy)
c.plot(t,inv,lw=.6,alpha=.65,label='Derivada numérica ruidosa');c.axhline(5,color='black',ls='--');c.set(xlabel='Tiempo (min)',ylabel='Entrada estimada (u.a.)',title='Derivar amplifica ruido')
inputs=np.linspace(.1,10,100);ts=np.linspace(.1,20,100);eq=1/(.1+.02*inputs[:,None]);ss=eq+(10-eq)*np.exp(-(.1+.02*inputs[:,None])*ts[None,:]);err=5*(10/ss-1)-inputs[:,None]
im=d.pcolormesh(ts,inputs,err,shading='auto',cmap='RdBu_r',vmin=-10,vmax=10);d.set(xlabel='Tiempo (min)',ylabel='Entrada verdadera (u.a.)',title='Error de la inversión estática');fig.colorbar(im,ax=d,label='Error (u.a.)',shrink=.8)
save(fig,'g08_sensor','Degradación de sensor e inferencia de una entrada','c26','Producción 1 nM/min, pérdida basal 0,1 min⁻¹, k=0,02 min⁻¹ por unidad de entrada; S(0)=10 nM. A–C reciben entrada 5. C: error normal σ=0,08 nM, semilla 18 y diferencias numéricas. D: entrada y tiempo variables. Este no es un ajuste experimental de DII ni una calibración absoluta de auxina.',['auxina','sensor','calibración','inferencia'],['A01','P01','P02','I06'])

# G09: Turing.
fig,axes=grid();a,b,c,d=axes.flat;kk=np.linspace(0,1.2,301)
for D in [(1,1),(1,20)]:a.plot(kk,av.dispersion_turing(kk,D=D),label=str(D))
a.axhline(0,color='gray',lw=.7);a.set(xlabel='Número de onda k',ylabel='Tasa de crecimiento',title='Difusión igual o desigual');a.legend(title='(Du,Dv)')
ds=np.linspace(1,35,100);ks=np.linspace(0,1.2,100);rates=np.array([av.dispersion_turing(ks,D=(1,q)) for q in ds]);im=b.pcolormesh(ks,ds,rates,shading='auto',cmap='RdBu_r',vmin=-1,vmax=1);b.contour(ks,ds,rates,levels=[0],colors='black',linewidths=.6);b.set(xlabel='Número de onda k',ylabel='Dv/Du',title='Régimen lineal');fig.colorbar(im,ax=b,label='Tasa',shrink=.8)
space=np.linspace(0,10,101);time=np.linspace(0,20,101);k=np.pi/10;lam=av.dispersion_turing([k])[0];mode=1e-3*np.exp(lam*time[:,None])*np.cos(k*space[None,:]);im=c.pcolormesh(space,time,mode,shading='auto',cmap='RdBu_r');c.set(xlabel='Posición',ylabel='Tiempo',title='Modo en L=10: perturbación firmada');fig.colorbar(im,ax=c,shrink=.8)
d.plot(space,mode[0],label='Inicial');d.plot(space,mode[-1],label='Tiempo 20');d.set(xlabel='Posición',ylabel='Desviación de u',title='Crecimiento lineal, no patrón final');d.legend()
save(fig,'g09_turing','Estabilidad espacial y selección de modos','c18','Jacobiano J=[1,−2;2,−3], estable sin difusión. A–B analizan autovalores J−k²D. C–D muestran solo una perturbación lineal del modo cos(πx/10), compatible con flujo nulo. Las magnitudes son adimensionales; desviaciones negativas no son concentraciones negativas. No se simula saturación no lineal ni se identifica un patrón vegetal real.',['Turing','difusión','tejido','modos'],['A01','D11'])

# G10: fosforilación.
fig,axes=grid();a,b,c,d=axes.flat;a.axis('off');a.set(xlim=(0,4),ylim=(0,2),title='Tres estados de modificación')
for xx,cc,ll in [(.6,colors[0],'X₀'),(2,colors[3],'X₁'),(3.4,colors[1],'X₂')]:protein(a,xx,1,cc,ll)
for left,right in [(.95,1.65),(2.35,3.05)]:arrow(a,(left,1.12),(right,1.12));arrow(a,(right,.85),(left,.85))
a.text(2,1.55,'E: modifica  ·  F: revierte',ha='center',fontsize=8);a.text(2,.25,'Enzimas y complejos explícitos',ha='center',fontsize=8)
t=np.linspace(0,60,301);y0=np.array([10,0,0,2,1,0,0,0,0]);y=av.integrar(av.fosforilacion,y0,t,method='Radau')
for j,l in enumerate(['X₀ libre','X₁ libre','X₂ libre']):b.plot(t,y[j],label=l)
b.set(xlabel='Tiempo (u.a.)',ylabel='Cantidad (u.a.)',title='Conversión con enzimas compartidas');b.legend()
N,L=av.fosforilacion_red();tot=L@y
for j,l in enumerate(['E total','F total','X total']):c.plot(t,tot[j],label=l)
c.set(xlabel='Tiempo (u.a.)',ylabel='Cantidad total',title='Comprobar las conservaciones');c.legend()
ratio=np.linspace(.5,1.5,200)
for Km in [.01,.3]:
    vals=[brentq(lambda z:r*(1-z)/(Km+1-z)-z/(Km+z),0,1) for r in ratio]
    d.plot(ratio,vals,label=f'K₁=K₂={Km}')
d.set(xlabel='V₁/V₂',ylabel='Fracción activa',title='Ciclo simple: ultrasensibilidad');d.legend()
save(fig,'g10_fosforilacion','Modificación multisito y respuesta ultrasensible','cascadas','A–C: red abstracta distributiva de nueve especies, doce reacciones; on=1, off=cat=0,5 en unidades coherentes, totales (E,F,X)=(2,1,10). D es un modelo distinto: ciclo simple con total uno y V₂=1. La curva pronunciada de D no prueba bistabilidad y no debe confundirse con la red multisito.',['fosforilación','cascada','enzima','ultrasensibilidad'],['A01','A12','A13','A16'])

# G11: dos anillos.
fig,axes=grid();a,b,c,d=axes.flat;a.axis('off');a.set(xlim=(0,4.5),ylim=(0,3),title='Dos módulos y dos enlaces cruzados')
points=[(.6,2),(1.8,2.55),(1.8,1.45),(3,2),(4.15,2.55),(4.15,1.45)]
for j,(xx,yy) in enumerate(points):protein(a,xx,yy,colors[0] if j<3 else colors[1],('X' if j<3 else 'Y')+str(j%3+1),.23)
for ring in [(0,1,2),(3,4,5)]:
    for j in range(3):
        start=np.array(points[ring[j]]);end=np.array(points[ring[(j+1)%3]]);v=(end-start)/np.linalg.norm(end-start);arrow(a,tuple(start+.28*v),tuple(end-.28*v),True)
arrow(a,(.9,2.18),(2.7,2.18),True,.2,color=colors[2]);arrow(a,(2.7,1.82),(.9,1.82),True,.2,color=colors[2]);a.text(2.25,.5,'κ: represión cruzada adicional',ha='center',fontsize=8)
t=np.linspace(0,180,3601);six=av.integrar(av.anillos_acoplados,[.1,2,5,2,.1,5],t,args=(30,3,.1))
b.plot(t,six[0],label='X₁');b.plot(t,six[3],label='Y₁');b.set(xlabel='Tiempo adimensional',ylabel='Proteína (u.a.)',title='Dos señales dentro de seis estados');b.legend()
c.plot(six[0,-1200:],six[3,-1200:],lw=.9);c.set(xlabel='X₁ (u.a.)',ylabel='Y₁ (u.a.)',title='Proyección tras el transitorio')
tail=six[:,t>120];im=d.imshow(tail,aspect='auto',origin='lower',extent=[120,180,-.5,5.5],cmap='viridis');d.set(xlabel='Tiempo adimensional',yticks=range(6),yticklabels=['X₁','X₂','X₃','Y₁','Y₂','Y₃'],title='El estado completo importa');fig.colorbar(im,ax=d,label='Abundancia (u.a.)',shrink=.8)
save(fig,'g11_seis_genes','Circuito compuesto de seis proteínas reguladoras','acoplados','Dos anillos con a=30, n=3 y κ=0,1; estado inicial (0,1;2;5;2;0,1;5). La represión adicional entra en el denominador de producción de X₁ y Y₁. Se muestran todas las especies para evitar clasificar la red solo por una proyección. Este ejemplo no se etiqueta como caos ni reproduce una parametrización publicada.',['seis genes','circuito complejo','módulos','acoplamiento'],['A01','A06'])

# G12: perfiles.
fig,axes=grid();a,b,c,d=axes.flat;alphas=np.linspace(3,16,100);rng=np.random.default_rng(26)
for tt,label in [(np.linspace(0,15,25),'Transitorio'),(np.linspace(40,55,25),'Tardío')]:
    data=av.primer_orden(tt)+rng.normal(0,1,len(tt));obj,dd=av.perfiles_lineales(tt,data,1,alphas)
    a.plot(alphas,obj-obj.min(),label=label);b.plot(alphas,dd,label=label)
a.set(xlabel='α fijada (nM/h)',ylabel='Δχ²',ylim=(0,30),title='Perfil con δ reoptimizada');a.legend()
b.plot(alphas,alphas/20,'k--',label='α/δ=20');b.set(xlabel='α fijada (nM/h)',ylabel='δ ajustada (1/h)',title='Compensación de parámetros');b.legend()
t=np.linspace(0,20,301)
for aa,dd in [(4,.2),(8,.4),(16,.8)]:c.plot(t,av.primer_orden(t,aa,dd),label=f'α={aa}, δ={dd}')
c.set(xlabel='Tiempo (h)',ylabel='Estado (nM)',title='Igual equilibrio; otro transitorio');c.legend()
aa=np.linspace(3,16,120);dd=np.linspace(.1,.9,120);error=(aa[None,:]/dd[:,None]-20)**2;im=d.pcolormesh(aa,dd,np.log10(1+error),shading='auto',cmap='viridis_r');d.plot(aa,aa/20,'w--');d.set(xlabel='α (nM/h)',ylabel='δ (1/h)',title='Error al observar solo equilibrio');fig.colorbar(im,ax=d,label='log₁₀(1+error²)',shrink=.8)
save(fig,'g12_perfiles','Diseño temporal e identificabilidad práctica','c24','Datos sintéticos de α=8 nM/h, δ=0,4 h⁻¹ y x₀=0; errores normales σ=1 nM, semilla 26. A–B reoptimizan δ para cada α. C–D son cálculos analíticos sin ruido. Un perfil ancho no se corrige congelando el parámetro compensador.',['perfil','identificabilidad','ajuste','diseño'],['I06','A09','A10'])

p=ROOT/'docs'/'figures.json';existing=json.loads(p.read_text(encoding='utf8'))
replacement={f['id']:f for f in META};known={f['id'] for f in existing}
result=[replacement.get(f['id'],f) for f in existing]+[f for f in META if f['id'] not in known]
p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print('Figuras nuevas:',len(META),'Total:',len(result))
