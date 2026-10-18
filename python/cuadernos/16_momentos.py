# Promotor telegráfico: media y varianza
# Modelos y números docentes originales. Fuentes: A20, I02
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av

t=np.array([0.,80.]);finales=[]
for seed in range(128):
    finales.append(av.telegr_ssa(t,seed=seed)[1,-1])
finales=np.array(finales)
media,var=av.momentos_telegr()
print('Analítica:',media,var)
print('Estimación Monte Carlo:',finales.mean(),finales.var(ddof=1))
plt.hist(finales,bins=np.arange(0,max(finales)+2)-.5,density=True)
plt.axvline(media,color='black',ls='--',label='Media analítica')
plt.xlabel('ARN (moléculas)');plt.ylabel('Frecuencia relativa');plt.legend();plt.show()
