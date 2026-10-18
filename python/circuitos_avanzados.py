"""Modelos docentes originales de la edición 2.0; no son ajustes a artículos.

Referencias de principios: Ingalls (versión 2015), capítulos 2–7; Briat et al.
2016 (A04); Gillespie 1977 (I02); Markevich et al. 2004 (A16). Las ecuaciones,
unidades y límites se explican en los capítulos correspondientes del libro.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares


def integrar(rhs, inicial, tiempo, args=(), method='RK45', **options):
    """Integra en tiempos de salida; falla explícitamente si falla el solver."""
    tiempo=np.asarray(tiempo,dtype=float)
    opts={'rtol':1e-8,'atol':1e-10};opts.update(options)
    sol=solve_ivp(rhs,(tiempo[0],tiempo[-1]),inicial,t_eval=tiempo,
                  args=args,method=method,**opts)
    if not sol.success:raise RuntimeError(sol.message)
    return sol.y


def primer_orden(t,alfa=8.,delta=.4,x0=0.):
    t=np.asarray(t,dtype=float)
    if delta==0:return x0+alfa*t
    return x0*np.exp(-delta*t)+alfa/delta*(-np.expm1(-delta*t))


def sensibilidad_lineal(t,alfa=8.,delta=.4):
    """dx/dalfa, dx/ddelta; x0=0. Tiempo h, salida nM."""
    t=np.asarray(t);e=np.exp(-delta*t)
    return np.array([(1-e)/delta,-alfa*(1-e)/delta**2+alfa*t*e/delta])


def union(t,c,k_on=1.,k_off=2.,total_a=10.,total_b=8.):
    """c en nM; libres total_a-c y total_b-c. Tiempo h."""
    z=c[0]
    return [k_on*(total_a-z)*(total_b-z)-k_off*z]


def union_equilibrio(total_a=10.,total_b=8.,kd=2.):
    # Forma estable: evita restar dos números cercanos cuando Kd es grande.
    s=total_a+total_b+kd
    return 2*total_a*total_b/(s+np.sqrt(s*s-4*total_a*total_b))


def autoactivacion(t,x,a=3.,fuga=0.):
    z=x[0]
    return [fuga+a*z*z/(1+z*z)-z]


def ramas_autoactivacion(a):
    """Equilibrios físicos para fuga=0; no clasifica otras leyes."""
    if a<2:return np.array([0.])
    return np.array([0.,(a-np.sqrt(a*a-4))/2,(a+np.sqrt(a*a-4))/2])


def goodwin(t,estado,a=8.,n=10.):
    x,y,z=estado
    return [a/(1+z**n)-x,x-y,y-z]


def umbral_goodwin(n=10.):
    """Candidato a Hopf para tres pérdidas iguales: g=8, omega=sqrt(3)."""
    if n<=8:raise ValueError('El modelo simétrico requiere n>8 para g>8.')
    s=(8/(n-8))**(1/n)
    return s,s*(1+s**n),np.sqrt(3.)


def antitetico(t,estado,mu=2.,theta=.5,k=1.,gamma=1.,eta=1.,
               dilucion=0.,vmax=None,km=1.):
    """Estados [salida,z1,z2] en nM; tiempo h. Actuación opcional saturable."""
    y,z1,z2=estado
    v=k*z1 if vmax is None else vmax*z1/(km+z1)
    encuentro=eta*z1*z2
    return [v-gamma*y,mu-encuentro-dilucion*z1,
            theta*y-encuentro-dilucion*z2]


def fases(t,phi,w1=2*np.pi/24,w2=2*np.pi/26,K=.015):
    p,q=phi
    return [w1+K*np.sin(q-p),w2+K*np.sin(p-q)]


def anillos_acoplados(t,estado,a=30.,n=3.,kappa=.1):
    """Seis proteínas adimensionales; dos represiladores con represión cruzada."""
    x1,x2,x3,y1,y2,y3=estado
    return [a/(1+x3**n+kappa*y1**n)-x1,
            a/(1+x1**n)-x2,a/(1+x2**n)-x3,
            a/(1+y3**n+kappa*x1**n)-y1,
            a/(1+y1**n)-y2,a/(1+y2**n)-y3]


def momentos_telegr(a_on=1.,a_off=1.,s=20.,gamma=1.):
    p=a_on/(a_on+a_off)
    media=s*p/gamma
    var=media+s*s*p*(1-p)/(gamma*(gamma+a_on+a_off))
    return media,var


def telegr_ssa(tiempos,kon=1.,koff=1.,s=20.,gamma=1.,seed=1,inicial=(0,0)):
    """SSA exacto del promotor telegráfico con tasas constantes. Devuelve G,N."""
    tiempos=np.asarray(tiempos);rng=np.random.default_rng(seed)
    t=float(tiempos[0]);G,N=map(int,inicial);events=[t];states=[(G,N)]
    changes=[(1,0),(-1,0),(0,1),(0,-1)]
    while t<tiempos[-1]:
        rates=np.array([kon*(1-G),koff*G,s*G,gamma*N],float)
        total=rates.sum()
        if total==0:break
        t+=rng.exponential(1/total)
        if t>tiempos[-1]:break
        j=np.searchsorted(np.cumsum(rates),rng.random()*total,side='right')
        dG,dN=changes[j];G+=dG;N+=dN
        events.append(t);states.append((G,N))
    indices=np.searchsorted(events,tiempos,side='right')-1
    return np.asarray(states)[indices].T


def dispersion_turing(ondas,J=None,D=(1.,20.)):
    """Parte real máxima de autovalores J-k²D; k en longitud inversa."""
    if J is None:J=np.array([[1.,-2.],[2.,-3.]])
    return np.array([np.max(np.linalg.eigvals(J-k*k*np.diag(D)).real) for k in ondas])


def sensor(t,S,p=1.,delta=.1,k=.02,entrada=5.):
    """Sensor abstracto; tiempo min, S nM, entrada en unidades arbitrarias."""
    u=entrada(t) if callable(entrada) else entrada
    return [p-(delta+k*u)*S[0]]


def registro(t,P,h=.1,mu0=0.,mu1=0.):
    """Fracción registrada con posible crecimiento diferencial."""
    q=P[0];rate=h(t) if callable(h) else h
    return [rate*(1-q)+(mu1-mu0)*q*(1-q)]


def perfiles_lineales(t,datos,sigma,alfas):
    """Fija alfa y reoptimiza delta positiva; devuelve chi² y delta óptima."""
    objectives=[];deltas=[]
    for a in alfas:
        fit=least_squares(lambda z:(primer_orden(t,a,np.exp(z[0]))-datos)/sigma,
                          [np.log(.4)],bounds=([-8.],[4.]))
        objectives.append(np.sum(fit.fun**2));deltas.append(np.exp(fit.x[0]))
    return np.array(objectives),np.array(deltas)


def fosforilacion_red():
    """X0,X1,X2,E,F,C1,C2,D2,D1; doce reacciones y tres conservaciones."""
    changes=[
      [-1,0,0,-1,0,1,0,0,0],[1,0,0,1,0,-1,0,0,0],
      [0,1,0,1,0,-1,0,0,0],[0,-1,0,-1,0,0,1,0,0],
      [0,1,0,1,0,0,-1,0,0],[0,0,1,1,0,0,-1,0,0],
      [0,0,-1,0,-1,0,0,1,0],[0,0,1,0,1,0,0,-1,0],
      [0,1,0,0,1,0,0,-1,0],[0,-1,0,0,-1,0,0,0,1],
      [0,1,0,0,1,0,0,0,-1],[1,0,0,0,1,0,0,0,-1]]
    N=np.array(changes,dtype=float).T
    L=np.array([[0,0,0,1,0,1,1,0,0],
                [0,0,0,0,1,0,0,1,1],
                [1,1,1,0,0,1,1,1,1]],float)
    return N,L


def fosforilacion(t,y,on=1.,off=.5,cat=.5):
    x0,x1,x2,E,F,c1,c2,d2,d1=y
    v=np.array([on*E*x0,off*c1,cat*c1,on*E*x1,off*c2,cat*c2,
                on*F*x2,off*d2,cat*d2,on*F*x1,off*d1,cat*d1])
    N,_=fosforilacion_red()
    return N@v


def recurso(dA,dB,total=1.,kA=1.,kB=1.):
    """Asignación rápida de recurso abstracto; demandas adimensionales."""
    den=1+np.asarray(dA)+np.asarray(dB)
    return kA*total*np.asarray(dA)/den,kB*total*np.asarray(dB)/den
