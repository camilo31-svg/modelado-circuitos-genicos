"""Figuras docentes originales y reproducibles; no son datos de artículos."""
from pathlib import Path
import sys,json,string
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import lectura_curvas
from scipy.stats import poisson,norm,binom
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists(): ROOT=BASE
sys.path.insert(0,str(ROOT/'python'))
from circuitos import *
OUT=ROOT/'docs'/'assets'/'figures';OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.labelsize':10,'axes.titlesize':11,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7,'lines.linewidth':1.8,'figure.facecolor':'white','savefig.facecolor':'white','svg.fonttype':'none','axes.prop_cycle':plt.cycler(color=['#167d9a','#d87826','#238674','#8262a3'])})
META=[]
def panels(n=2):
    return plt.subplots(1,n,figsize=(8,3.45),layout='constrained')
def save(fig,slug,title,chapters,caption,tags):
    axes=[a for a in fig.axes if a.get_label()!='<colorbar>']
    for i,a in enumerate(axes):
        a.text(-.13,1.12,string.ascii_uppercase[i],transform=a.transAxes,weight='bold',fontsize=12)
        a.tick_params(width=.6,labelsize=9)
    curves=lectura_curvas.extraer(fig,slug)
    fig.savefig(OUT/(slug+'.png'),dpi=220,bbox_inches='tight')
    fig.savefig(OUT/(slug+'.svg'),bbox_inches='tight')
    META.append(dict(id=slug,title=title,chapters=chapters,caption=caption,alt=title+'. '+caption,tags=tags,png='assets/figures/'+slug+'.png',svg='assets/figures/'+slug+'.svg',source='Simulación o esquema didáctico original; parámetros ilustrativos.',curve_guide=curves))
    plt.close(fig)

t=np.linspace(0,10,200)
fig,ax=panels();ax[0].plot(t,10*np.ones_like(t),label='Cantidad constante');ax[0].plot(t,10*np.exp(-.2*t),label='Concentración')
ax[0].set(xlabel='Tiempo (h)',ylabel='Valor relativo (u.a.)',title='Expandir diluye');ax[0].legend(fontsize=8)
vol=np.logspace(-2,1,200);ax[1].loglog(vol,6.02214076e2*vol);ax[1].set(xlabel='Volumen (pL)',ylabel='Moléculas a 1 nM',title='Concentración y conteo')
save(fig,'f01_unidades','Cantidad, concentración y volumen',['c01','c25'],'A: diez unidades de cantidad permanecen constantes; con V/V0=exp(0,2t), la concentración cae por dilución. B: a 1 nM, el número esperado es 602,214 por pL, usando el valor exacto de Avogadro. Un valor esperado fraccionario no es una molécula partida.',['unidades','volumen','dilución','Avogadro'])

fig,ax=panels();x=np.linspace(0,6,200);y=x*x
ax[0].plot(x,y,label='x²');ax[0].plot(x,6*x-9,'--',label='Tangente en x=3');ax[0].set(xlabel='x',ylabel='f(x)',title='La derivada es pendiente');ax[0].legend(fontsize=8)
ax[1].plot(x,2*x);ax[1].fill_between(x,0,2*x,alpha=.18);ax[1].set(xlabel='Tiempo (h)',ylabel='Tasa (u.a./h)',title='El área acumula cantidad')
save(fig,'f02_calculo','Derivar y acumular',['c03','c05','c06'],'A: f(x)=x² y su tangente en x=3, con pendiente 6. La tangente aproxima localmente, no en todo el dominio. B: integrar la tasa 2t entre 0 y 6 produce 36 unidades; la tasa cambia mientras la cantidad se acumula. Los ejes son ejemplos abstractos.',['derivada','integral','pendiente','área'])

fig,ax=panels();t=np.linspace(0,20,300)
for d in [.1,.2,.4]:
    ax[0].plot(t,np.exp(-d*t),label=f'delta={d}/h');ax[1].semilogy(t,np.exp(-d*t))
