# Dos anillos acoplados: seis proteínas
# Modelos y números docentes originales. Fuentes: A01, A06
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av

t=np.linspace(0,180,3601)
for kappa in [0.,.1]:
    y=av.integrar(av.anillos_acoplados,[.1,2,5,2,.1,5],t,
                    args=(30.,3.,kappa))
    fig,ax=plt.subplots(2,1)
    ax[0].plot(t,y[0],label='X1');ax[0].plot(t,y[3],label='Y1')
    ax[0].set_xlabel('Tiempo adimensional')
    ax[0].set_ylabel('Proteínas (u.a.)');ax[0].legend()
    ax[1].plot(y[0,-1500:],y[3,-1500:])
    ax[1].set_xlabel('X1 (u.a.)');ax[1].set_ylabel('Y1 (u.a.)')
    fig.suptitle(f'Acoplamiento kappa={kappa}');plt.show()
    print('Rango final X1:',kappa,np.ptp(y[0,-1000:]))
