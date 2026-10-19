"""Dieciséis secuencias gráficas: reacción, paso matemático y consecuencia."""
from pathlib import Path
import sys,json,string
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import lectura_curvas
from matplotlib.patches import FancyArrowPatch,PathPatch,FancyBboxPatch
from matplotlib.path import Path as PlotPath
from scipy.integrate import solve_ivp
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists():ROOT=BASE
sys.path.insert(0,str(ROOT/'python'))
import circuitos_casos as cc
import ilustracion_molecular as art
OUT=ROOT/'docs'/'assets'/'figures';META=[]
C=['#176d8b','#7c5ba1','#d17d32','#23816a']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.labelsize':9,'legend.fontsize':7,'axes.spines.top':False,'axes.spines.right':False,'lines.linewidth':1.6,'svg.fonttype':'none','axes.prop_cycle':plt.cycler(color=C)})
def grid():return plt.subplots(2,2,figsize=(7.6,5.45),layout='constrained')
def protein(ax,x,y,label,color=C[0],scale=.25):
    art.protein(ax,x,y,color,label,scale)
def arrow(ax,a,b,label='',bar=False,rad=0,color='#54716c'):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-[' if bar else '-|>',mutation_scale=9,lw=1.2,color=color,connectionstyle=f'arc3,rad={rad}'))
    if label:
        vertical=abs(b[1]-a[1])>abs(b[0]-a[0])
        ax.text((a[0]+b[0])/2+(.18 if vertical else 0),(a[1]+b[1])/2+(0 if vertical else .15),label,ha='left' if vertical else 'center',fontsize=8)
def dna(ax,x,y,label):art.dna(ax,x,y,label)
def rna(ax,x,y,label):art.rna(ax,x,y,label)
def pieces(ax,x,y):
    ax.plot([x-.13,x],[y-.05,y+.07],color='#83958f',lw=1.3)
    ax.plot([x+.12,x+.19],[y+.08,y-.08],color='#83958f',lw=1.3)
    ax.plot([x-.06,x+.05],[y-.16,y-.13],color='#83958f',lw=1.3)
def molecular(ax,kind='linear'):
    ax._atlas_kind=kind
    ax.axis('off');ax.set(xlim=(0,4.2),ylim=(0,2.9),title='A · Qué representa el balance')
    if kind in ['linear','gene','hill','auto']:
        dna(ax,.1,1.5,'ADN / promotor');rna(ax,1.65,1.5,'ARN');protein(ax,3.1,1.5,'P')
        arrow(ax,(1.12,1.5),(1.52,1.5));arrow(ax,(2.4,1.5),(2.8,1.5))
        art.ribosome(ax,2.48,1.5,scale=.13,label=True)
        arrow(ax,(3.1,1.15),(3.1,.55),'δP');pieces(ax,3.1,.32)
        if kind=='hill':
            protein(ax,.58,2.45,'R',C[2]);arrow(ax,(.58,2.2),(.58,1.7),'represión',bar=True)
        elif kind=='auto':arrow(ax,(3.1,1.8),(.5,1.8),'autoactivación',rad=.52,color=C[2])
        else:ax.text(2.1,2.4,'Producción y pérdida se cuentan por separado',ha='center',fontsize=8)
    elif kind=='binding':
        protein(ax,.45,1.6,'A');ax.text(.92,1.6,'+',ha='center',va='center');protein(ax,1.35,1.6,'B',C[1]);protein(ax,3.25,1.6,'AB',C[3],.36)
        arrow(ax,(1.8,1.75),(2.8,1.75),'k₊ab');arrow(ax,(2.8,1.4),(1.8,1.4),'k₋c')
        ax.text(2.1,.6,'A libre + AB = A total\nB libre + AB = B total',ha='center',fontsize=9)
    elif kind=='toggle':
        dna(ax,.2,1.05,'gen X');dna(ax,2.7,1.05,'gen Y');protein(ax,.7,2.12,'X');protein(ax,3.2,2.12,'Y',C[1])
        arrow(ax,(.7,1.3),(.7,1.9));arrow(ax,(3.2,1.3),(3.2,1.9))
        arrow(ax,(1,2.1),(3.2,1.35),bar=True,rad=-.12,color=C[0]);arrow(ax,(2.9,2.1),(.7,1.35),bar=True,rad=.12,color=C[1])
    elif kind=='control':
        protein(ax,.5,1.7,'Z₁');protein(ax,1.8,1.7,'Z₂',C[1]);protein(ax,3.25,1.7,'Y',C[3])
        ax.text(1.15,1.7,'+',ha='center',va='center');arrow(ax,(1.15,1.35),(1.15,.65),'retirada conjunta');pieces(ax,1.15,.4)
        arrow(ax,(.55,2),(3.2,2),'actuación',rad=-.22);arrow(ax,(3.25,1.4),(1.95,1.4),'medición',rad=-.28)
        ax.text(.45,2.58,'entrada μ',fontsize=8);ax.text(2.9,.5,'salida y',fontsize=8)
    elif kind=='telegraph':
        dna(ax,.15,2,'OFF');dna(ax,2.75,2,'ON');arrow(ax,(1.25,2.15),(2.55,2.15),'k_on');arrow(ax,(2.55,1.7),(1.25,1.7),'k_off')
        rna(ax,3,1.05,'M');arrow(ax,(3.3,1.6),(3.3,1.25),'r');arrow(ax,(2.9,.85),(2.1,.6),'γM');pieces(ax,1.9,.5)
    elif kind=='observation':
        rna(ax,.1,1.7,'ARN');protein(ax,1.55,1.7,'Pi','#95a79f');protein(ax,3.15,1.7,'Pf',C[3]);arrow(ax,(.85,1.7),(1.22,1.7));arrow(ax,(1.9,1.7),(2.8,1.7),'maduración')
        ax.text(3.15,2.4,'✦ luz',ha='center',color=C[3],fontsize=11);ax.text(2.1,.5,'Medida = fondo + escala × Pf + error',ha='center',fontsize=8)
    elif kind=='diffusion':
        for x,label in [(.2,'célula 1'),(2.45,'célula 2')]:
            ax.add_patch(FancyBboxPatch((x,.7),1.45,1.45,boxstyle='round,pad=.08,rounding_size=.18',facecolor='#edf3e8',edgecolor='#698c6e',lw=1.4));ax.text(x+.7,.38,label,ha='center',fontsize=9)
        protein(ax,.85,1.45,'X');protein(ax,3.2,1.45,'X',C[1]);arrow(ax,(1.5,1.7),(2.5,1.7),'q(x₁−x₂)');arrow(ax,(2.5,1.1),(1.5,1.1))
    elif kind=='enzyme':
        protein(ax,.42,1.65,'E');protein(ax,1.32,1.65,'S',C[2],.17);ax.text(.87,1.65,'+',ha='center',va='center');protein(ax,2.55,1.65,'ES',C[1],.35)
        arrow(ax,(1.65,1.85),(2.12,1.85));arrow(ax,(2.12,1.4),(1.65,1.4));arrow(ax,(2.95,1.65),(3.8,1.65),'kcat')
        ax.text(3.75,1.2,'E + P',ha='center',fontsize=9);ax.text(2.1,.5,'E total = E libre + ES',ha='center',fontsize=9)
    elif kind=='feedforward':
        protein(ax,.5,1.65,'U');protein(ax,2.1,2.3,'Y',C[1]);protein(ax,3.65,1.65,'Z',C[3])
        arrow(ax,(.8,1.7),(3.3,1.7),'vía rápida');arrow(ax,(.7,1.9),(1.8,2.3));arrow(ax,(2.4,2.3),(3.5,1.95),'vía lenta',bar=True)
        ax.text(2.1,.5,'Una entrada actúa por dos caminos opuestos',ha='center',fontsize=8)
    elif kind=='sensor':
        protein(ax,.6,1.8,'A',C[2],.18);protein(ax,1.9,1.8,'sensor',C[3],.36);arrow(ax,(.9,1.8),(1.5,1.8),'entrada')
        arrow(ax,(2.35,1.8),(3.5,1.8),'retirada');pieces(ax,3.7,1.8)
        ax.text(2.1,.65,'Más entrada → mayor pérdida del sensor',ha='center',fontsize=9)
def formulas(ax,lines,title='B · De dónde sale la relación'):
    ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1),title=title)
    for i,(heading,math) in enumerate(lines):
        y=.86-i*.28;ax.text(.03,y,heading,color='#30675c',fontsize=9,weight='bold');ax.text(.04,y-.14,math,fontsize=11)
