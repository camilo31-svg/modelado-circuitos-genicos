"""Cuadernos ejecutables y registro de prácticas para la edición 2.0."""
from pathlib import Path
import json,sys,textwrap,re
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists():ROOT=BASE
OUT=ROOT/'python'/'cuadernos';OUT.mkdir(exist_ok=True)
setup='''from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av
'''
LABS=[
('11_union','Unión molecular y raíz físicamente válida','reacciones',['A01'],
 'Resuelve la unión A+B⇌C con totales conservados. Compara integración con la raíz analítica y comprueba el dominio antes de interpretar un equilibrio. Las concentraciones se expresan en nM y el tiempo en horas.',
 '''t=np.linspace(0,3,151)
c=av.integrar(av.union,[0.],t,method='Radau')[0]
equilibrio=av.union_equilibrio()
print('Complejo en equilibrio:',equilibrio,'nM')
print('A libre, B libre:',10-equilibrio,8-equilibrio)
plt.plot(t,c,label='Complejo')
plt.axhline(equilibrio,color='black',ls='--',label='Raíz analítica')
plt.xlabel('Tiempo (h)');plt.ylabel('Complejo (nM)');plt.legend();plt.show()''',
 'La raíz válida es 10−√20≈5,528 nM. La otra raíz excede los totales. Cambia ambos totales y comprueba que C nunca supera el menor. Aumenta Kd sin cambiar los totales y predice el desplazamiento antes de integrar.'),
('12_bifurcaciones','Ramas estables e inestables de una autoactivación','bifurcaciones',['A01','A02'],
 'Construye el diagrama de equilibrios de x′=a x²/(1+x²)−x. La variable y el tiempo son adimensionales. Un barrido de trayectorias no muestra por sí solo las ramas inestables.',
 '''a=np.linspace(2,5,301)
low=(a-np.sqrt(a*a-4))/2;high=(a+np.sqrt(a*a-4))/2
plt.plot(a,high,label='Rama alta estable')
plt.plot(a,low,'--',label='Rama intermedia inestable')
plt.plot([0,5],[0,0],label='Origen estable')
plt.xlabel('a (adimensional)');plt.ylabel('Equilibrio x*');plt.legend();plt.show()
print('Raíces para a=2,5:',av.ramas_autoactivacion(2.5))
t=np.linspace(0,30,301)
for x0 in [.4,.6]:
    y=av.integrar(av.autoactivacion,[x0],t,args=(2.5,))
    plt.plot(t,y[0],label=f'x0={x0}')
plt.xlabel('Tiempo adimensional');plt.ylabel('x');plt.legend();plt.show()''',
 'Para a=2,5 hay raíces 0, 0,5 y 2. Los estados iniciales 0,4 y 0,6 tienen destinos diferentes. Añadir fuga cambia la estructura: no uses las mismas raíces analíticas después de añadirla.'),
('13_goodwin','Derivar y comprobar el umbral de Goodwin','c14',['A01'],
 'Compara relajación y oscilación en tres etapas con pérdidas iguales. El umbral analítico es un candidato de Hopf; la estabilidad de los ciclos necesita comprobarse. Todos los valores son adimensionales.',
 '''s,acrit,w=av.umbral_goodwin(10)
print('Equilibrio crítico, a crítico, frecuencia:',s,acrit,w)
print('Período lineal en el cruce:',2*np.pi/w)
t=np.linspace(0,120,2401)
for a in [4.,8.]:
    y=av.integrar(av.goodwin,[.1,.5,.7],t,args=(a,10.))
    plt.plot(t,y[0],label=f'a={a}')
plt.xlabel('Tiempo adimensional');plt.ylabel('Estado x');plt.legend();plt.show()''',
 'Para n=10, a crítico≈5,743. El equilibrio por debajo del cruce relaja; la trayectoria por encima debe evaluarse tras el transitorio. Aumenta la ventana y comprueba máximos consecutivos y tolerancias.'),
('14_control','Control antitético, perturbación y fuga','control',['A04','I09'],
 'Estudia [salida,z1,z2] en nM y tiempo en horas. La pérdida de salida cambia de 1 a 2 h⁻¹ en t=30 h. Integra por tramos para respetar la discontinuidad.',
 '''for fuga in [0.,.05]:
    t1=np.linspace(0,30,301);t2=np.linspace(30,90,601)
    y1=av.integrar(av.antitetico,[0,0,0],t1,
                    args=(2.,.5,1.,1.,1.,fuga),method='Radau')
    y2=av.integrar(av.antitetico,y1[:,-1],t2,
                    args=(2.,.5,1.,2.,1.,fuga),method='Radau')
    tt=np.r_[t1,t2[1:]];yy=np.c_[y1,y2[:,1:]]
    plt.plot(tt,yy[0],label=f'Dilución control={fuga}/h')
    print('Salida final, fuga:',yy[0,-1],fuga)
plt.axhline(4,color='black',ls='--',label='Referencia ideal')
plt.axvline(30,color='gray',ls=':')
plt.xlabel('Tiempo (h)');plt.ylabel('Salida (nM)');plt.legend();plt.show()''',
 'La referencia ideal es μ/θ=4 nM. La fuga añade −δc(z1−z2) a la identidad del integrador y puede producir error. Prueba actuación saturable con una capacidad insuficiente y explica por qué aumentar ganancia no crea capacidad.'),
('15_fases','Bloqueo y deriva entre dos osciladores','acoplados',['A01','A05'],
 'Utiliza períodos libres de 24 y 26 h. Las fases están en radianes. El modelo de fase supone acoplamiento débil y amplitudes relajadas; no es el modelo molecular del artículo de Danino.',
 '''t=np.linspace(0,1000,3001)
for K in [.005,.015]:
    phi=av.integrar(av.fases,[0,.2],t,args=(2*np.pi/24,2*np.pi/26,K))
    psi=phi[1]-phi[0]
    plt.plot(t,psi,label=f'K={K}/h')
    print('Cambio final de fase relativa:',K,psi[-1]-psi[-101])
plt.xlabel('Tiempo (h)');plt.ylabel('Fase relativa (rad)');plt.legend();plt.show()''',
 'La diferencia de frecuencias tiene magnitud≈0,02014/h. El acoplamiento simétrico permite bloqueo si 2K la supera. Reduce la diferencia de períodos y comprueba el cambio de frontera.'),
('16_momentos','Promotor telegráfico: media y varianza','c21',['A20','I02'],
 'Compara momentos analíticos y muestras independientes de SSA. Una cantidad de ARN es un entero; las muestras se toman en un tiempo regular final, no escogiendo estados por número de eventos.',
 '''t=np.array([0.,80.]);finales=[]
for seed in range(128):
    finales.append(av.telegr_ssa(t,seed=seed)[1,-1])
finales=np.array(finales)
media,var=av.momentos_telegr()
print('Analítica:',media,var)
print('Estimación Monte Carlo:',finales.mean(),finales.var(ddof=1))
plt.hist(finales,bins=np.arange(0,max(finales)+2)-.5,density=True)
plt.axvline(media,color='black',ls='--',label='Media analítica')
plt.xlabel('ARN (moléculas)');plt.ylabel('Frecuencia relativa');plt.legend();plt.show()''',
 'La media es 10 y la varianza 43,333 para las tasas por defecto. La estimación finita fluctúa. Aumenta el número de trayectorias y compara su error; cambia kon y koff por un mismo factor y observa qué momento permanece.'),
('17_sensibilidades','Sensibilidad, tiempo e información','sensibilidad',['A01','I06'],
 'Deriva sensibilidades del balance lineal y compáralas con diferencias centrales. α está en nM/h, δ en h⁻¹ y t en horas. El valor de una sensibilidad depende del tiempo y de su normalización.',
 '''t=np.linspace(.01,20,301);alpha=8.;delta=.4
S=av.sensibilidad_lineal(t,alpha,delta)
x=av.primer_orden(t,alpha,delta)
plt.plot(t,alpha*S[0]/x,label='Elasticidad a alfa')
plt.plot(t,delta*S[1]/x,label='Elasticidad a delta')
plt.xlabel('Tiempo (h)');plt.ylabel('Sensibilidad relativa');plt.legend();plt.show()
for h in [1e-2,1e-3,1e-4]:
    fd=(av.primer_orden(t,alpha,delta+h)-av.primer_orden(t,alpha,delta-h))/(2*h)
    print('Paso, error derivada:',h,np.max(np.abs(fd-S[1])))''',
 'La elasticidad a producción es uno. La de pérdida es pequeña al principio y tiende a −1. Los tiempos elegidos para estimar pérdida deben contener un transitorio informativo; puntos tempranos adicionales no sustituyen esa ventana.'),
('18_sensor','Calibración estática frente a dinámica de auxina','c26',['A01','P01','P02'],
 'El sensor docente parte de 10 nM y recibe una entrada de 5 unidades en t=0. No son parámetros calibrados de DII-VENUS ni del sensor luminiscente publicado. El tiempo es minutos.',
 '''t=np.linspace(0,30,301)
S=av.integrar(av.sensor,[10.],t)[0]
static=5*(10/S-1)
derivative=1-(.1+.02*5)*S
dynamic=(1-.1*S-derivative)/(.02*S)
plt.plot(t,static,label='Inversión estacionaria')
plt.plot(t,dynamic,label='Identidad dinámica sin ruido')
plt.axhline(5,color='black',ls='--',label='Entrada verdadera')
plt.xlabel('Tiempo (min)');plt.ylabel('Entrada estimada (u.a.)');plt.legend();plt.show()
print('Error inicial estático:',static[0]-5)''',
 'La inversión estática al comienzo da cero aunque la entrada ya sea cinco. La identidad dinámica recupera cinco con derivadas exactas. Añade ruido a S y estima una derivada numérica para observar amplificación; no confundas exactitud algebraica con inferencia fiable.'),
('19_turing','Estabilidad homogénea y modos espaciales','c18',['A01','D11'],
 'Analiza un Jacobiano abstracto estable sin difusión y una difusión desigual. Las curvas son tasas lineales de crecimiento de perturbaciones; no son concentraciones vegetales ni un patrón no lineal final.',
 '''k=np.linspace(0,1.3,401)
plt.plot(k,av.dispersion_turing(k),label='D=(1,20)')
plt.plot(k,av.dispersion_turing(k,D=(1,1)),label='D=(1,1)')
plt.axhline(0,color='black',ls='--')
plt.xlabel('Número de onda (1/longitud)')
plt.ylabel('Máxima parte real (1/tiempo)');plt.legend();plt.show()
unstable=k[av.dispersion_turing(k)>0]
print('Intervalo aproximado inestable:',unstable[0],unstable[-1])''',
 'El Jacobiano tiene traza −2 y determinante 1. Con difusión desigual existe un intervalo inestable; con difusión igual, los modos se estabilizan. Un dominio finito solo permite ciertos números de onda: comprueba si alguno cae dentro del intervalo.'),
('20_fosforilacion','Nueve especies y tres conservaciones','cascadas',['A01','A16'],
 'Construye una red abstracta de modificación doble distributiva, con dos enzimas compartidas. Las cantidades son unidades arbitrarias y el tiempo es una unidad coherente con las constantes. No se utilizan las tasas publicadas de Markevich.',
 '''N,L=av.fosforilacion_red()
print('Conservaciones L@N:',np.max(np.abs(L@N)))
y0=np.array([10,0,0,2,1,0,0,0,0],float)
t=np.linspace(0,80,401)
y=av.integrar(av.fosforilacion,y0,t,method='Radau')
for i,label in enumerate(['X0 libre','X1 libre','X2 libre']):
    plt.plot(t,y[i],label=label)
plt.xlabel('Tiempo (u.a.)');plt.ylabel('Cantidad (u.a.)');plt.legend();plt.show()
print('Totales iniciales:',L@y0)
print('Máxima desviación de totales:',np.max(np.abs(L@y-(L@y0)[:,None])))''',
 'Se conservan enzima E, enzima F y unidades de sustrato. Los complejos deben incluirse en los totales. Esta práctica verifica balance; no afirma que las tasas por defecto produzcan biestabilidad.'),
('21_seis_genes','Dos anillos acoplados: seis proteínas','acoplados',['A01','A06'],
 'Integra seis balances adimensionales con represión cruzada. El ejemplo explora la interacción de módulos; no reproduce parámetros ni figuras del estudio teórico de 2025/2026.',
 '''t=np.linspace(0,180,3601)
for kappa in [0.,.1]:
    y=av.integrar(av.anillos_acoplados,[.1,2,5,2,.1,5],t,
                    args=(30.,3.,kappa))
    fig,ax=plt.subplots(2,1)
    ax[0].plot(t,y[0],label='X1');ax[0].plot(t,y[3],label='Y1')
    ax[0].set_xlabel('Tiempo adimensional')
    ax[0].set_ylabel('Proteínas (u.a.)');ax[0].legend()
    ax[1].plot(y[0,-1500:],y[3,-1500:])
    ax[1].set_xlabel('X1 (u.a.)');ax[1].set_ylabel('Y1 (u.a.)')
    fig.suptitle(f'Acoplamiento kappa={kappa}');plt.show()
    print('Rango final X1:',kappa,np.ptp(y[0,-1000:]))''',
 'Describe el régimen observado con criterios de período, fase y amplitud. Una curva cerrada en una proyección no demuestra por sí sola el período de todo el estado. Repite tolerancias y ventana antes de proponer un régimen complejo.'),
('22_perfiles','Perfil de verosimilitud y diseño temporal','c24',['I06','A09','A10'],
 'Compara un registro transitorio y otro casi estacionario con la misma verdad α=8 nM/h y δ=0,4 h⁻¹. En cada valor de α se reoptimiza δ. Los datos son sintéticos con semilla registrada.',
 '''rng=np.random.default_rng(26);sigma=1.;alfas=np.linspace(3,16,100)
for t,label in [(np.linspace(0,15,25),'Transitorio'),
                 (np.linspace(40,55,25),'Casi equilibrio')]:
    datos=av.primer_orden(t,8,.4)+rng.normal(0,sigma,len(t))
    obj,delta=av.perfiles_lineales(t,datos,sigma,alfas)
    plt.plot(alfas,obj-obj.min(),label=label)
plt.ylim(0,30);plt.xlabel('alfa fijada (nM/h)')
plt.ylabel('Aumento de chi² tras reoptimizar');plt.legend();plt.show()''',
 'En el registro tardío, muchas parejas conservan α/δ≈20 y el perfil puede quedar amplio. El transitorio aporta información de forma. No congeles δ al construir el perfil: esa curva sería una sección del objetivo y no un perfil reoptimizado.')
]

