# Sensibilidad, tiempo e información
# Modelos y números docentes originales. Fuentes: A01, I06
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av

t=np.linspace(.01,20,301);alpha=8.;delta=.4
S=av.sensibilidad_lineal(t,alpha,delta)
x=av.primer_orden(t,alpha,delta)
plt.plot(t,alpha*S[0]/x,label='Elasticidad a alfa')
plt.plot(t,delta*S[1]/x,label='Elasticidad a delta')
plt.xlabel('Tiempo (h)');plt.ylabel('Sensibilidad relativa');plt.legend();plt.show()
for h in [1e-2,1e-3,1e-4]:
    fd=(av.primer_orden(t,alpha,delta+h)-av.primer_orden(t,alpha,delta-h))/(2*h)
    print('Paso, error derivada:',h,np.max(np.abs(fd-S[1])))
