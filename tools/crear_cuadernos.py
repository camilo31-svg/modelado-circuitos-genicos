import json, textwrap, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists():ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'python'/'cuadernos';out.mkdir(parents=True,exist_ok=True)
def md(s):return dict(cell_type='markdown',metadata={},source=textwrap.dedent(s).strip().splitlines(True))
def code(s):return dict(cell_type='code',metadata={},source=textwrap.dedent(s).strip().splitlines(True),outputs=[],execution_count=None)
setup="""from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
from circuitos import *
"""
labs=[
('01_python','Python y tu primera curva',
'''Aprende a ejecutar celdas, usar arrays y etiquetar ejes. Los valores son inventados para aprender. Predice primero: ¿qué ocurre al duplicar la producción? Lecciones de EDO y programación. La numeración visible se consulta en la app; los identificadores internos se conservan al revisar contenidos.''',
'''tiempo = np.linspace(0, 20, 101)
proteina = primer_orden(tiempo, alfa=4, delta=.4)
print('Equilibrio esperado:', 4/.4)
plt.plot(tiempo, proteina, label='alfa=4')
plt.plot(tiempo, primer_orden(tiempo,8,.4), label='alfa=8')
plt.xlabel('Tiempo (h)'); plt.ylabel('Concentración (u.a.)')
plt.legend(); plt.show()''',
'''Prueba alfa=0 y x0=10. Solución: la curva decae exponencialmente; con alfa=8 el equilibrio es 20 y el tiempo característico sigue siendo 2,5 h. Comprueba que no has cambiado delta al cambiar alfa.'''),
('02_balances','ARN y proteína: dos escalas',
'''Integra dos balances, compara estados y revisa unidades. Alfa: u.a. ARN/h; dm: 1/h; beta: u.a. proteína/(u.a. ARN h); dp: 1/h. Lecciones edo y c09.''',
'''t=np.linspace(0,40,401)
y=integrar(gen,[0,0],t)
print('Estado final:',y[:,-1], 'Equilibrio: [4, 60]')
plt.plot(t,y[0],label='ARN');plt.plot(t,y[1],label='Proteína')
plt.xlabel('Tiempo (h)');plt.ylabel('Estado (u.a. de cada especie)')
plt.legend();plt.show()''',
'''¿Por qué empieza la proteína con pendiente cero? Porque beta*m(0)=0 y p(0)=0. Al duplicar dp, el equilibrio proteico se reduce a 30; el del ARN permanece en 4. No compares unidades de ARN y proteína como si fueran idénticas.'''),
('03_hill','Regular no equivale a un interruptor',
'''Explora K y n, separa umbral y pendiente. Capítulo c16. Esta familia fenomenológica no demuestra un mecanismo molecular concreto.''',
'''x=np.linspace(0,5,301)
for n in [1,2,4]:
    plt.plot(x,hill(x,K=1,n=n),label=f'n={n}')
print('f(K)=',hill(1,K=1,n=4))
plt.xlabel('Entrada / K (adimensional)');plt.ylabel('Fracción activada')
plt.legend();plt.show()''',
'''Solución: las tres curvas cruzan 0,5 en x=K. Un n alto hace más pronunciada la transición, pero no crea por sí solo memoria ni bistabilidad. Es necesario cerrar un circuito y analizar su dinámica.'''),
('04_toggle','Dos estados y sus cuencas',
'''Modelo reducido adimensional, original y distinto de una calibración del artículo. Capítulos c11–c13.''',
'''t=np.linspace(0,30,601)
for inicio in ([9,.1],[.1,9],[3,2.9]):
    y=integrar(toggle,inicio,t)
    print(inicio,'->',y[:,-1].round(3))
    plt.plot(y[0],y[1],label=str(inicio))
plt.xlabel('x (adimensional)');plt.ylabel('z (adimensional)')
plt.legend();plt.show()''',
'''Solución: condiciones iniciales opuestas alcanzan estados opuestos. La trayectoria exactamente simétrica puede quedarse en una variedad especial; no demuestra ausencia de otros equilibrios. Cambia alfa a 1 y vuelve a analizar.'''),
('05_oscilador','Oscilar y comprobarlo',
'''Modelo mínimo de proteínas, tiempo adimensional. Capítulo c14. Compara amplitud al final y al principio y repite con tolerancias más estrictas.''',
'''t=np.linspace(0,120,2401)
y=integrar(represilador,[.1,2,5],t)
for j in range(3):plt.plot(t,y[j],label=f'Proteína {j+1}')
print('Amplitud final:',np.ptp(y[0,-600:]))
plt.xlabel('Tiempo (adimensional)');plt.ylabel('Estado / K')
plt.legend();plt.show()''',
'''Solución: con estos parámetros hay oscilaciones persistentes. Cambia n a 1 manteniendo alfa=30 y analiza la amortiguación. Una línea ondulada durante un transitorio no demuestra un ciclo límite.'''),
('06_gillespie','Eventos y trayectorias discretas',
'''Capítulos c19–c21. Alfa=5 moléculas/h y delta=0,5/h. Cada salto cambia una molécula. No confundir SSA con añadir ruido independiente a una EDO.''',
'''for seed in [1,2,3]:
    t,x=ssa_nacimiento_muerte(seed=seed)
    plt.step(t,x,where='post',alpha=.7,label=f'semilla {seed}')
t=np.linspace(0,20,201)
plt.plot(t,primer_orden(t,5,.5),'k--',label='Media teórica')
plt.xlabel('Tiempo (h)');plt.ylabel('Moléculas')
plt.legend();plt.show()''',
'''Calcula 500 estados finales. Solución: su media estará cerca de 10 y su varianza también, con fluctuación de muestreo. Una sola trayectoria no representa la media ni el histograma estacionario.'''),
('07_ajuste','Estimar con datos sintéticos explícitos',
'''Capítulos c22–c24. Datos generados, no observaciones de un artículo. x0=0 y sigma=1 conocidos; los errores son gaussianos independientes. No confundir recuperar parámetros simulados con validación experimental.''',
'''rng=np.random.default_rng(2026)
t=np.linspace(0,20,31)
observado=primer_orden(t,8,.4)+rng.normal(0,1,len(t))
theta,fit=ajustar_primer_orden(t,observado)
print('alfa, delta ajustados:',theta)
pred=primer_orden(t,*theta)
fig,ax=plt.subplots(1,2,figsize=(10,3.5))
ax[0].scatter(t,observado,label='Datos sintéticos')
ax[0].plot(t,pred,label='Ajuste');ax[0].legend()
ax[0].set(xlabel='Tiempo (h)',ylabel='Concentración (u.a.)')
ax[1].scatter(t,observado-pred);ax[1].axhline(0,color='k')
ax[1].set(xlabel='Tiempo (h)',ylabel='Residuo (u.a.)')
plt.tight_layout();plt.show()''',
'''Repite con datos solo del equilibrio: muchas parejas alfa/delta describen la misma salida. Solución: medir el transitorio añade información sobre delta. Mira los residuos; un buen ajuste visual no prueba un mecanismo.'''),
('08_plantas','Tejido en una cadena de células',
'''Capítulos c18 y c25–c27. Modelo conceptual: células iguales, intercambio simétrico, fronteras sin flujo, producción localizada. No es un modelo calibrado de auxina ni de raíces del artículo.''',
'''N=30
s=np.zeros(N);s[3:7]=3
t=np.linspace(0,30,301)
y=integrar(tejido,np.zeros(N),t,args=(s,))
plt.imshow(y,aspect='auto',origin='lower',extent=[0,30,0,N],cmap='viridis')
plt.colorbar(label='Concentración (u.a.)')
plt.xlabel('Tiempo (h)');plt.ylabel('Índice de célula')
plt.show()
print('Suma intercambio:',sum(tejido(0,y[:,-1],np.zeros(N),delta=0)))''',
'''Duplica intercambio. La distribución se ensancha. Solución de conservación: con producción y pérdida desactivadas, la suma de estados permanece constante. Si los volúmenes difieren, hay que conservar cantidades, no sumar concentraciones.'''),
('09_incertidumbre','Distribución de muestreo por Monte Carlo',
'''Capítulos c23–c24. Simula el procedimiento bajo un modelo supuesto; no incorpora automáticamente incertidumbre estructural. Guarda semilla, número de réplicas y fracasos.''',
'''rng=np.random.default_rng(13)
t=np.linspace(0,20,31)
estimaciones=[]
for i in range(100):
    datos=primer_orden(t,8,.4)+rng.normal(0,1,len(t))
    p,_=ajustar_primer_orden(t,datos)
    estimaciones.append(p)
estimaciones=np.array(estimaciones)
print('Cuantiles 2,5/50/97,5%:',np.quantile(estimaciones,[.025,.5,.975],axis=0))
plt.scatter(*estimaciones.T,s=12)
plt.xlabel('alfa (u.a./h)');plt.ylabel('delta (1/h)');plt.show()''',
'''Solución: los parámetros pueden estar correlacionados aun si el ajuste es bueno. Estos cuantiles describen el procedimiento con verdad conocida; para un bootstrap ajustado a tus datos, simula desde sus parámetros estimados y respeta su modelo de error.'''),
('10_reportero','La fluorescencia llega con retraso',
'''Capítulo c22 y aplicaciones vegetales. Producción 5 u.a./h; maduración 0,4/h; pérdida 0,1/h. La señal es proporcional solo a proteína madura en este ejemplo.''',
'''t=np.linspace(0,40,401)
y=integrar(maduracion,[0,0],t)
plt.plot(t,y[0],label='Inmadura')
plt.plot(t,y[1],label='Madura (señal)')
plt.plot(t,y.sum(axis=0),'--',label='Total')
plt.xlabel('Tiempo (h)');plt.ylabel('Concentración (u.a.)')
plt.legend();plt.show()
print('Equilibrio esperado inmadura=10, madura=40')''',
'''Solución: total=50 en equilibrio; solo el 80% es madura con estos parámetros. Ignorar maduración confunde tiempo de respuesta del circuito con tiempo de respuesta del instrumento. Añade un fondo aditivo antes de comparar señales.''')]
for slug,title,intro,src,sol in labs:
    cells=[md('# '+title+'\n\n'+intro),md('## Preparación\nEjecuta desde esta carpeta o desde `python/`. Instala las dependencias siguiendo el README.'),code(setup),code(src),md('## Comprueba y cambia\n'+sol),md('## Diario de modelado\nEscribe la pregunta, unidades, hipótesis, predicción anterior a ejecutar, resultado y una limitación. Guarda tus cambios en otra copia.')]
    for i,cell in enumerate(cells):cell['id']=slug+'-'+str(i)
    nb=dict(cells=cells,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python',version=sys.version.split()[0])),nbformat=4,nbformat_minor=5)
    (out/(slug+'.ipynb')).write_text(json.dumps(nb,ensure_ascii=False,indent=2),encoding='utf8')
    (out/(slug+'.py')).write_text('# '+title+'\n# Datos y parámetros didácticos originales.\n'+textwrap.dedent(setup)+textwrap.dedent(src)+'\n',encoding='utf8')
print('Cuadernos y scripts:',len(labs))
