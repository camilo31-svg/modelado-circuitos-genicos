# Oscilar y comprobarlo
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
t=np.linspace(0,120,2401)
y=integrar(represilador,[.1,2,5],t)
for j in range(3):plt.plot(t,y[j],label=f'Proteína {j+1}')
print('Amplitud final:',np.ptp(y[0,-600:]))
plt.xlabel('Tiempo (adimensional)');plt.ylabel('Estado / K')
plt.legend();plt.show()
