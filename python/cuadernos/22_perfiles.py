# Perfil de verosimilitud y diseño temporal
# Modelos y números docentes originales. Fuentes: I06, A09, A10
from pathlib import Path
import sys
base = Path(__file__).resolve().parent.parent if '__file__' in globals() else Path.cwd()
if not (base / 'circuitos_avanzados.py').exists():
    base = base.parent
sys.path.insert(0, str(base))
import numpy as np
import matplotlib.pyplot as plt
import circuitos_avanzados as av

rng=np.random.default_rng(26);sigma=1.;alfas=np.linspace(3,16,100)
for t,label in [(np.linspace(0,15,25),'Transitorio'),
                 (np.linspace(40,55,25),'Casi equilibrio')]:
    datos=av.primer_orden(t,8,.4)+rng.normal(0,sigma,len(t))
    obj,delta=av.perfiles_lineales(t,datos,sigma,alfas)
    plt.plot(alfas,obj-obj.min(),label=label)
plt.ylim(0,30);plt.xlabel('alfa fijada (nM/h)')
plt.ylabel('Aumento de chi² tras reoptimizar');plt.legend();plt.show()
