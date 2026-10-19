"""Tres prácticas con derivación, comentarios y comprobación independiente."""
from pathlib import Path
import json,sys,textwrap
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'outputs'/'atlas-circuitos-genicos'
if not ROOT.exists():ROOT=BASE
OUT=ROOT/'python'/'cuadernos'
setup='''# Localizar los módulos en python/, tanto como script como en Jupyter.
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_casos.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
# NumPy organiza vectores; SciPy integra; Matplotlib dibuja resultados.
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import circuitos_casos as cc
'''
specs=[
 ('23_codigo_paso_a_paso','De una pendiente a un resultado comprobado',['edo','c08','c11'],['A01','A02','A27','R05','R20','R21'],
  'Lee el flujo completo de un programa: entradas, función, integración, forma del resultado y verificación. Después compara un Jacobiano analítico con diferencias centrales.',
  [('Definir el balance y nombrar cada término',
   '''def pendientes(t, estado, alfa, delta):
    x = estado[0]             # una concentración en nM
    produccion = alfa        # nM/h; independiente del estado
    perdida = delta * x      # nM/h; aumenta con x
    return np.array([produccion - perdida])

tiempos = np.linspace(0, 20, 201)  # 201 salidas, separadas 0,1 h
inicial = [5.0]                   # el vector tiene una componente
parametros = (12.0, 0.3)          # orden: alfa, delta
sol = solve_ivp(pendientes, (0, 20), inicial, args=parametros,
                t_eval=tiempos, rtol=1e-9, atol=1e-11)
if not sol.success:
    raise RuntimeError(sol.message)
print('Forma especie/tiempo:', sol.y.shape)'''),
   ('Comparar con una solución obtenida por integración algebraica',
    '''exacta = cc.primer_orden(tiempos, alfa=12, delta=.3, x0=5)
error = np.abs(sol.y[0, :] - exacta)  # una discrepancia por tiempo
print('Máximo error absoluto (nM):', error.max())
np.testing.assert_allclose(sol.y[0], exacta, atol=1e-7, rtol=1e-7)
plt.plot(tiempos, sol.y[0], label='Integración')
plt.plot(tiempos, exacta, '--', label='Solución analítica')
plt.xlabel('Tiempo (h)'); plt.ylabel('Concentración (nM)')
plt.legend(); plt.show()'''),
   ('Construir columnas de derivadas moviendo una variable cada vez',
    '''def dos_pendientes(estado):
    m, p = estado
    return np.array([4 - .5*m, 2*m - .2*p])

# Cada columna responde a cambiar una entrada, con las otras fijas.
analitico = np.array([[-.5, 0], [2, -.2]])
numerico = cc.diferencia_central(dos_pendientes, [3, 8], paso=1e-5)
print('Jacobiano calculado:', numerico)
np.testing.assert_allclose(numerico, analitico, atol=1e-8)
# Los autovalores de una matriz triangular son sus diagonales.
print('Tasas locales:', np.linalg.eigvals(analitico))''')],
  'Explica por qué 201 tiempos no significan 201 pasos internos. Intercambia alfa y delta, observa que Python puede ejecutarlo y localiza el error de unidades. Deriva las cuatro entradas del Jacobiano antes de ejecutar la última celda.'),
 ('24_represilador_completo','Seis EDO bacterianas: escalas y código',['caso-bacteriano','c14'],['A01','D02','A27','R05','R21'],
  'Integra el anillo de tres ARN y tres proteínas, explica cada índice y verifica que las ecuaciones con unidades y normalizadas describen la misma trayectoria docente.',
  [('Escribir el mecanismo y conservar el orden del vector',
   '''def circuito(t, estado, alfa, basal, beta, n):
    m = estado[:3]                  # m0, m1, m2
    p = estado[3:]                  # p0, p1, p2
    represores = p[[2, 0, 1]]       # p2->m0, p0->m1, p1->m2
    actividad = 1 / (1 + represores**n)
    dm = basal + alfa*actividad - m # tres balances de ARN
    dp = beta*(m - p)               # tres balances proteicos
    return np.concatenate([dm, dp]) # seis tasas, mismo orden

inicial = np.array([.1, .2, .3, 1, 2, 3])
tau = np.linspace(0, 300, 1501)
sol = solve_ivp(circuito, (0, 300), inicial,
                args=(60, .01, .2, 2), t_eval=tau,
                rtol=1e-9, atol=1e-11)
if not sol.success:
    raise RuntimeError(sol.message)
for i in range(3):
    plt.plot(tau, sol.y[3+i], label=f'p{i}')
plt.xlabel('Tiempo normalizado tau'); plt.ylabel('Proteína / K')
plt.legend(); plt.show()'''),
   ('Volver a horas y concentraciones, con el mismo experimento matemático',
    '''# gm=.5/h, gp=.1/h, K=10 nM, kt=2/h; parámetros docentes.
gm = .5
inicial_dim = cc.a_dimensional(inicial)
horas = tau / gm
dim = solve_ivp(cc.represilador_dimensional, (0, horas[-1]),
                inicial_dim, t_eval=horas, rtol=1e-10, atol=1e-12)
if not dim.success:
    raise RuntimeError(dim.message)
normalizada = cc.a_normalizado(dim.y)
print('Diferencia máxima entre versiones:', np.max(np.abs(sol.y-normalizada)))
np.testing.assert_allclose(sol.y, normalizada, rtol=2e-5, atol=2e-5)'''),
   ('Contrastar el Jacobiano y el polinomio de seis estados',
    '''s = cc.equilibrio_represilador()
equilibrio = np.full(6, s)
J = cc.jacobiano_represilador(equilibrio)
J_fd = cc.diferencia_central(lambda z: circuito(0,z,60,.01,.2,2), equilibrio)
np.testing.assert_allclose(J, J_fd, atol=1e-7)
valores = np.linalg.eigvals(J)
g = 60*2*s/(1+s*s)**2
residuo = ((valores+1)*(valores+.2))**3 + (.2*g)**3
print('Equilibrio simétrico:', s)
print('Partes reales:', valores.real)
np.testing.assert_allclose(residuo, 0, atol=1e-10)''')],
  'Duplica gm en la versión dimensional. Deriva primero cómo cambian alfa, basal, beta y la conversión de tiempo. No cambies solo el eje horizontal. Compara el equilibrio con las oscilaciones y explica por qué una condición inicial perfectamente simétrica merece atención.'),
 ('25_levadura_estado_adaptacion','Levadura: dos destinos y una respuesta que se adapta',['caso-levadura','control'],['A01','A02','A25','A26','R05'],
  'Compara un modelo docente de autoactivación con una analogía local de control. Los estados y parámetros de ambas simulaciones se definen por separado; no son ajustes a los artículos.',
  [('Encontrar y clasificar equilibrios, sin inferirlos a ojo',
   '''raices = cc.raices_autoactivacion(a=3, basal=.02)
pendientes = cc.pendiente_autoactivacion(raices, a=3)
print('Equilibrios:', raices)
print('Derivadas locales:', pendientes)
np.testing.assert_allclose(cc.autoactivacion(0,raices,3,.02),0,atol=1e-12)
t = np.linspace(0, 25, 501)
for x0 in [.1, .8]:
    sol = solve_ivp(cc.autoactivacion, (0,25), [x0], t_eval=t,
                   args=(3,.02,2), rtol=1e-9, atol=1e-11)
    if not sol.success:
        raise RuntimeError(sol.message)
    plt.plot(t, sol.y[0], label=f'x inicial={x0}')
plt.xlabel('Tiempo normalizado'); plt.ylabel('Activador normalizado')
plt.legend(); plt.show()'''),
   ('Comprobar la analogía de adaptación con una solución exacta',
    '''t = np.linspace(0, 20, 401)
sol = solve_ivp(cc.adaptacion, (0,20), [0,0], t_eval=t,
                rtol=1e-10, atol=1e-12)
if not sol.success:
    raise RuntimeError(sol.message)
exacta = cc.adaptacion_exacta(t)
np.testing.assert_allclose(sol.y, exacta, rtol=2e-8, atol=2e-10)
plt.plot(t, sol.y[0], label='Desviación h')
plt.plot(t, sol.y[1], label='Compensación g')
plt.plot(t, exacta[0], '--', label='h analítica')
plt.xlabel('Tiempo docente'); plt.ylabel('Estado en escala normalizada')
plt.legend(); plt.show()'''),
   ('Añadir fuga y comprobar qué igualdad deja de cumplirse',
    '''for fuga in [0, .1, .3]:
    equilibrio = cc.equilibrio_adaptacion(fuga=fuga)
    # Evaluar ambos balances debe devolver pendientes cero.
    np.testing.assert_allclose(cc.adaptacion(0,equilibrio,fuga=fuga),0,atol=1e-12)
    print('Fuga, respuesta residual, compensación:', fuga, *equilibrio)''')],
  'Deriva el polinomio lambda^2+b*lambda+a*c y comprueba sus autovalores. Explica por qué h puede ser negativa en una analogía de desviaciones, mientras que la concentración del activador del primer modelo debe permanecer no negativa. No confundas bimodalidad observada y dos raíces estables deterministas.')
]
refs={r['id']:r for r in json.loads((ROOT/'book'/'references.json').read_text(encoding='utf8'))}
chapters={c['id']:c for c in json.loads((ROOT/'book'/'chapters.json').read_text(encoding='utf8'))}
for slug,title,lessons,sources,intro,blocks,exercise in specs:
    cells=[]
    def cell(kind,text):
        value={'cell_type':kind,'source':text.splitlines(True),'metadata':{},'id':slug+'-'+str(len(cells))}
        if kind=='code':value.update(outputs=[],execution_count=None)
        cells.append(value)
    source_line='Fuentes: '+', '.join('['+key+']('+refs[key]['url']+')' for key in sources)+'.'
    lesson_line='Lecciones: '+', '.join(chapters[key]['number']+' · '+chapters[key]['title'] for key in lessons)+'.'
    cell('markdown','# '+title+'\n\n'+intro+'\n\n'+lesson_line+'\n\n'+source_line)
    cell('markdown','## Preparación\nEl primer bloque localiza los módulos del paquete. `__file__` existe al ejecutar un script; en Jupyter se utiliza la carpeta actual. `sys.path.insert` permite importar el módulo de modelos. Ejecuta desde `python/cuadernos/` o desde `python/`. Lee los comentarios antes de cada llamada.')
    cell('code',setup)
    scripts=[setup]
    for heading,code in blocks:
        cell('markdown','## '+heading+'\nAntes de ejecutar, identifica qué entra, qué sale y las unidades. El capítulo correspondiente deriva las fórmulas que se están comprobando.\n\n'+source_line)
        code=textwrap.dedent(code).strip()+'\n';cell('code',code);scripts.append(code)
    cell('markdown','## Comprueba con tus palabras\n'+exercise+'\n\nLos `assert_allclose` comparan consecuencias analíticas o implementaciones equivalentes; no validan experimentalmente las hipótesis.')
    nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':sys.version.split()[0]},'atlas':{'lessons':lessons,'sources':sources}},'nbformat':4,'nbformat_minor':5}
    (OUT/(slug+'.ipynb')).write_text(json.dumps(nb,ensure_ascii=False,indent=2),encoding='utf8')
    (OUT/(slug+'.py')).write_text('# '+title+'\n# Fuentes: '+', '.join(sources)+'; números docentes originales.\n\n'+'\n\n'.join(scripts),encoding='utf8')
# Registro de 25 prácticas con los campos estables de la app.
p=ROOT/'docs'/'labs.json';registry=json.loads(p.read_text(encoding='utf8'));byid={x[0]:x for x in registry}
for slug,title,lessons,sources,intro,_,_ in specs:byid[slug]=[slug,title,intro,sources,lessons]
p.write_text(json.dumps([byid[key] for key in sorted(byid)],ensure_ascii=False),encoding='utf8')
print('Casos comentados:',len(specs),'Prácticas totales:',len(byid))