refs={r['id']:r for r in json.loads((ROOT/'book'/'references.json').read_text(encoding='utf8'))}
chapters={c['id']:c for c in json.loads((ROOT/'book'/'chapters.json').read_text(encoding='utf8'))}
for slug,title,chapter,sources,intro,src,solution in LABS:
    src=textwrap.dedent(src).strip()+'\n'
    source_line='Fuentes de los principios: '+', '.join('['+key+']('+refs[key]['url']+')' for key in sources)+'.'
    cells=[]
    for kind,text in [('markdown','# '+title+'\n\n'+intro+'\n\nLección '+chapters[chapter]['number']+': '+chapters[chapter]['title']+'.\n\n'+source_line),('markdown','## Predice antes de ejecutar\nIdentifica estados, parámetros, unidades y una propiedad que puedas comprobar. Los parámetros son docentes y los resultados no se atribuyen a datos de artículos.'),('code',setup),('code',src),('markdown','## Solución y ampliación\n'+solution),('markdown','## Registro del análisis\nAnota solver, tolerancias, entradas, condiciones iniciales, resultado y una limitación. Si cambias una ecuación, vuelve a comprobar balance y dominio.')]:
        cell={'cell_type':kind,'metadata':{},'source':text.splitlines(True),'id':slug+'-'+str(len(cells))}
        if kind=='code':cell.update(outputs=[],execution_count=None)
        cells.append(cell)
    nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':sys.version.split()[0]}},'nbformat':4,'nbformat_minor':5}
    (OUT/(slug+'.ipynb')).write_text(json.dumps(nb,ensure_ascii=False,indent=2),encoding='utf8')
    (OUT/(slug+'.py')).write_text('# '+title+'\n# Modelos y números docentes originales. Fuentes: '+', '.join(sources)+'\n'+setup+'\n'+src,encoding='utf8')