ax[0].set(xlabel='Tiempo (h)',ylabel='Fracción restante',title='Decaimiento exponencial');ax[0].legend(fontsize=8)
ax[1].set(xlabel='Tiempo (h)',ylabel='Fracción (escala log)',title='La pendiente revela la tasa')
save(fig,'f03_exponencial','Tasas, logaritmos y semividas',['c02','c04'],'Tres pérdidas de primer orden: x/x0=exp(-delta t). A: la misma fracción se pierde en intervalos iguales. B: una escala logarítmica convierte cada exponencial en recta. Las semividas son 6,93; 3,47 y 1,73 h. Una recta semilogarítmica puede apoyar este modelo dentro de su rango medido.',['logaritmo','semivida','exponencial'])

fig,ax=panels();t=np.linspace(0,30,250)
for a,d in [(2,.2),(8,.4),(3,.1)]:
    y=primer_orden(t,a,d);ax[0].plot(t,y,label=f'a={a}, d={d}');ax[1].plot(d*t,y/(a/d))
ax[0].set(xlabel='Tiempo (h)',ylabel='Concentración (u.a.)',title='Tres escalas distintas');ax[0].legend(fontsize=8)
ax[1].set(xlabel='tau = delta·t',ylabel='x / (alfa/delta)',title='Una curva adimensional')
save(fig,'f04_escalas','Adimensionalizar para comparar',['c07'],'A: respuestas con producción alfa y pérdida delta diferentes. B: dividir concentración por alfa/delta y tiempo por 1/delta colapsa las curvas para x0=0. Esto muestra una forma común de ecuación; no demuestra que distintos organismos tengan mecanismos idénticos.',['adimensionalización','escala','álgebra'])

fig,ax=panels();t=np.linspace(0,30,300);y=integrar(gen,[0,0],t)
ax[0].plot(t,y[0]);ax[0].axhline(4,color='#777',ls='--');ax[0].set(xlabel='Tiempo (h)',ylabel='ARN (u.a.)',title='Producción y pérdida de ARN')
ax[1].plot(t,y[1],color='#d87826');ax[1].axhline(60,color='#777',ls='--');ax[1].set(xlabel='Tiempo (h)',ylabel='Proteína (u.a.)',title='Una segunda etapa añade demora')
save(fig,'f05_gen','Del ARN a la proteína',['c08','c09'],'Modelo original: dm/dt=4-m; dp/dt=3m-0,2p; ambos estados empiezan en cero. Las líneas discontinuas indican m*=4 y p*=60. El ARN se acerca antes al equilibrio; la proteína integra una señal que todavía está cambiando. No se representan mediciones experimentales.',['ARN','proteína','balance','Python'])

fig,ax=panels();t=np.linspace(0,10,200);ax[0].plot(t,np.exp(-t),'k',label='Exacta')
for h in [.2,1.8,2.2]:
    tt=np.arange(0,10+h/2,h);yy=(1-h)**np.arange(len(tt));ax[0].plot(tt,yy,'o-',ms=3,label=f'h={h}')
ax[0].set(xlabel='Tiempo (h)',ylabel='Estado (u.a.)',title='Euler puede inventar oscilaciones',ylim=(-2,3));ax[0].legend(fontsize=8)
h=np.logspace(-3,-.1,40);err=[]
for dt in h:
    n=int(np.ceil(2/dt));paso=2/n;err.append(abs((1-paso)**n-np.exp(-2)))
ax[1].loglog(h,err);ax[1].set(xlabel='Paso objetivo (h)',ylabel='Error absoluto en t=2 h',title='La convergencia se comprueba')
save(fig,'f06_numerica','Error, estabilidad y positividad',['c10'],'A: para dx/dt=-x, Euler multiplica por 1-h. h=1,8 es estable pero alterna de signo; h=2,2 es inestable. El proceso real permanece positivo. B: el error global disminuye aproximadamente de forma lineal al refinar el paso. Esta figura separa estabilidad numérica, exactitud y sentido físico.',['Euler','estabilidad','solver','error'])

