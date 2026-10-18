# Estabilidad homogénea y modos espaciales
# Modelos y números docentes originales. Fuentes: A01, D11
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av

k=np.linspace(0,1.3,401)
plt.plot(k,av.dispersion_turing(k),label='D=(1,20)')
plt.plot(k,av.dispersion_turing(k,D=(1,1)),label='D=(1,1)')
plt.axhline(0,color='black',ls='--')
plt.xlabel('Número de onda (1/longitud)')
plt.ylabel('Máxima parte real (1/tiempo)');plt.legend();plt.show()
unstable=k[av.dispersion_turing(k)>0]
print('Intervalo aproximado inestable:',unstable[0],unstable[-1])