def integrate(fun,initial,t,args=()):
    sol=solve_ivp(fun,(t[0],t[-1]),initial,t_eval=t,args=args,rtol=1e-9,atol=1e-11)
    assert sol.success,sol.message
    return sol.y
def save(fig,key,title,chapter,hint,caption,refs,tags):
    # Los rótulos A/B se incluyen en los títulos para mantener sitio a los esquemas.
    for i,ax in enumerate(fig.axes[:4]):
        if i>=2:ax.set_title(string.ascii_uppercase[i]+' · '+ax.get_title())
    curves=lectura_curvas.extraer(fig,key)
    for ext in ['png','svg']:fig.savefig(OUT/(key+'.'+ext),dpi=240,bbox_inches='tight')
    if getattr(fig.axes[0],'_atlas_kind',None)=='linear':caption+=' El ARN del esquema indica una plantilla de producción resumida; no se añade como estado al balance de una variable.'
    caption+=' Esquemas moleculares conceptuales, sin escala estructural. Parámetros y simulaciones docentes originales. Fuentes: '+' '.join('['+r+']' for r in refs)+'.'
    META.append(dict(id=key,title=title,chapters=[chapter],after_heading=hint,caption=caption,alt=title+'. '+caption,refs=refs,tags=tags,kind='model',advanced=True,curve_guide=curves,png='assets/figures/'+key+'.png',svg='assets/figures/'+key+'.svg',source='Figura original reproducible: tools/crear_figuras_pasos.py. Cada panel conecta mecanismo, ecuación y predicción.'))
    plt.close(fig)

