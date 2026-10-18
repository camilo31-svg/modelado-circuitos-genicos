# Distribución de muestreo por Monte Carlo
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
rng=np.random.default_rng(13)
t=np.linspace(0,20,31)
estimaciones=[]
for i in range(100):
    datos=primer_orden(t,8,.4)+rng.normal(0,1,len(t))
    p,_=ajustar_primer_orden(t,datos)
    estimaciones.append(p)
estimaciones=np.array(estimaciones)
print('Cuantiles 2,5/50/97,5%:',np.quantile(estimaciones,[.025,.5,.975],axis=0))
plt.scatter(*estimaciones.T,s=12)
plt.xlabel('alfa (u.a./h)');plt.ylabel('delta (1/h)');plt.show()
