# Unión molecular y raíz físicamente válida
# Modelos y números docentes originales. Fuentes: A01
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av

t=np.linspace(0,3,151)
c=av.integrar(av.union,[0.],t,method='Radau')[0]
equilibrio=av.union_equilibrio()
print('Complejo en equilibrio:',equilibrio,'nM')
print('A libre, B libre:',10-equilibrio,8-equilibrio)
plt.plot(t,c,label='Complejo')
plt.axhline(equilibrio,color='black',ls='--',label='Raíz analítica')
plt.xlabel('Tiempo (h)');plt.ylabel('Complejo (nM)');plt.legend();plt.show()
