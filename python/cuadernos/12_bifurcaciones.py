# Ramas estables e inestables de una autoactivación
# Modelos y números docentes originales. Fuentes: A01, A02
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av

a=np.linspace(2,5,301)
low=(a-np.sqrt(a*a-4))/2;high=(a+np.sqrt(a*a-4))/2
plt.plot(a,high,label='Rama alta estable')
plt.plot(a,low,'--',label='Rama intermedia inestable')
plt.plot([0,5],[0,0],label='Origen estable')
plt.xlabel('a (adimensional)');plt.ylabel('Equilibrio x*');plt.legend();plt.show()
print('Raíces para a=2,5:',av.ramas_autoactivacion(2.5))
t=np.linspace(0,30,301)
for x0 in [.4,.6]:
    y=av.integrar(av.autoactivacion,[x0],t,args=(2.5,))
    plt.plot(t,y[0],label=f'x0={x0}')
plt.xlabel('Tiempo adimensional');plt.ylabel('x');plt.legend();plt.show()
