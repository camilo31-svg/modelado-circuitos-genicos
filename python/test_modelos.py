"""Validación científica pequeña: invariantes y casos con respuesta conocida."""
import unittest
import numpy as np
from circuitos import *


class Modelos(unittest.TestCase):
    def test_analitico(self):
        t=np.linspace(0,30,101)
        y=integrar(lambda t,y: [10-.2*y[0]], [0], t)[0]
        np.testing.assert_allclose(y, primer_orden(t), atol=1e-6)

    def test_conservacion_intercambio(self):
        y=np.array([1.,3.,7.,9.])
        self.assertAlmostEqual(sum(tejido(0,y,np.zeros(4),delta=0)),0.)

    def test_toggle_memoria(self):
        t=np.linspace(0,40,300)
        a=integrar(toggle,[9.,.1],t)[:,-1]
        b=integrar(toggle,[.1,9.],t)[:,-1]
        self.assertGreater(a[0],9.); self.assertLess(a[1],.2)
        np.testing.assert_allclose(a,b[::-1],atol=1e-5)

    def test_hill(self):
        self.assertAlmostEqual(float(hill(3,K=3,n=4)),.5)
        np.testing.assert_allclose(hill([0,1,2])+hill([0,1,2],activar=False),1)

    def test_ssa_entero_no_negativo_y_media(self):
        finales=[]
        for s in range(500):
            t,x=ssa_nacimiento_muerte(seed=s)
            self.assertTrue(np.all(x>=0)); self.assertTrue(np.all(np.diff(t)>=0))
            finales.append(x[-1])
        esperada=10*(1-np.exp(-10))
        self.assertLess(abs(np.mean(finales)-esperada),.6)

    def test_estimacion_sin_ruido(self):
        t=np.linspace(0,30,40)
        p,_=ajustar_primer_orden(t,primer_orden(t,8,.4))
        np.testing.assert_allclose(p,[8,.4],rtol=1e-5)

    def test_represilador(self):
        y=integrar(represilador,[.1,2.,5.],np.linspace(0,150,1501))
        self.assertGreater(np.ptp(y[0,-500:]),2)
        self.assertGreaterEqual(y.min(),0)

    def test_gen_equilibrio(self):
        y=integrar(gen,[0,0],np.linspace(0,100,300))[:,-1]
        np.testing.assert_allclose(y,[4,60],rtol=1e-5)

if __name__=='__main__':
    unittest.main(verbosity=2)
