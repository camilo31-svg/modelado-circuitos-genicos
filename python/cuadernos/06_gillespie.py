# Eventos y trayectorias discretas
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
for seed in [1,2,3]:
    t,x=ssa_nacimiento_muerte(seed=seed)
    plt.step(t,x,where='post',alpha=.7,label=f'semilla {seed}')
t=np.linspace(0,20,201)
plt.plot(t,primer_orden(t,5,.5),'k--',label='Media teórica')
plt.xlabel('Tiempo (h)');plt.ylabel('Moléculas')
plt.legend();plt.show()