# 1: EDO, desplazamiento al equilibrio.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a)
formulas(b,[('Balance de tasas',r'$x\prime=\alpha-\delta x$'),('El equilibrio cancela entradas y salidas',r'$x^*=\alpha/\delta$'),('La distancia al equilibrio se relaja',r'$z=x-x^*,\quad z\prime=-\delta z$')])
t=np.linspace(0,15,301)
for x0 in [5,40,70]:c.plot(t,cc.primer_orden(t,x0=x0),label=f'x₀={x0} nM')
c.set(xlabel='Tiempo (h)',ylabel='Concentración (nM)',title='El mismo destino, otros inicios');c.legend()
xx=np.linspace(0,80,201);d.plot(xx,np.full_like(xx,12),label='Producción α');d.plot(xx,.3*xx,label='Pérdida δx');d.axvline(40,color='gray',ls=':');d.set(xlabel='x (nM)',ylabel='Tasa (nM/h)',title='La intersección fija x*');d.legend()
save(fig,'q01_balance','Ver cada término del balance y su solución','edo','Integrar sin esconder','α=12 nM/h y δ=0,3/h. C muestra tres condiciones iniciales; D compara las dos tasas, no dos estados. z puede ser negativa porque es una diferencia respecto a 40 nM.',['A01','A02'],['EDO','balance','equilibrio','producción','pérdida'])

# 2: ARN y proteína.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'gene')
formulas(b,[('La primera etapa crea plantilla',r'$m\prime=s-\gamma_m m$'),('La segunda utiliza esa plantilla',r'$p\prime=k_t m-\gamma_p p$'),('Desde cero, la proteína arranca curvada',r'$p(t)\approx k_t s t^2/2$')])
t=np.linspace(0,30,601);y=integrate(lambda t,z:[4-.5*z[0],2*z[0]-.2*z[1]],[0,0],t)
c.plot(t,y[0],label='ARN m');c.plot(t,y[1],label='Proteína p');c.set(xlabel='Tiempo (h)',ylabel='Concentración (nM)',title='Dos escalas que se conectan');c.legend()
early=np.linspace(0,.8,201);ye=integrate(lambda t,z:[4-.5*z[0],2*z[0]-.2*z[1]],[0,0],early)
d.plot(early,ye[1],label='Dos balances');d.plot(early,4*early**2,'--',label='Aproximación inicial');d.set(xlabel='Tiempo (h)',ylabel='Proteína (nM)',title='La pendiente inicial es cero');d.legend()
save(fig,'q02_dos_etapas','Del ADN a dos balances y al arranque de proteína','c09','Resolver en el orden','s=4 nM/h, γm=0,5/h, kt=2/h, γp=0,2/h; estados iniciales cero. La curva t² es una aproximación de tiempos pequeños, no una solución para todo el registro.',['A01','A02'],['ARN','proteína','traducción','dos etapas','curvatura'])

# 3: ocupación de un promotor.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'hill')
formulas(b,[('La unión redistribuye promotores',r'$D+R\rightleftharpoons DR$'),('Fracción libre de un sitio en equilibrio',r'$f_D=1/(1+R/K_d)$'),('Actividad ponderada de los dos estados',r'$s=s_b+(s_f-s_b)f_D$')])
r=np.linspace(0,50,301);c.plot(r,1/(1+r/10),label='Libre');c.plot(r,1-1/(1+r/10),label='Ocupado');c.set(xlabel='Represor R (nM)',ylabel='Fracción de promotores',title='Las dos fracciones suman uno');c.legend()
for n in [1,2,4]:d.plot(r,1+9/(1+(r/10)**n),label=f'n={n}')
d.set(xlabel='Represor R (nM)',ylabel='Producción de ARN (nM/h)',title='Pendiente y umbral son distintos');d.legend()
save(fig,'q03_promotor','De ocupación molecular a producción regulada','c16','Del promotor ocupado','C usa Kd=10 nM y unión de un sitio; D compara leyes de Hill efectivas con K=10 nM, sb=1 y sf=10 nM/h. La generalización de D no identifica por sí sola un número de sitios moleculares.',['A01','D07'],['promotor','Hill','ocupación','represor','fracción'])

