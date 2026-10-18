# Calibración estática frente a dinámica de auxina
# Modelos y números docentes originales. Fuentes: A01, P01, P02
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av

t=np.linspace(0,30,301)
S=av.integrar(av.sensor,[10.],t)[0]
static=5*(10/S-1)
derivative=1-(.1+.02*5)*S
dynamic=(1-.1*S-derivative)/(.02*S)
plt.plot(t,static,label='Inversión estacionaria')
plt.plot(t,dynamic,label='Identidad dinámica sin ruido')
plt.axhline(5,color='black',ls='--',label='Entrada verdadera')
plt.xlabel('Tiempo (min)');plt.ylabel('Entrada estimada (u.a.)');plt.legend();plt.show()
print('Error inicial estático:',static[0]-5)
