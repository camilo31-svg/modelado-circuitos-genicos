# Nueve especies y tres conservaciones
# Modelos y números docentes originales. Fuentes: A01, A16
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av

N,L=av.fosforilacion_red()
print('Conservaciones L@N:',np.max(np.abs(L@N)))
y0=np.array([10,0,0,2,1,0,0,0,0],float)
t=np.linspace(0,80,401)
y=av.integrar(av.fosforilacion,y0,t,method='Radau')
for i,label in enumerate(['X0 libre','X1 libre','X2 libre']):
    plt.plot(t,y[i],label=label)
plt.xlabel('Tiempo (u.a.)');plt.ylabel('Cantidad (u.a.)');plt.legend();plt.show()
print('Totales iniciales:',L@y0)
print('Máxima desviación de totales:',np.max(np.abs(L@y-(L@y0)[:,None])))
