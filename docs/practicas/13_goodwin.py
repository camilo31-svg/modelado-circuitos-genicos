# Derivar y comprobar el umbral de Goodwin
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

s,acrit,w=av.umbral_goodwin(10)
print('Equilibrio crítico, a crítico, frecuencia:',s,acrit,w)
print('Período lineal en el cruce:',2*np.pi/w)
t=np.linspace(0,120,2401)
for a in [4.,8.]:
    y=av.integrar(av.goodwin,[.1,.5,.7],t,args=(a,10.))
    plt.plot(t,y[0],label=f'a={a}')
plt.xlabel('Tiempo adimensional');plt.ylabel('Estado x');plt.legend();plt.show()
