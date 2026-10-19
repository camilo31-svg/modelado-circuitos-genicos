# De una pendiente a un resultado comprobado
# Fuentes: A01, A02, A27, R05, R20, R21; números docentes originales.

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


def pendientes(t, estado, alfa, delta):
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
print('Forma especie/tiempo:', sol.y.shape)


exacta = cc.primer_orden(tiempos, alfa=12, delta=.3, x0=5)
error = np.abs(sol.y[0, :] - exacta)  # una discrepancia por tiempo
print('Máximo error absoluto (nM):', error.max())
np.testing.assert_allclose(sol.y[0], exacta, atol=1e-7, rtol=1e-7)
plt.plot(tiempos, sol.y[0], label='Integración')
plt.plot(tiempos, exacta, '--', label='Solución analítica')
plt.xlabel('Tiempo (h)'); plt.ylabel('Concentración (nM)')
plt.legend(); plt.show()


def dos_pendientes(estado):
    m, p = estado
    return np.array([4 - .5*m, 2*m - .2*p])

# Cada columna responde a cambiar una entrada, con las otras fijas.
analitico = np.array([[-.5, 0], [2, -.2]])
numerico = cc.diferencia_central(dos_pendientes, [3, 8], paso=1e-5)
print('Jacobiano calculado:', numerico)
np.testing.assert_allclose(numerico, analitico, atol=1e-8)
# Los autovalores de una matriz triangular son sus diagonales.
print('Tasas locales:', np.linalg.eigvals(analitico))