# 4: Jacobiano y perturbaciones.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'gene')
formulas(b,[('Cada tasa es una salida diferente',r'$f_1=4-0.5m,\quad f_2=2m-0.2p$'),('Perturbar solo m afecta a ambas',r'$\partial_m f_1=-0.5,\quad\partial_m f_2=2$'),('Perturbar solo p afecta a la segunda',r'$\partial_p f_1=0,\quad\partial_p f_2=-0.2$')])
J=np.array([[-.5,0],[2,-.2]]);im=c.imshow(J,cmap='RdBu_r',vmin=-2,vmax=2);c.set(xticks=[0,1],yticks=[0,1],xticklabels=['m','p'],yticklabels=['m′','p′'],title='Columnas: entrada que se mueve')
for i in range(2):
    for j in range(2):c.text(j,i,str(J[i,j]),ha='center',va='center',color='white' if abs(J[i,j])>1 else '#183c3d')
fig.colorbar(im,ax=c,shrink=.8)
t=np.linspace(0,15,301);y=integrate(lambda t,z:J@z,[1,0],t);d.plot(t,y[0],label='εm');d.plot(t,y[1],label='εp');d.axhline(0,color='gray',lw=.6);d.set(xlabel='Tiempo (h)',ylabel='Perturbación (nM)',title='Una perturbación puede transmitirse');d.legend()
save(fig,'q04_jacobiano','De una reacción a las cuatro entradas del Jacobiano','c11','De dónde viene la ecuación de autovalores','Modelo lineal de dos etapas con s=4 nM/h y constantes indicadas en B. D integra desviaciones del equilibrio desde (1,0), no concentraciones absolutas.',['A01','A27'],['Jacobiano','derivada parcial','perturbación','autovalor'])

# 5: doble represión.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'toggle')
formulas(b,[('Cada proteína reduce la producción de la otra',r'$x\prime=3/(1+y^2)-x$'),('Segunda nulclina',r'$y\prime=3/(1+x^2)-y$'),('En puntos asimétricos, restar da',r'$(x-y)(1-xy)=0$')])
x=np.linspace(.01,3.3,301);c.plot(x,3/(1+x*x),label='y′=0');c.plot(3/(1+x*x),x,label='x′=0');c.set(xlabel='x',ylabel='y',title='Las intersecciones son equilibrios');c.legend()
t=np.linspace(0,20,301)
for initial in [[.5,2],[2,.5]]:
    yy=integrate(lambda t,z:[3/(1+z[1]**2)-z[0],3/(1+z[0]**2)-z[1]],initial,t)
    d.plot(t,yy[0],label=f'x desde {initial}')
d.set(xlabel='Tiempo normalizado',ylabel='Represor x',title='Dos inicios, dos destinos');d.legend()
save(fig,'q05_interruptor','Cómo la doble represión construye dos destinos','c13','Un ejemplo con tres equilibrios','a=3, n=2, pérdidas normalizadas a uno y fuga cero. Las curvas de C son nulclinas, no trayectorias temporales; D integra dos condiciones iniciales del mismo circuito.',['A01','D01'],['interruptor','nulclina','bistabilidad','represión cruzada'])

# 6: autoactivación y pliegue.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'auto')
formulas(b,[('La producción se refuerza y satura',r'$x\prime=a x^2/(1+x^2)-x$'),('Equilibrio no nulo',r'$x^2-a x+1=0$'),('Las dos raíces se encuentran cuando',r'$a^2-4=0$')])
x=np.linspace(0,3.5,301)
for aa in [1.5,2,2.5]:c.plot(x,aa*x*x/(1+x*x)-x,label=f'a={aa}')
c.axhline(0,color='gray',lw=.6);c.set(xlabel='x',ylabel='x′',title='Los ceros cambian al mover a');c.legend()
aa=np.linspace(2,5,301);d.plot(aa,(aa+np.sqrt(aa*aa-4))/2,label='Estable');d.plot(aa,(aa-np.sqrt(aa*aa-4))/2,'--',label='Inestable');d.plot([0,5],[0,0],color=C[3]);d.set(xlabel='Capacidad a',ylabel='Equilibrio x*',title='Parámetro y tiempo no son el mismo eje');d.legend()
save(fig,'q06_pliegue','De la autoactivación a un pliegue de equilibrios','bifurcaciones','Identificar la estabilidad','Todos los valores son adimensionales, con fuga cero. C muestra campos de velocidad para tres parámetros; D reúne raíces estacionarias, no el historial temporal de una célula.',['A01','A02'],['autoactivación','bifurcación','pliegue','discriminante'])

