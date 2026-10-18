# Control antitético, perturbación y fuga
# Modelos y números docentes originales. Fuentes: A04, I09
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av

for fuga in [0.,.05]:
    t1=np.linspace(0,30,301);t2=np.linspace(30,90,601)
    y1=av.integrar(av.antitetico,[0,0,0],t1,
                    args=(2.,.5,1.,1.,1.,fuga),method='Radau')
    y2=av.integrar(av.antitetico,y1[:,-1],t2,
                    args=(2.,.5,1.,2.,1.,fuga),method='Radau')
    tt=np.r_[t1,t2[1:]];yy=np.c_[y1,y2[:,1:]]
    plt.plot(tt,yy[0],label=f'Dilución control={fuga}/h')
    print('Salida final, fuga:',yy[0,-1],fuga)
plt.axhline(4,color='black',ls='--',label='Referencia ideal')
plt.axvline(30,color='gray',ls=':')
plt.xlabel('Tiempo (h)');plt.ylabel('Salida (nM)');plt.legend();plt.show()
