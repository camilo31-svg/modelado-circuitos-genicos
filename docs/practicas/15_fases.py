# Bloqueo y deriva entre dos osciladores
# Modelos y números docentes originales. Fuentes: A01, A05
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av

t=np.linspace(0,1000,3001)
for K in [.005,.015]:
    phi=av.integrar(av.fases,[0,.2],t,args=(2*np.pi/24,2*np.pi/26,K))
    psi=phi[1]-phi[0]
    plt.plot(t,psi,label=f'K={K}/h')
    print('Cambio final de fase relativa:',K,psi[-1]-psi[-101])
plt.xlabel('Tiempo (h)');plt.ylabel('Fase relativa (rad)');plt.legend();plt.show()
