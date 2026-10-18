# Regular no equivale a un interruptor
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
x=np.linspace(0,5,301)
for n in [1,2,4]:
    plt.plot(x,hill(x,K=1,n=n),label=f'n={n}')
print('f(K)=',hill(1,K=1,n=4))
plt.xlabel('Entrada / K (adimensional)');plt.ylabel('Fracción activada')
plt.legend();plt.show()