# El registro se obtiene de los cuadernos para mantener títulos y archivos sincronizados.
registry=[]
first_info={
 '01_python':(['edo','c08'],['A01','A21','A23']),
 '02_balances':(['edo','c09'],['A01','R05']),
 '03_hill':(['c16'],['A01','D07']),
 '04_toggle':(['c11','c13'],['A01','D01']),
 '05_oscilador':(['c14'],['A01','D02']),
 '06_gillespie':(['c20','c21'],['I02','I03']),
 '07_ajuste':(['c22','c23','c24'],['I05','I06','A09']),
 '08_plantas':(['c18','c25','c26','c27'],['A01','P03','P04']),
 '09_incertidumbre':(['c23','c24'],['A09','I06']),
 '10_reportero':(['c22','c26'],['I04','P01']),
}
for p in sorted(OUT.glob('*.ipynb')):
    nb=json.loads(p.read_text(encoding='utf8'));text=''.join(nb['cells'][0]['source'])
    if p.stem in first_info:
        lines=[x for x in text.splitlines() if x.strip()]
        intro=lines[1]
        intro=re.sub(r'(?:Capítulos?|Lecciones?)\s+(?:c\d\d|edo)[^.]*\.','',intro)
        if p.stem=='01_python':intro='Aprende a ejecutar celdas, usar arrays y etiquetar ejes. Los valores son inventados para aprender. Predice primero: ¿qué ocurre al duplicar la producción?'
        if p.stem=='02_balances':intro='Integra dos balances, compara estados y revisa unidades. Alfa: u.a. ARN/h; dm: 1/h; beta: u.a. proteína/(u.a. ARN h); dp: 1/h.'
        intro=' '.join(intro.split())
        lesson_ids,sources=first_info[p.stem]
        source_line='Fuentes de los principios: '+', '.join('['+key+']('+refs[key]['url']+')' for key in sources)+'.'
        text=lines[0]+'\n\n'+intro+'\n\nLecciones relacionadas: '+', '.join(chapters[key]['number']+' · '+chapters[key]['title'] for key in lesson_ids)+'.\n\n'+source_line
    else:
        spec=next((l for l in LABS if l[0]==p.stem),None)
        if spec:lesson_ids,sources=[spec[2]],spec[3]
        else:lesson_ids,sources=nb['metadata']['atlas']['lessons'],nb['metadata']['atlas']['sources']
    nb['cells'][0]['source']=text.splitlines(True)
    (p).write_text(json.dumps(nb,ensure_ascii=False,indent=2),encoding='utf8')
    lines=[x for x in text.splitlines() if x.strip()]
    registry.append([p.stem,lines[0].lstrip('# '),lines[1] if len(lines)>1 else 'Modelo docente con comprobación y explicación.',sources,lesson_ids])
(ROOT/'docs'/'labs.json').write_text(json.dumps(registry,ensure_ascii=False),encoding='utf8')
print('Prácticas ejecutables:',len(registry))