fig,ax=panels();x=np.linspace(0,5,300)
for n in [1,2,4]:ax[0].plot(x,hill(x,n=n),label=f'n={n}')
ax[0].set(xlabel='Entrada / K',ylabel='Fracción activada',title='K y n cumplen papeles distintos');ax[0].legend(fontsize=8)
for K in [.5,1,2]:ax[1].plot(x,hill(x,K=K,n=2,activar=False),label=f'K={K}')
ax[1].set(xlabel='Entrada (u.a.)',ylabel='Fracción no reprimida',title='Mover el umbral');ax[1].legend(fontsize=8)
save(fig,'f07_hill','Funciones de regulación y saturación',['c16'],'A: con K=1, todas las curvas de activación pasan por 0,5; n modifica la pendiente. B: represión con n=2 y varios K. Estas son relaciones fenomenológicas de entrada y salida: un ajuste de Hill no identifica por sí solo la estequiometría ni genera memoria.',['Hill','Michaelis','cooperatividad','saturación'])

fig,ax=panels();t=np.linspace(0,10,300)
yn=integrar(lambda t,y:[10/(1+y[0])-y[0]],[0],t)[0];eq=(-1+np.sqrt(41))/2
ax[0].plot(t,yn/eq,label='Autorrepresión');ax[0].plot(t,primer_orden(t,eq,1)/eq,label='Sin feedback')
ax[0].set(xlabel='Tiempo (h)',ylabel='Fracción de su equilibrio',title='Comparar a igual salida');ax[0].legend(fontsize=8)
x=np.linspace(0,7,300);ax[1].plot(x,10/(1+x),label='Producción');ax[1].plot(x,x,label='Pérdida');ax[1].set(xlabel='Estado (u.a.)',ylabel='Tasa (u.a./h)',title='El equilibrio es una intersección');ax[1].legend(fontsize=8)
save(fig,'f08_feedback','Retroalimentación y equilibrio',['c11','c12'],'Autorrepresión dx/dt=10/(1+x)-x. El equilibrio positivo es (-1+sqrt(41))/2. A: comparación normalizada con un sistema sin feedback ajustado a la misma salida estacionaria y pérdida. B: producción y pérdida se cruzan una vez. La mejora dinámica depende del criterio de comparación y de los supuestos.',['retroalimentación','equilibrio','autorrepresión'])

fig,ax=panels();x=np.linspace(0,11,500)
ax[0].plot(x,10/(1+x*x),label='dz/dt=0');ax[0].plot(10/(1+x*x),x,label='dx/dt=0')
for ini in [[9,.1],[.1,9],[4,3]]:
    y=integrar(toggle,ini,np.linspace(0,20,300));ax[0].plot(y[0],y[1],alpha=.65)
ax[0].set(xlabel='x',ylabel='z',title='Nulclinas y trayectorias',xlim=(0,11),ylim=(0,11));ax[0].legend(fontsize=8)
for ini in [[9,.1],[.1,9]]:
    tt=np.linspace(0,12,300);yy=integrar(toggle,ini,tt);ax[1].plot(tt,yy[0],label=f'x0={ini[0]}')
ax[1].set(xlabel='Tiempo adimensional',ylabel='x (adimensional)',title='La historia cambia el estado');ax[1].legend(fontsize=8)
save(fig,'f09_toggle','Biestabilidad y cuencas de atracción',['c13'],'Modelo original adimensional: dx/dt=10/(1+z²)-x y dz/dt=10/(1+x²)-z. A: las nulclinas se cruzan tres veces; las trayectorias ilustran cuencas diferentes. B: condiciones iniciales opuestas alcanzan dos salidas persistentes. No es una reconstrucción cuantitativa del experimento de Gardner.',['toggle','bistabilidad','memoria','nulclina'])

fig,ax=panels();t=np.linspace(0,100,1501);y=integrar(represilador,[.1,2,5],t)
for i in range(3):ax[0].plot(t,y[i],label=f'x{i+1}')
ax[0].set(xlabel='Tiempo adimensional',ylabel='Concentración / K',title='Represión cíclica');ax[0].legend(fontsize=8)
ax[1].plot(y[0,700:],y[1,700:]);ax[1].set(xlabel='x1 / K',ylabel='x2 / K',title='Órbita tras el transitorio')
save(fig,'f10_represilador','Oscilaciones persistentes en un anillo',['c14'],'Anillo reducido dx_i/dt=30/(1+x_previa³)-x_i, con estado inicial (0,1;2;5). A: tres variables oscilan desfasadas. B: proyección de la órbita final. Tiempo y estados son adimensionales; la figura no pretende reproducir amplitudes o períodos de un artículo. Hay que comprobar persistencia y convergencia numérica.',['represilador','oscilación','fase'])

