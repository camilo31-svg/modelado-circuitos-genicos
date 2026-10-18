# Python y tu primera curva
# Datos y parámetros didácticos originales.
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
from circuitos import *
tiempo = np.linspace(0, 20, 101)
proteina = primer_orden(tiempo, alfa=4, delta=.4)
print('Equilibrio esperado:', 4/.4)
plt.plot(tiempo, proteina, label='alfa=4')
plt.plot(tiempo, primer_orden(tiempo,8,.4), label='alfa=8')
plt.xlabel('Tiempo (h)'); plt.ylabel('Concentración (u.a.)')
plt.legend(); plt.show()
