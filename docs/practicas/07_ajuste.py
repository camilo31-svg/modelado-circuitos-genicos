# Estimar con datos sintéticos explícitos
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
rng=np.random.default_rng(2026)
t=np.linspace(0,20,31)
observado=primer_orden(t,8,.4)+rng.normal(0,1,len(t))
theta,fit=ajustar_primer_orden(t,observado)
print('alfa, delta ajustados:',theta)
pred=primer_orden(t,*theta)
fig,ax=plt.subplots(1,2,figsize=(10,3.5))
ax[0].scatter(t,observado,label='Datos sintéticos')
ax[0].plot(t,pred,label='Ajuste');ax[0].legend()
ax[0].set(xlabel='Tiempo (h)',ylabel='Concentración (u.a.)')
ax[1].scatter(t,observado-pred);ax[1].axhline(0,color='k')
ax[1].set(xlabel='Tiempo (h)',ylabel='Residuo (u.a.)')
plt.tight_layout();plt.show()
