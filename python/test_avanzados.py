"""Casos científicos con respuesta conocida; edición 2.0."""
import unittest
import numpy as np
from circuitos_avanzados import *


class Avanzados(unittest.TestCase):
    def test_union_dominio_y_equilibrio(self):
        c=union_equilibrio()
        self.assertAlmostEqual(c,10-np.sqrt(20))
        self.assertAlmostEqual(union(0,[c])[0],0.,places=10)
        y=integrar(union,[0],np.linspace(0,3,50),method='Radau')
        self.assertTrue(np.all((y>=-1e-10)&(y<=8)))

    def test_ramas_y_estabilidad(self):
        roots=ramas_autoactivacion(2.5)
        np.testing.assert_allclose(roots,[0,.5,2])
        for x in roots:self.assertAlmostEqual(autoactivacion(0,[x],2.5)[0],0.)
        slopes=[2*2.5*x/(1+x*x)**2-1 for x in roots]
        self.assertLess(slopes[0],0);self.assertGreater(slopes[1],0);self.assertLess(slopes[2],0)

    def test_goodwin_umbral(self):
        s,a,w=umbral_goodwin(10)
        np.testing.assert_allclose(goodwin(0,[s,s,s],a,10),0,atol=1e-12)
        g=a*10*s**9/(1+s**10)**2
        self.assertAlmostEqual(g,8)
        self.assertAlmostEqual(abs((1+1j*w)**3+g),0,places=10)

    def test_identidad_control_y_equilibrio(self):
        y,z1,z2=3.,2.,.7
        rhs=antitetico(0,[y,z1,z2])
        self.assertAlmostEqual(rhs[1]-rhs[2],2-.5*y)
        np.testing.assert_allclose(antitetico(0,[4,4,.5]),0,atol=1e-12)
        r=antitetico(0,[y,z1,z2],dilucion=.1)
        self.assertAlmostEqual(r[1]-r[2],2-.5*y-.1*(z1-z2))

    def test_fase_bloqueada(self):
        w1,w2=2*np.pi/24,2*np.pi/26;K=.015
        psi=np.arcsin((w2-w1)/(2*K))
        rhs=fases(0,[0,psi],w1,w2,K)
        self.assertAlmostEqual(rhs[0],rhs[1])
        self.assertAlmostEqual(rhs[0],(w1+w2)/2)

    def test_momentos_telegr(self):
        m,v=momentos_telegr()
        self.assertAlmostEqual(m,10.)
        self.assertAlmostEqual(v,10+100/3)
        self.assertLess(momentos_telegr(10,10)[1],v)

    def test_ssa_dominio(self):
        y=telegr_ssa(np.linspace(0,30,301),seed=12)
        self.assertTrue(np.all(np.isin(y[0],[0,1])))
        self.assertTrue(np.all(y[1]>=0))
        self.assertTrue(np.all(y[1]==np.floor(y[1])))

    def test_sensibilidad_analitica(self):
        t=np.array([.1,1,4,20]);h=1e-4
        finite=(primer_orden(t,8,.4+h)-primer_orden(t,8,.4-h))/(2*h)
        np.testing.assert_allclose(sensibilidad_lineal(t)[1],finite,rtol=1e-6)

    def test_conservaciones_fosforilacion(self):
        N,L=fosforilacion_red()
        np.testing.assert_array_equal(L@N,np.zeros((3,12)))
        y0=np.array([10,0,0,2,1,0,0,0,0],float)
        y=integrar(fosforilacion,y0,np.linspace(0,10,51),method='Radau')
        np.testing.assert_allclose(L@y,np.repeat((L@y0)[:,None],51,axis=1),atol=1e-8)
        self.assertGreater(np.min(y),-1e-8)

    def test_turing_requiere_difusion(self):
        k=np.linspace(0,1,101)
        rate=dispersion_turing(k)
        self.assertLess(rate[0],0);self.assertGreater(rate.max(),0)
        self.assertTrue(np.all(dispersion_turing(k,D=(1,1))<0))

    def test_riesgo_acumulado(self):
        t=np.linspace(0,10,50);p=integrar(registro,[0],t,args=(.1,))
        np.testing.assert_allclose(p[0],1-np.exp(-.1*t),atol=1e-8)

    def test_recurso_competencia(self):
        self.assertAlmostEqual(recurso(1,0)[0],.5)
        self.assertAlmostEqual(recurso(1,4)[0],1/6)
        a,b=recurso(3,7)
        self.assertLess(a+b,1)


if __name__=='__main__':unittest.main()