fig,ax=panels();t=np.linspace(0,15,501);u=(t>=2).astype(float)
def ff(t,y):
    u=float(t>=2);z,r=y
    return [(u-z)/2,3*u/(1+4*z)-r]
y=integrar(ff,[0,0],t)
ax[0].plot(t,u,label='Entrada');ax[0].plot(t,y[0],label='Rama lenta');ax[0].plot(t,y[1],label='Salida');ax[0].set(xlabel='Tiempo (h)',ylabel='Señal (u.a.)',title='Un pulso por dos caminos');ax[0].legend(fontsize=8)
gate=np.array([[0,0],[0,1]]);im=ax[1].imshow(gate,cmap='Blues',vmin=0,vmax=1);ax[1].set(xticks=[0,1],yticks=[0,1],xlabel='Entrada A',ylabel='Entrada B',title='AND idealizada')
for i in range(2):
    for j in range(2):ax[1].text(j,i,str(gate[i,j]),ha='center',va='center',color='white' if gate[i,j] else 'black')
save(fig,'f11_logica','Pulsos, lógica y dinámica',['c15'],'A: ejemplo incoherente: una entrada escalón activa salida y una rama lenta que la reprime. La salida presenta un máximo pero no vuelve exactamente al basal; pulso y adaptación perfecta son conceptos distintos. B: tabla AND ideal. Un circuito bioquímico necesita umbrales y márgenes para aproximarla.',['feedforward','adaptación','AND','lógica'])

fig,ax=panels();t=np.linspace(0,20,400)
for tau in [1,3,6]:ax[0].plot(t,np.where(t>=tau,1-np.exp(-np.maximum(t-tau,0)),0),label=f'retraso={tau} h')
ax[0].set(xlabel='Tiempo (h)',ylabel='Respuesta (u.a.)',title='Un retraso desplaza el inicio');ax[0].legend(fontsize=8)
T=np.linspace(0,20,401)
def chain(t,y):
    u=float(t>=2);return [(u-y[0])*2,(y[0]-y[1])*2,(y[1]-y[2])*2]
z=integrar(chain,[0,0,0],T)
for i in range(3):ax[1].plot(T,z[i],label=f'Etapa {i+1}')
ax[1].set(xlabel='Tiempo (h)',ylabel='Señal normalizada',title='Una cadena también suaviza');ax[1].legend(fontsize=8)
save(fig,'f12_retrasos','Retraso puro y etapas intermedias',['c17'],'A: respuesta de primer orden que empieza tras un retraso fijo. B: tres etapas con tasa 2/h tras una entrada en t=2 h. Una cadena reparte tiempos de tránsito y suaviza; un retraso puro desplaza una señal. Son hipótesis distintas y requieren algoritmos y condiciones iniciales diferentes.',['retraso','híbrido','evento','cadena'])

fig,ax=panels();n=40;s=np.zeros(n);s[5:10]=3;t=np.linspace(0,20,201);y=integrar(tejido,np.zeros(n),t,args=(s,))
im=ax[0].imshow(y,aspect='auto',origin='lower',extent=[0,20,0,n],cmap='viridis');ax[0].set(xlabel='Tiempo (h)',ylabel='Célula',title='Producción local e intercambio');fig.colorbar(im,ax=ax[0],label='u.a.')
for k in [0,.4,2]:
    z=integrar(tejido,np.zeros(n),t,args=(s,.4,k));ax[1].plot(z[:,-1],label=f'k={k}/h')
ax[1].set(xlabel='Célula',ylabel='Concentración (u.a.)',title='El intercambio ensancha el perfil');ax[1].legend(fontsize=8)
save(fig,'f13_espacio','Un tejido como red de células',['c18','c25'],'Cadena de 40 células de igual volumen, pérdida 0,4/h, producción 3 u.a./h en las células 5–9 y bordes sin flujo. A: intercambio 0,8/h. B: perfiles en t=20 h para distintas tasas de intercambio. Modelo conceptual de transporte, sin calibración vegetal ni identificación con auxina real.',['difusión','tejido','grafo','espacio'])