# 7: resta de controladores.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'control')
formulas(b,[('Se retiran juntos en los dos balances',r'$z_1\prime=\mu-\eta z_1z_2$'),('La salida produce la segunda especie',r'$z_2\prime=\theta y-\eta z_1z_2$'),('Restar cancela el flujo compartido',r'$(z_1-z_2)\prime=\mu-\theta y$')])
t=np.linspace(0,30,601)
def ctl(t,z):
    y,z1,z2=z;return [z1-y,2-z1*z2,.5*y-z1*z2]
y=integrate(ctl,[0,0,0],t);c.plot(t,y[0],label='Salida');c.axhline(4,ls='--',color=C[1],label='μ/θ');c.set(xlabel='Tiempo (h)',ylabel='y (nM)',title='El equilibrio fija una referencia');c.legend()
w=y[1]-y[2];identity=2-.5*y[0];d.plot(t,identity,label='Error escalado μ−θy');d.plot(t,np.gradient(w,t),'--',label='Derivada numérica de z₁−z₂');d.set(xlabel='Tiempo (h)',ylabel='Tasa (nM/h)',title='Una identidad que se puede comprobar');d.legend()
save(fig,'q07_integral','Ver la cancelación que produce control integral','control','Restar antes','μ=2 nM/h, θ=0,5/h, η=1/(nM·h), producción de salida z1/h y pérdida y/h. Sin fuga ni saturación, inicio cero. La derivada numérica de D es una comprobación aproximada sobre la malla.',['A01','A04'],['integral','antitético','secuestro','resta','adaptación'])

# 8: tiempo de espera SSA.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a)
formulas(b,[('Sumar propensiones',r'$a_0=\alpha+\delta X$'),('No ocurre ningún evento hasta τ',r'$S(\tau)=\exp(-a_0\tau)$'),('Transformar un uniforme U',r'$\tau=-\log U/a_0$')])
wait=np.linspace(0,2,301);c.plot(wait,np.exp(-4*wait));c.set(xlabel='Espera τ (h)',ylabel='Probabilidad sin evento',title='Ejemplo con tasa total 4/h')
u=np.linspace(.001,.999,301);d.plot(u,-np.log(u)/4);d.set(xlabel='Uniforme U',ylabel='Espera τ (h)',title='Un uniforme se convierte en tiempo')
save(fig,'q08_espera','De producción y pérdida al próximo evento','c20','Derivar el tiempo de espera','X es un conteo entero. C–D congelan un estado con α+δX=4/h durante la espera; si ocurre un evento se recalculan propensiones. El esquema de A representa procesos de producción y retirada, no una trayectoria continua de conteos.',['A01','I02'],['Gillespie','SSA','propensión','exponencial','espera'])

# 9: promotor y ruido.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'telegraph')
formulas(b,[('Fracción de promotores encendidos',r'$p^*=k_{on}/(k_{on}+k_{off})$'),('ARN medio estacionario',r'$\mu=r p^*/\gamma$'),('Separar media de dispersión',r'$F=\operatorname{Var}(M)/\mu$')])
rates=np.logspace(-1,2,200);fano=1+20*rates/((2*rates)*(1+2*rates));c.semilogx(rates,fano);c.set(xlabel='kon=koff (1/h)',ylabel='Factor de Fano',title='La misma fracción ON, otro ruido')
tt=np.linspace(0,15,301);slow=.5*(1-np.exp(-.4*tt));fast=.5*(1-np.exp(-4*tt));d.plot(tt,slow,label='kon=koff=0,2/h');d.plot(tt,fast,label='kon=koff=2/h');d.set(xlabel='Tiempo (h)',ylabel='Probabilidad ON',title='La persistencia del promotor importa');d.legend()
save(fig,'q09_promotor_ruido','Conectar un promotor ON/OFF con media y varianza','c21','Por qué hace falta una correlación','Producción r=20 ARN/h y pérdida γ=1/h. C mantiene kon=koff, así p*=1/2 y media=10 ARN; D comienza con promotor apagado. Las curvas son probabilidades, no estados intermedios de un promotor individual.',['A01','A20'],['promotor','ráfagas','media','varianza','Fano'])

