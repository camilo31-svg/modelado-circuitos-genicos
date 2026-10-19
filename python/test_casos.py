"""Consecuencias analíticas independientes de las curvas de enseñanza."""
import unittest
import numpy as np
from scipy.integrate import solve_ivp
import circuitos_casos as cc


class Casos(unittest.TestCase):
    def test_normalizacion_es_inversa_y_no_modifica_entrada(self):
        z=np.arange(1.,19.).reshape(6,3);copia=z.copy()
        np.testing.assert_allclose(cc.a_normalizado(cc.a_dimensional(z)),z)
        np.testing.assert_array_equal(z,copia)

    def test_equivalencia_de_pendientes_por_regla_cadena(self):
        z=np.array([.1,.3,.6,1.,3.,5.])
        dimensional=cc.a_dimensional(z)
        # dx_normalizado/dtau = transformación de dx_dimensional/dt / gm.
        transformada=cc.a_normalizado(cc.represilador_dimensional(0,dimensional))/.5
        np.testing.assert_allclose(transformada,cc.represilador(0,z),rtol=1e-13)

    def test_equivalencia_de_trayectorias(self):
        z=np.array([.1,.2,.3,1.,2.,3.]);tau=np.linspace(0,30,151)
        s1=solve_ivp(cc.represilador,(0,30),z,t_eval=tau,rtol=1e-10,atol=1e-12)
        s2=solve_ivp(cc.represilador_dimensional,(0,60),cc.a_dimensional(z),
                     t_eval=tau/.5,rtol=1e-10,atol=1e-12)
        self.assertTrue(s1.success and s2.success)
        np.testing.assert_allclose(s1.y,cc.a_normalizado(s2.y),rtol=2e-8,atol=2e-8)

    def test_jacobiano_con_diferencias_independientes(self):
        z=np.array([.2,.5,.7,1.,2.,4.])
        fd=cc.diferencia_central(lambda v:cc.represilador(0,v),z)
        np.testing.assert_allclose(fd,cc.jacobiano_represilador(z),rtol=2e-8,atol=2e-8)

    def test_polinomio_de_seis_estados_en_equilibrio(self):
        s=cc.equilibrio_represilador();z=np.full(6,s)
        np.testing.assert_allclose(cc.represilador(0,z),0,atol=1e-11)
        g=60*2*s/(1+s*s)**2;beta=.2
        eigen=np.linalg.eigvals(cc.jacobiano_represilador(z))
        residuo=((eigen+1)*(eigen+beta))**3+(beta*g)**3
        np.testing.assert_allclose(residuo,0,atol=1e-11)

    def test_dominio_no_negativo_en_fronteras(self):
        for j in range(6):
            z=np.arange(1.,7.);z[j]=0
            self.assertGreaterEqual(cc.represilador(0,z)[j],0)

    def test_raices_y_estabilidad_autoactivacion_con_y_sin_fuga_basal(self):
        for basal in [0.,.02]:
            roots=cc.raices_autoactivacion(basal=basal)
            self.assertEqual(len(roots),3)
            np.testing.assert_allclose(cc.autoactivacion(0,roots,basal=basal),0,atol=1e-12)
            self.assertEqual(list(cc.pendiente_autoactivacion(roots)<0),[True,False,True])
        np.testing.assert_allclose(cc.raices_autoactivacion(basal=0),
            [0,(3-np.sqrt(5))/2,(3+np.sqrt(5))/2],atol=1e-12)

    def test_adaptacion_con_solucion_analitica(self):
        t=np.linspace(0,20,401)
        sol=solve_ivp(cc.adaptacion,(0,20),[0,0],t_eval=t,rtol=1e-10,atol=1e-12)
        self.assertTrue(sol.success)
        np.testing.assert_allclose(sol.y,cc.adaptacion_exacta(t),atol=2e-10,rtol=2e-8)

    def test_error_con_fuga_resuelve_ambos_balances(self):
        for fuga in [0,.1,.3]:
            state=cc.equilibrio_adaptacion(a=2,b=3,c=4,entrada=5,fuga=fuga)
            np.testing.assert_allclose(cc.adaptacion(0,state,2,3,4,5,fuga),0,atol=1e-13)
            if fuga>0:self.assertGreater(state[0],0)

    def test_primer_orden_sin_perdida_no_divide_por_cero(self):
        np.testing.assert_allclose(cc.primer_orden([0,1,2],alfa=3,delta=0,x0=2),[2,5,8])


if __name__=='__main__':unittest.main()
