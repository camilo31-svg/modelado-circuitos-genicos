# Seis EDO bacterianas: escalas y código
# Fuentes: A01, D02, A27, R05, R21; números docentes originales.

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


def circuito(t, estado, alfa, basal, beta, n):
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
plt.legend(); plt.show()


# gm=.5/h, gp=.1/h, K=10 nM, kt=2/h; parámetros docentes.
gm = .5
inicial_dim = cc.a_dimensional(inicial)
horas = tau / gm
dim = solve_ivp(cc.represilador_dimensional, (0, horas[-1]),
                inicial_dim, t_eval=horas, rtol=1e-10, atol=1e-12)
if not dim.success:
    raise RuntimeError(dim.message)
normalizada = cc.a_normalizado(dim.y)
print('Diferencia máxima entre versiones:', np.max(np.abs(sol.y-normalizada)))
np.testing.assert_allclose(sol.y, normalizada, rtol=2e-5, atol=2e-5)


s = cc.equilibrio_represilador()
equilibrio = np.full(6, s)
J = cc.jacobiano_represilador(equilibrio)
J_fd = cc.diferencia_central(lambda z: circuito(0,z,60,.01,.2,2), equilibrio)
np.testing.assert_allclose(J, J_fd, atol=1e-7)
valores = np.linalg.eigvals(J)
g = 60*2*s/(1+s*s)**2
residuo = ((valores+1)*(valores+.2))**3 + (.2*g)**3
print('Equilibrio simétrico:', s)
print('Partes reales:', valores.real)
np.testing.assert_allclose(residuo, 0, atol=1e-10)