# 10: observación.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'observation')
formulas(b,[('Producción y maduración son pasos distintos',r'$p_i\prime=s-k_m p_i-\gamma p_i$'),('Solo la fracción madura emite aquí',r'$p_f\prime=k_m p_i-\gamma p_f$'),('El instrumento añade escala y fondo',r'$y=b+c p_f+\epsilon$')])
t=np.linspace(0,35,501);y=integrate(lambda t,z:[5-.5*z[0],.4*z[0]-.1*z[1]],[0,0],t)
c.plot(t,y[0]+y[1],label='Total');c.plot(t,y[1],label='Madura');c.set(xlabel='Tiempo (h)',ylabel='Proteína (nM)',title='Total y señal no son idénticos');c.legend()
rng=np.random.default_rng(41);times=np.linspace(0,35,30);mu=np.interp(times,t,2+1.5*y[1]);d.plot(t,2+1.5*y[1],label='Predicción del detector');d.scatter(times,mu+rng.normal(0,2,len(times)),s=10,label='Medidas sintéticas');d.set(xlabel='Tiempo (h)',ylabel='Intensidad (u.a.)',title='La comparación usa las unidades medidas');d.legend()
save(fig,'q10_medida','De proteína a observación, paso por paso','c22','Construir la ecuación de lo que realmente mide','s=5 nM/h, km=0,4/h, γ=0,1/h; inicio cero. Detector b=2 u.a., c=1,5 u.a./nM y error normal σ=2 u.a., semilla 41. Las observaciones son inventadas para aprender.',['A01','I04','A09'],['observación','maduración','fluorescencia','ruido','sensor'])

# 11: residuos y ajuste.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a)
formulas(b,[('Comparar en la escala del detector',r'$r_i=(\mu_i-y_i)/\sigma_i$'),('Errores normales independientes',r'$L=\prod_i p(y_i\mid\theta)$'),('Tomar logaritmos lleva a cuadrados',r'$\chi^2=\sum_i r_i^2$')])
t=np.linspace(0,15,16);true=cc.primer_orden(t,8,.4,0);rng=np.random.default_rng(42);data=true+rng.normal(0,1,t.size)
c.plot(t,true,label='Predicción');c.scatter(t,data,s=14,label='Dato sintético')
for ti,yi,mi in zip(t,data,true):c.plot([ti,ti],[yi,mi],color=C[2],lw=.8)
c.set(xlabel='Tiempo (h)',ylabel='Concentración (nM)',title='Cada segmento es un residuo');c.legend()
al=np.linspace(4,12,200);obj=[np.sum((cc.primer_orden(t,aa,.4,0)-data)**2) for aa in al];d.plot(al,obj);d.set(xlabel='α (nM/h), δ fijada',ylabel='Suma de residuos²',title='Un objetivo condicionado a los supuestos')
save(fig,'q11_ajuste','Ver qué minimiza un ajuste de ecuaciones','c23','Qué entrega la función de residuos','Datos de α=8 nM/h, δ=0,4/h, x0=0 y σ=1 nM, semilla 42. En D solo se mueve α y se fija δ; no es un perfil con δ reoptimizada.',['A01','A09','I05'],['residuo','verosimilitud','mínimos cuadrados','ajuste'])

# 12: identificabilidad.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a)
formulas(b,[('El equilibrio informa de un cociente',r'$x^*=\alpha/\delta$'),('Cambiar ambas constantes conserva el cociente',r'$(c\alpha)/(c\delta)=\alpha/\delta$'),('El transitorio conserva una segunda escala',r'$x(t)=(\alpha/\delta)(1-e^{-\delta t})$')])
t=np.linspace(0,20,301)
for aa,de in [(4,.2),(8,.4),(16,.8)]:c.plot(t,cc.primer_orden(t,aa,de,0),label=f'α={aa}, δ={de}')
c.set(xlabel='Tiempo (h)',ylabel='Estado (nM)',title='La misma altura no implica la misma rapidez');c.legend()
aa=np.linspace(2,18,301);d.plot(aa,aa/20);d.set(xlabel='α (nM/h)',ylabel='δ (1/h)',title='Todas estas parejas predicen 20 nM')
save(fig,'q12_identificabilidad','Explicar una ambigüedad antes de ajustar','c24','Cómo un transitorio','Tres parejas con α/δ=20 nM y x0=0. La línea de D es una familia de parámetros compatibles con una observación de equilibrio; no es una relación causal entre constantes de una célula.',['A01','I06'],['identificabilidad','cociente','diseño','transitorio'])