fig,ax=panels();k=np.arange(0,25)
for mu in [2,6,12]:ax[0].plot(k,poisson.pmf(k,mu),'o-',ms=3,label=f'media={mu}')
ax[0].set(xlabel='Conteo (moléculas)',ylabel='Probabilidad',title='La Poisson es discreta');ax[0].legend(fontsize=8)
x=np.linspace(-4,4,300);ax[1].plot(x,norm.pdf(x));ax[1].fill_between(x,0,norm.pdf(x),where=abs(x)<1,alpha=.2);ax[1].set(xlabel='Desviación / sigma',ylabel='Densidad',title='Densidad no es probabilidad puntual')
save(fig,'f14_probabilidad','Contar eventos y medir variación',['c19'],'A: distribuciones Poisson con varianza igual a la media. B: densidad normal estándar; la probabilidad es un área y la franja de una desviación típica contiene aproximadamente el 68,3%. No se debe asignar densidad a un punto como si fuera su probabilidad.',['probabilidad','Poisson','normal','varianza'])

fig,ax=panels();final=[]
for seed in range(300):
    tt,xx=ssa_nacimiento_muerte(seed=seed);final.append(xx[-1])
    if seed<3:ax[0].step(tt,xx,where='post',alpha=.7)
t=np.linspace(0,20,100);ax[0].plot(t,primer_orden(t,5,.5),'k--',label='Media teórica');ax[0].set(xlabel='Tiempo (h)',ylabel='Moléculas',title='La media no es una trayectoria');ax[0].legend(fontsize=8)
k=np.arange(0,24);ax[1].hist(final,bins=np.arange(-.5,24.5),density=True,alpha=.5,label='300 simulaciones');ax[1].plot(k,poisson.pmf(k,10),'o',ms=3,label='Poisson(10)');ax[1].set(xlabel='Moléculas en t=20 h',ylabel='Probabilidad',title='Ensamble y distribución');ax[1].legend(fontsize=8)
save(fig,'f15_ssa','Gillespie frente al balance medio',['c20'],'Nacimiento 5 moléculas/h, muerte 0,5 por molécula y hora, estado inicial cero. A: tres trayectorias SSA y media exacta. B: 300 estados finales y referencia Poisson(10), cercana al límite estacionario. Las semillas van de 0 a 299; la variación entre trayectorias es parte del modelo.',['Gillespie','SSA','CME','estocástico'])

fig,ax=panels();t,s,x=telegrapho();ax[0].step(t,s,where='post');ax[0].set(xlabel='Tiempo (h)',ylabel='Promotor 0/1',title='Cambio de estado regulador',ylim=(-.1,1.2))
ax[1].step(t,x,where='post',color='#d87826');ax[1].set(xlabel='Tiempo (h)',ylabel='Moléculas',title='Ráfagas y memoria temporal')
save(fig,'f16_rafagas','Un promotor telegráfico',['c21'],'Simulación original: kon=0,15/h, koff=0,4/h, producción en ON=14 moléculas/h, pérdida=0,4/h, semilla 7. A: estado del promotor. B: abundancia discreta del producto. La persistencia del estado ON genera ráfagas; una fluctuación correlacionada no equivale a errores independientes de medición.',['ráfaga','promotor','ruido','telegráfico'])

fig,ax=panels();t=np.linspace(0,35,301);y=integrar(maduracion,[0,0],t)
ax[0].plot(t,y.sum(axis=0),label='Total');ax[0].plot(t,y[1],label='Madura');ax[0].set(xlabel='Tiempo (h)',ylabel='Concentración (u.a.)',title='Lo visible llega después');ax[0].legend(fontsize=8)
rng=np.random.default_rng(9);ax[1].plot(t,y[1],label='Estado maduro');ax[1].scatter(t[::10],1.5*y[1,::10]+8+rng.normal(0,1.5,len(t[::10])),s=12,label='Lectura sintética');ax[1].set(xlabel='Tiempo (h)',ylabel='Señal / estado (unidades propias)',title='Ganancia, fondo y error');ax[1].legend(fontsize=8)
save(fig,'f17_observacion','Un modelo del proceso y otro de la medida',['c22'],'Producción 5 u.a./h, maduración 0,4/h y pérdida 0,1/h. A: proteína total y madura. B: y=1,5·madura+8+error normal de desviación 1,5, semilla 9. Los puntos son sintéticos. Ganancia, fondo y cinética del reportero pueden confundirse con parámetros del circuito.',['reportero','fluorescencia','maduración','medición'])

