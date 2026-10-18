# La fluorescencia llega con retraso
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
t=np.linspace(0,40,401)
y=integrar(maduracion,[0,0],t)
plt.plot(t,y[0],label='Inmadura')
plt.plot(t,y[1],label='Madura (señal)')
plt.plot(t,y.sum(axis=0),'--',label='Total')
plt.xlabel('Tiempo (h)');plt.ylabel('Concentración (u.a.)')
plt.legend();plt.show()
print('Equilibrio esperado inmadura=10, madura=40')
