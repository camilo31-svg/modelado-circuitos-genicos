# ARN y proteína: dos escalas
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
y=integrar(gen,[0,0],t)
print('Estado final:',y[:,-1], 'Equilibrio: [4, 60]')
plt.plot(t,y[0],label='ARN');plt.plot(t,y[1],label='Proteína')
plt.xlabel('Tiempo (h)');plt.ylabel('Estado (u.a. de cada especie)')
plt.legend();plt.show()