fig,ax=panels();rng=np.random.default_rng(2026);t=np.linspace(0,20,31);obs=primer_orden(t,8,.4)+rng.normal(0,1,len(t));theta,_=ajustar_primer_orden(t,obs);pred=primer_orden(t,*theta)
ax[0].scatter(t,obs,s=13,label='Datos sintéticos');ax[0].plot(t,pred,label='Ajuste');ax[0].set(xlabel='Tiempo (h)',ylabel='Concentración (u.a.)',title='Ajustar una hipótesis');ax[0].legend(fontsize=8)
ax[1].scatter(t,obs-pred,s=13);ax[1].axhline(0,color='gray',ls='--');ax[1].set(xlabel='Tiempo (h)',ylabel='Residuo (u.a.)',title='Los residuos también hablan')
save(fig,'f18_ajuste','Estimación y comprobación del ajuste',['c23'],'Datos sintéticos de alfa=8 u.a./h, delta=0,4/h y x0=0, más errores gaussianos independientes de desviación 1 (semilla 2026). Ajuste en logparámetros para mantener positividad. A: curva y puntos. B: residuos. Recuperar la verdad simulada comprueba el procedimiento; no valida un sistema experimental.',['estimación','likelihood','residuo','mínimos cuadrados'])

fig,ax=panels();a=np.linspace(1,15,100);d=np.linspace(.05,.9,100);A,D=np.meshgrid(a,d);err=(A/D-20)**2
im=ax[0].contourf(A,D,np.log10(1+err),levels=20,cmap='viridis');ax[0].plot(20*d,d,'w--');ax[0].set(xlabel='alfa (u.a./h)',ylabel='delta (1/h)',title='Un equilibrio deja una cresta');fig.colorbar(im,ax=ax[0],label='log10(1+error²)')
t=np.linspace(0,20,200)
for aa,dd in [(2,.1),(8,.4),(14,.7)]:ax[1].plot(t,primer_orden(t,aa,dd),label=f'{aa}/{dd}')
ax[1].set(xlabel='Tiempo (h)',ylabel='Concentración (u.a.)',title='El transitorio distingue tasas');ax[1].legend(fontsize=8)
save(fig,'f19_identificabilidad','Predecir una salida no identifica todos los parámetros',['c24'],'A: observar solo x*=20 admite todas las parejas alfa=20·delta; el mapa muestra el error de equilibrio. B: tres parejas con el mismo cociente producen transitorios diferentes desde cero. Para estimarlas, la observación temporal debe tener resolución y precisión suficientes; más puntos redundantes no garantizan información nueva.',['identificabilidad','sensibilidad','parámetro','diseño'])

fig,ax=panels();a=np.linspace(0,30,300);r=.1/(.1+.02*a);ax[0].plot(a,r);ax[0].set(xlabel='Entrada de auxina (u.a.)',ylabel='Sensor / basal',title='Más entrada, menos sensor')
rr=np.linspace(.08,1,300);ax[1].plot(rr,5*(1/rr-1));ax[1].set(xlabel='Cociente normalizado r',ylabel='Entrada inferida (u.a.)',title='Invertir puede amplificar errores')
save(fig,'f20_auxina','Leer un sensor de degradación',['c26'],'Ejemplo conceptual dS/dt=p-(0,1+0,02a)S, con tiempo en minutos y entrada a en unidades arbitrarias. A: lectura estacionaria normalizada r. B: inversión a=5(1/r-1). Cerca del fondo, pequeños errores en r causan errores grandes en a. No constituye una calibración de DII ni R2D2.',['auxina','sensor','DII','plantas','calibración'])

