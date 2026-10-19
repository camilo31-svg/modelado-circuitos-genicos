"""Modelos docentes para reconstruir ecuaciones, unidades y código.

Fuentes de principios: Ingalls (A01), Teschl (A02), Elowitz y Leibler
(D02), Becskei et al. (A25) y Muzzey et al. (A26). Los parámetros son
propios; la analogía de adaptación no es el modelo molecular de Hog1.
"""
import numpy as np
from scipy.optimize import brentq


def primer_orden(t, alfa=12., delta=.3, x0=5.):
    """Concentración exacta del balance x'=alfa-delta*x, t>=0."""
    t=np.asarray(t,dtype=float)
    if delta<0 or alfa<0 or x0<0 or np.any(t<0):
        raise ValueError('Se requieren tiempo, entrada y pérdidas no negativos.')
    if delta==0:
        return x0+alfa*t
    return alfa/delta+(x0-alfa/delta)*np.exp(-delta*t)


def diferencia_central(funcion, estado, paso=1e-5):
    """Columna j: cambio de todas las salidas al mover solo estado[j]."""
    estado=np.asarray(estado,dtype=float)
    if paso<=0:
        raise ValueError('El paso de diferencias debe ser positivo.')
    columnas=[]
    for j in range(estado.size):
        desplazamiento=np.zeros_like(estado)
        desplazamiento[j]=paso
        columna=(funcion(estado+desplazamiento)-
                 funcion(estado-desplazamiento))/(2*paso)
        columnas.append(columna)
    return np.column_stack(columnas)


def represilador(t, estado, alfa=60., basal=.01, beta=.2, n=2.):
    """Estado [m0,m1,m2,p0,p1,p2], todo adimensional."""
    estado=np.asarray(estado,dtype=float)
    m=estado[:3]
    p=estado[3:]
    reguladores=p[[2,0,1]]
    actividad=1./(1.+reguladores**n)
    dm=basal+alfa*actividad-m
    dp=beta*(m-p)
    return np.concatenate([dm,dp])


def represilador_dimensional(t, estado, sb=.0025, sv=15.,
                             gm=.5, gp=.1, kt=2., K=10., n=2.):
    """Concentraciones nM, tiempo h; no son tasas calibradas de E. coli."""
    estado=np.asarray(estado,dtype=float)
    M=estado[:3]
    P=estado[3:]
    reguladores=P[[2,0,1]]
    dM=sb+sv/(1.+(reguladores/K)**n)-gm*M
    dP=kt*M-gp*P
    return np.concatenate([dM,dP])


def a_dimensional(estado, gp=.1, kt=2., K=10.):
    """Convierte [m,p] a [M,P]; admite columnas de tiempos."""
    resultado=np.array(estado,dtype=float,copy=True)
    resultado[:3]*=gp*K/kt
    resultado[3:]*=K
    return resultado


def a_normalizado(estado, gp=.1, kt=2., K=10.):
    """Inversa de a_dimensional; el reloj se convierte por separado."""
    resultado=np.array(estado,dtype=float,copy=True)
    resultado[:3]*=kt/(gp*K)
    resultado[3:]/=K
    return resultado


def jacobiano_represilador(estado, alfa=60., basal=.01, beta=.2, n=2.):
    """Derivada respecto a seis estados, no respecto a los parámetros."""
    p=np.asarray(estado,dtype=float)[3:]
    J=np.zeros((6,6))
    J[:3,:3]=-np.eye(3)
    J[3:,:3]=beta*np.eye(3)
    J[3:,3:]=-beta*np.eye(3)
    for i,j in enumerate([2,0,1]):
        J[i,3+j]=-alfa*n*p[j]**(n-1)/(1+p[j]**n)**2
    return J


def equilibrio_represilador(alfa=60., basal=.01, n=2.):
    """Raíz simétrica única, acotada por basal y basal+alfa."""
    return brentq(lambda s:s-basal-alfa/(1+s**n),basal,basal+alfa)


def autoactivacion(t, x, a=3., basal=.02, n=2.):
    """Una variable tras reducción rápida del ARN; tiempo adimensional."""
    return basal+a*np.asarray(x)**n/(1+np.asarray(x)**n)-np.asarray(x)


def raices_autoactivacion(a=3., basal=.02):
    """Para n=2, multiplica por 1+x² y resuelve el cúbico exacto.

    Los coeficientes son [-1, a+basal, -1, basal]. Filtra el dominio
    físico y comprueba después el residuo en la ecuación original.
    """
    raices=np.roots([-1.,a+basal,-1.,basal])
    reales=sorted(float(z.real) for z in raices
                  if abs(z.imag)<1e-9 and z.real>=0)
    return np.array(reales)


def pendiente_autoactivacion(x, a=3.):
    return 2*a*np.asarray(x)/(1+np.asarray(x)**2)**2-1


def adaptacion(t, estado, a=1., b=1., c=1., entrada=1., fuga=0.):
    """Desviación h y compensación g; analogía local, no especies Hog1."""
    h,g=estado
    dh=a*(entrada-g)-b*h
    dg=c*h-fuga*g
    return np.array([dh,dg])


def adaptacion_exacta(t, a=1., b=1., c=1., entrada=1.):
    """Solución sin fuga, inicio cero, ac>b²/4, entrada constante."""
    if a<=0 or c<=0 or b<=0 or a*c<=b*b/4:
        raise ValueError('Esta fórmula se restringe al caso subamortiguado.')
    t=np.asarray(t,dtype=float)
    w=np.sqrt(a*c-b*b/4)
    envolvente=np.exp(-b*t/2)
    h=a*entrada*envolvente*np.sin(w*t)/w
    dh=a*entrada*envolvente*(np.cos(w*t)-b*np.sin(w*t)/(2*w))
    g=entrada-(dh+b*h)/a
    return np.array([h,g])


def equilibrio_adaptacion(a=1., b=1., c=1., entrada=1., fuga=0.):
    """Resuelve ambas ecuaciones estacionarias, también con fuga=0."""
    h=fuga*entrada/(c+fuga*b/a)
    g=entrada-b*h/a
    return np.array([h,g])
