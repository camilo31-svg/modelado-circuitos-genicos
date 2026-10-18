# Tejido en una cadena de células
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
N=30
s=np.zeros(N);s[3:7]=3
t=np.linspace(0,30,301)
y=integrar(tejido,np.zeros(N),t,args=(s,))
plt.imshow(y,aspect='auto',origin='lower',extent=[0,30,0,N],cmap='viridis')
plt.colorbar(label='Concentración (u.a.)')
plt.xlabel('Tiempo (h)');plt.ylabel('Índice de célula')
plt.show()
print('Suma intercambio:',sum(tejido(0,y[:,-1],np.zeros(N),delta=0)))