# 13: flujo entre células.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'diffusion')
formulas(b,[('Un mismo flujo sale de una y entra en otra',r'$J=q(x_1-x_2)$'),('Primera concentración',r'$x_1\prime=-J/V_1$'),('Segunda concentración',r'$x_2\prime=J/V_2$')])
t=np.linspace(0,10,301);y=integrate(lambda t,z:[-(z[0]-z[1]),(z[0]-z[1])/2],[10,0],t)
c.plot(t,y[0],label='x₁, V₁=1');c.plot(t,y[1],label='x₂, V₂=2');c.set(xlabel='Tiempo (h)',ylabel='Concentración (nM)',title='Volúmenes distintos cambian las pendientes');c.legend()
d.plot(t,y[0]+2*y[1],label='V₁x₁+V₂x₂');d.plot(t,y[0]+y[1],'--',label='x₁+x₂');d.set(xlabel='Tiempo (h)',ylabel='Cantidad o suma indicada',title='La cantidad se conserva; la suma simple no');d.legend()
save(fig,'q13_transporte','Ver dónde van las moléculas al cambiar de compartimento','c18','De intercambio entre dos células','q=1 unidad de volumen/h, V1=1 y V2=2 de esa unidad; inicio (10,0) nM. D compara cantidad normalizada V1x1+V2x2 y suma de concentraciones; esas dos curvas no tienen la misma interpretación dimensional.',['A01'],['transporte','flujo','células','volumen','conservación'])

# 14: enzima.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'enzyme')
formulas(b,[('El complejo se forma y desaparece',r'$ES\prime=k_1 E S-(k_{-1}+k_{cat})ES$'),('Aproximar la etapa rápida',r'$ES\prime\approx0,\quad E=E_T-ES$'),('Sustituir el complejo en la tasa',r'$v=V_{max}S/(K_M+S)$')])
s=np.linspace(0,50,301)
for K in [2,10,25]:c.plot(s,5*s/(K+s),label=f'KM={K} nM')
c.set(xlabel='Sustrato S (nM)',ylabel='Tasa (nM/h)',title='La tasa se aproxima a una capacidad');c.legend()
t=np.linspace(0,2,301);es=integrate(lambda t,z:[(2-z[0])*10-4*z[0]],[0],t)[0]
d.plot(t,es);d.axhline(20/14,color=C[1],ls='--',label='Complejo cuasiestacionario');d.set(xlabel='Tiempo (h)',ylabel='Complejo ES (nM)',title='La aproximación omite una relajación');d.legend()
save(fig,'q14_enzima','De unión y catálisis a Michaelis–Menten','c16','Michaelis–Menten exige otra','C usa Vmax=5 nM/h. D ilustra una etapa de unión con E total=2 nM, S libre fijado a 10 nM, k1=1/(nM·h) y k−1+kcat=4/h, sin agotamiento de S. No son la misma parametrización ni datos de una enzima.',['A01','D08'],['Michaelis–Menten','enzima','complejo','saturación','cuasiestacionario'])

# 15: dos vías.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'feedforward')
formulas(b,[('Una etapa intermedia tarda en acumularse',r'$y\prime=u-y$'),('La salida recibe caminos opuestos',r'$z\prime=u-y-z$'),('Desde cero con entrada unitaria',r'$y=1-e^{-t},\quad z=t e^{-t}$')])
t=np.linspace(0,8,301);c.plot(t,np.ones_like(t),label='Directa u');c.plot(t,1-np.exp(-t),label='Intermedia y');c.set(xlabel='Tiempo normalizado',ylabel='Contribución normalizada',title='La compensación llega después');c.legend()
d.plot(t,t*np.exp(-t));d.set(xlabel='Tiempo normalizado',ylabel='Desviación z',title='La diferencia forma un pulso')
save(fig,'q15_dos_vias','Cómo dos vías opuestas fabrican un pulso','c15','Seguir el inicio de un escalón','Todas las constantes de las dos ecuaciones se fijan a uno en escalas coherentes; entrada uno y estados iniciales cero. z es una desviación local, no una ley válida para concentraciones absolutas arbitrarias.',['A01','D05'],['feedforward','pulso','adaptación','vía lenta','señal'])

# 16: invertir un sensor.
fig,axs=grid();a,b,c,d=axs.flat;molecular(a,'sensor')
formulas(b,[('Una entrada aumenta la retirada',r'$S\prime=s-(\gamma_0+kA)S$'),('Solo en equilibrio puede omitirse la pendiente',r'$A_{est}=(s/S-\gamma_0)/k$'),('Durante un cambio hay una corrección',r'$A=(s/S-\gamma_0-S\prime/S)/k$')])
t=np.linspace(0,20,401);S=5+5*np.exp(-.2*t);sp=-np.exp(-.2*t)
c.plot(t,S);c.axhline(5,color=C[1],ls='--');c.set(xlabel='Tiempo (min)',ylabel='Sensor S (nM)',title='La salida todavía está cambiando')
d.plot(t,(1/S-.1)/.02,label='Inversión estática');d.plot(t,(1/S-.1-sp/S)/.02,'--',label='Inversión dinámica');d.axhline(5,color='gray',lw=.6);d.set(xlabel='Tiempo (min)',ylabel='Entrada A (escala docente)',title='La pendiente explica la diferencia');d.legend()
save(fig,'q16_sensor','De una reacción de pérdida a una entrada inferida','c26','Derivar la inversión dinámica','s=1 nM/min, γ0=0,1/min, k=0,02 por unidad de entrada y minuto, A=5 desde t=0 y S(0)=10 nM. El cálculo usa la derivada exacta sin ruido; no calibra un sensor publicado.',['A01','P02','V01'],['sensor','auxina','inversión','derivada','calibración'])