fig,ax=panels();i=np.arange(1,13);A=(i>=3)&(i<=9);B=(i>=7)&(i<=11);M=np.array([A,B,A&B,A&(~B)],float)
im=ax[0].imshow(M,aspect='auto',cmap='Blues',vmin=0,vmax=1);ax[0].set(yticks=range(4),yticklabels=['A','B','A AND B','A AND NOT B'],xticks=[0,5,11],xticklabels=[1,6,12],xlabel='Célula',title='Intersecciones espaciales')
ax[1].plot(i,hill(i,K=5,n=4)*hill(13-i,K=4,n=4),'o-');ax[1].set(xlabel='Célula',ylabel='Salida normalizada',title='Una implementación continua')
save(fig,'f21_raices','De la lógica a un patrón de tejido',['c27'],'A: entradas binarias artificiales en 12 células; una intersección selecciona un dominio y AND NOT excluye otro. B: producto de dos funciones de Hill de entradas espaciales opuestas. Es una ilustración del razonamiento espacial, no una reproducción de los circuitos o morfologías del artículo de Brophy.',['raíz','lógica espacial','AND','Brophy','plantas'])

fig,ax=panels();t=np.linspace(0,20,500);inp=((t>=3)&(t<=6)).astype(float);H=np.maximum(np.minimum(t-3,3),0);mem=1-np.exp(-.6*H)
ax[0].plot(t,inp,label='Pulso de entrada');ax[0].plot(t,mem,label='Probabilidad de registro');ax[0].set(xlabel='Tiempo (h)',ylabel='Entrada / probabilidad',title='Registrar una exposición');ax[0].legend(fontsize=8)
dur=np.linspace(0,8,300);ax[1].plot(dur,1-np.exp(-.6*dur));ax[1].set(xlabel='Duración de exposición (h)',ylabel='Fracción esperada registrada',title='La memoria puede ser probabilística')
save(fig,'f22_memoria','Memoria persistente y registro probabilístico',['c28'],'Modelo de registro irreversible con tasa 0,6/h durante una exposición. A: pulso de 3 horas y probabilidad acumulada 1-exp(-tasa·duración). B: duración y fracción registrada. Es una población de estados con probabilidad de cambio, no una concentración continua de ADN ni una reconstrucción del artículo de memoria vegetal.',['memoria','recombinasa','probabilidad','plantas'])

fig,ax=panels();t=np.linspace(0,120,1000)
ax[0].plot(t,np.cos(2*np.pi*t/24),label='24 h');ax[0].plot(t,np.cos(2*np.pi*t/26),label='26 h');ax[0].set(xlabel='Tiempo (h)',ylabel='Señal centrada (u.a.)',title='Un período pequeño cambia la fase');ax[0].legend(fontsize=8)
phase=np.linspace(-np.pi,np.pi,300);ax[1].plot(phase,0*phase+.1,label='Desajuste');ax[1].plot(phase,.3*np.sin(phase),label='Acoplamiento');ax[1].set(xlabel='Diferencia de fase (rad)',ylabel='Tasa de fase (rad/h)',title='Bloqueo de fase como equilibrio');ax[1].legend(fontsize=8)
save(fig,'f23_reloj','Período, fase y sincronización',['c29'],'A: dos sinusoides ilustrativas de períodos 24 y 26 h; la fase diverge. B: un modelo de fase dphi/dt=0,1-0,3 sin(phi) puede bloquearse donde se cruzan las curvas, con estabilidad dependiente de la pendiente. Son ejemplos matemáticos, sin pretender reconstruir el reloj molecular de Arabidopsis.',['circadiano','reloj','fase','Arabidopsis'])

fig,ax=panels();r=np.linspace(0,10,300);ax[0].plot(r,r,label='Sin competencia');ax[0].plot(r,r/(1+.3*r),label='Recursos finitos');ax[0].set(xlabel='Demanda relativa',ylabel='Salida relativa',title='La carga cambia la relación');ax[0].legend(fontsize=8)
q=np.linspace(0,8,200)
for d in [0,1,4]:ax[1].plot(q,q/(1+q+d),label=f'Competidor={d}')
ax[1].set(xlabel='Demanda del módulo A',ylabel='Fracción de recurso para A',title='Módulos conectados por el huésped');ax[1].legend(fontsize=8)
save(fig,'f24_recursos','Carga y acoplamiento invisible',['c30','c32'],'A: relaciones originales de salida frente a demanda: lineal y saturante r/(1+0,3r). B: reparto ilustrativo de un recurso normalizado entre A, un competidor y fondo. Un módulo puede alterar otro sin enlace regulador directo. No es un ajuste a datos de crecimiento ni una ley universal.',['carga','retroactividad','recursos','control'])

