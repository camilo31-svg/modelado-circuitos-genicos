# Dos estados y sus cuencas
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
t=np.linspace(0,30,601)
for inicio in ([9,.1],[.1,9],[3,2.9]):
    y=integrar(toggle,inicio,t)
    print(inicio,'->',y[:,-1].round(3))
    plt.plot(y[0],y[1],label=str(inicio))
plt.xlabel('x (adimensional)');plt.ylabel('z (adimensional)')
plt.legend();plt.show()