# 17: una condición cambia; las constantes y el estado tienen papeles distintos.
fig,axs=grid();a,b,c,d=axs.flat
a.axis('off');a.set(xlim=(0,4.2),ylim=(0,3),title='A · Tres momentos del mismo mecanismo')
s0=12/(1+(1/5)**2);e0=s0/.3;sf=12/(1+(10/5)**2);ef=sf/.3
t=np.linspace(0,25,501);R=np.where(t<5,1.,10.);s=12/(1+(R/5)**2)
E=np.where(t<5,e0,ef+(e0-ef)*np.exp(-.3*(t-5)))
for y,ti,rr,ee in [(2.5,0,1,e0),(1.55,5,10,e0),(.6,25,10,E[-1])]:
    protein(a,.4,y,'R',C[2],.19);art.dna(a,1.15,y,'',width=.85);protein(a,3.35,y,'E',C[0],.24)
    arrow(a,(.65,y),(1.05,y),bar=True);arrow(a,(2.15,y),(3.0,y))
    a.text(2.1,y-.32,f't={ti} h: R={rr}; E={ee:.2f} nM'.replace('.',','),ha='center',fontsize=7)
b.step(t,R,where='post',color=C[2],label='Entrada R(t)');b.set(xlabel='Tiempo (h)',ylabel='Represor R (nM)',title='B · La condición externa sube en 5 h',ylim=(0,12))
c.step(t,s,where='post',color=C[1],label='Producción efectiva s(R)');c.set(xlabel='Tiempo (h)',ylabel='Producción (nM/h)',title='La producción baja; smax sigue fija',ylim=(0,14))
d.plot(t,E,label='Enzima E');d.axhline(ef,color='gray',ls='--');d.set(xlabel='Tiempo (h)',ylabel='Enzima E (nM)',title='La enzima responde de forma gradual',ylim=(0,45))
for ax,yy,left,right in [(b,R,'R=1 nM','R=10 nM'),(c,s,'s≈11,54 nM/h','s=2,4 nM/h'),(d,E,'E₀≈38,46 nM','E₂₅≈8,076 nM')]:
    ax.axvline(5,color='#778b84',lw=.7,ls=':')
    ax.annotate(left,(t[0],yy[0]),xytext=(2,yy[0]+(2 if ax is not d else -8)),fontsize=7,arrowprops=dict(arrowstyle='->',lw=.6,color='#45695f'))
    ax.annotate(right,(t[-1],yy[-1]),xytext=(11,6 if ax is b else yy[-1]+(3 if ax is not d else 9)),fontsize=7,arrowprops=dict(arrowstyle='->',lw=.6,color='#45695f'))
d.text(8,32,'δ=0,3/h permanece fija\nE∞=2,4/0,3=8 nM',fontsize=7,color='#345e53')
assert abs(e0-s0/.3)<1e-12 and abs(E[100]-e0)<1e-12
assert abs(E[-1]-(8+(e0-8)*np.exp(-6)))<1e-12
save(fig,'q17_represion','Inicio, cambio y final: una enzima bajo represión','edo','Leer el inicio, el recorrido y el final','Modelo reducido E′=s(R)−δE, s(R)=smax/[1+(R/K)ⁿ]. smax=12 nM/h, K=5 nM, n=2, δ=0,3/h. Se resume la producción de enzima sin un estado explícito de ARN. Inicialmente R=1 nM y E está en su equilibrio de 38,46 nM. En t=5 h R sube a 10 nM, la producción pasa de 11,54 a 2,4 nM/h y E no salta: se relaja hacia 8 nM. A las 25 h E≈8,076 nM; ese final dibujado aún no es el límite exacto. La pérdida δE también disminuye al disminuir E, aunque δ sea constante.',['A01','A02','D07'],['inicio','final','represión','enzima','condición inicial','entrada','parámetro constante','cambio temporal'])

p=ROOT/'docs'/'figures.json';old=json.loads(p.read_text(encoding='utf8'));replacement={f['id']:f for f in META};known={f['id'] for f in old}
result=[replacement.get(f['id'],f) for f in old]+[f for f in META if f['id'] not in known]
p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print('Secuencias visuales añadidas:',len(META),'Total:',len(result))