fig,ax=panels();rng=np.random.default_rng(21);tt=np.linspace(0,20,31);ests=[]
for _ in range(100):
    obs=primer_orden(tt,8,.4)+rng.normal(0,1,len(tt));p,_=ajustar_primer_orden(tt,obs);ests.append(p)
ests=np.array(ests);ax[0].scatter(*ests.T,s=13,alpha=.6);ax[0].set(xlabel='alfa estimada (u.a./h)',ylabel='delta estimada (1/h)',title='El procedimiento tiene variación')
t=np.linspace(0,30,200);preds=np.array([primer_orden(t,*p) for p in ests]);lo,hi=np.quantile(preds,[.025,.975],axis=0);ax[1].fill_between(t,lo,hi,alpha=.25);ax[1].plot(t,primer_orden(t,8,.4));ax[1].set(xlabel='Tiempo (h)',ylabel='Concentración (u.a.)',title='Incertidumbre de la curva media')
save(fig,'f25_incertidumbre','Parámetros correlacionados y bandas',['c23','c24'],'Cien conjuntos sintéticos con errores normales de desviación 1 y verdad (8;0,4); semilla 21. A: estimaciones. B: cuantiles puntuales de las curvas ajustadas. La banda refleja variación del ajuste bajo este modelo, no un intervalo de predicción de nuevas lecturas ni incertidumbre estructural o garantía simultánea.',['bootstrap','incertidumbre','intervalo','Bayes'])

fig,ax=panels();ax[0].axis('off');labels=['Pregunta','Supuestos','Modelo','Comprobación','Datos y ajuste','Predicción nueva']
for j,lab in enumerate(labels):
    y=1-j*.17;ax[0].text(.5,y,lab,ha='center',va='center',bbox=dict(boxstyle='round,pad=.4',facecolor='#e5f2f2',edgecolor='#167d9a'))
    if j<5:ax[0].annotate('',(.5,y-.11),(.5,y-.05),arrowprops=dict(arrowstyle='->',color='#444'))
ax[0].set_title('Un ciclo de razonamiento')
ax[1].barh(['Datos','Estructura','Parámetros','Algoritmo'],[.8,.9,.5,.3],color=['#167d9a','#d87826','#238674','#8262a3']);ax[1].set(xlabel='Magnitud ilustrativa, sin medida empírica',title='Incertidumbres diferentes',xlim=(0,1))
save(fig,'f26_investigar','Del resultado numérico a una conclusión defendible',['c00','c31','c33','c34','c35','c37'],'A: cada predicción debe conectarse con una pregunta, supuestos y pruebas. B: esquema cualitativo de fuentes de incertidumbre; las alturas son arbitrarias y no comparan riesgos reales. Un ajuste excelente no elimina errores de estructura, observación o extrapolación.',['investigación','reproducibilidad','IA','validación'])

catalog=OUT.parent.parent/'figures.json'
previous=json.loads(catalog.read_text(encoding='utf8')) if catalog.exists() else []
mechanisms=[f for f in previous if f.get('kind')=='mechanism' or f['id'].startswith(('g','h','q'))]
known={f['id']:f for f in previous}
if (ROOT/'book'/'edition.json').exists():
    META=[f for f in META if f['id']!='f02_calculo']
    for ext in ['png','svg']:
        removed=OUT/('f02_calculo.'+ext)
        if removed.exists():removed.unlink()
for f in META:
    f['kind']='model'
    if f['id'] in known:
        for field in ['chapters','refs','caption']:f[field]=known[f['id']].get(field,f.get(field))
catalog.write_text(json.dumps(META+mechanisms,ensure_ascii=False,indent=2),encoding='utf8')
print('Figuras originales:',len(META))
