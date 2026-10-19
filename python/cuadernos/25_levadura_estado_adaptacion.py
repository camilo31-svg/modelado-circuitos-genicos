# Levadura: dos destinos y una respuesta que se adapta
# Fuentes: A01, A02, A25, A26, R05; números docentes originales.

# Localizar los módulos en python/, tanto como script como en Jupyter.
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


raices = cc.raices_autoactivacion(a=3, basal=.02)
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
plt.legend(); plt.show()


t = np.linspace(0, 20, 401)
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
plt.legend(); plt.show()


for fuga in [0, .1, .3]:
    equilibrio = cc.equilibrio_adaptacion(fuga=fuga)
    # Evaluar ambos balances debe devolver pendientes cero.
    np.testing.assert_allclose(cc.adaptacion(0,equilibrio,fuga=fuga),0,atol=1e-12)
    print('Fuga, respuesta residual, compensación:', fuga, *equilibrio)
