"""Modelos docentes originales. Tiempo en horas salvo indicación explícita.

Los parámetros son ilustrativos: no constituyen calibraciones experimentales.
"""
from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares


def primer_orden(t, alfa=10.0, delta=0.2, x0=0.0):
    t = np.asarray(t)
    if alfa < 0 or delta <= 0 or x0 < 0:
        raise ValueError("Se requiere alfa>=0, delta>0 y x0>=0")
    return alfa / delta + (x0 - alfa / delta) * np.exp(-delta * t)


def hill(x, K=1.0, n=2.0, activar=True):
    x = np.asarray(x, dtype=float)
    if np.any(x < 0) or K <= 0 or n <= 0:
        raise ValueError("Hill requiere x>=0, K>0, n>0")
    f = x**n / (K**n + x**n)
    return f if activar else 1 - f


def integrar(rhs, y0, t, args=(), method="RK45", rtol=1e-8, atol=1e-10):
    t = np.asarray(t, dtype=float)
    if len(t) < 2 or np.any(np.diff(t) <= 0):
        raise ValueError("Los tiempos deben ser estrictamente crecientes")
    sol = solve_ivp(rhs, (t[0], t[-1]), y0, t_eval=t,
                    args=args, method=method, rtol=rtol, atol=atol)
    if not sol.success:
        raise RuntimeError(sol.message)
    if not np.all(np.isfinite(sol.y)):
        raise RuntimeError("Estado no finito")
    return sol.y


def gen(t, y, alfa=4.0, dm=1.0, beta=3.0, dp=0.2):
    m, p = y
    return [alfa - dm * m, beta * m - dp * p]


def toggle(t, y, alfa=10.0, n=2.0):
    x, z = y
    return [alfa / (1 + z**n) - x, alfa / (1 + x**n) - z]


def represilador(t, y, alfa=30.0, n=3.0):
    # Modelo reducido de tres proteínas: tiempo y concentración adimensionales.
    return alfa / (1 + np.roll(y, 1)**n) - y


def ssa_nacimiento_muerte(alfa=5.0, delta=0.5, x0=0, T=20.0, seed=42):
    """SSA exacta para nacimiento constante y muerte de primer orden.

    alfa: moléculas/h; delta: 1/h; estados enteros. Conserva el estado en T.
    """
    if alfa < 0 or delta < 0 or x0 < 0 or int(x0) != x0 or T <= 0:
        raise ValueError("Parámetros SSA no válidos")
    rng = np.random.default_rng(seed)
    t, x = 0.0, int(x0)
    ts, xs = [t], [x]
    while t < T:
        a0 = alfa + delta * x
        if a0 == 0:
            break
        dt = rng.exponential(1 / a0)
        if t + dt > T:
            break
        t += dt
        x += 1 if rng.random() * a0 < alfa else -1
        ts.append(t)
        xs.append(x)
    ts.append(T)
    xs.append(x)
    return np.array(ts), np.array(xs, dtype=int)


def telegrapho(T=50.0, seed=7, kon=0.15, koff=0.4, alfa=14., delta=0.4):
    """Promotor 0/1 y producto discreto; propensiones en eventos/h."""
    rng = np.random.default_rng(seed)
    t, s, x = 0., 0, 0
    ts, ss, xs = [0.], [s], [x]
    while t < T:
        a = np.array([kon*(1-s), koff*s, alfa*s, delta*x])
        if a.sum() == 0:
            break
        dt = rng.exponential(1 / a.sum())
        if t + dt > T:
            break
        t += dt
        j = rng.choice(4, p=a/a.sum())
        if j == 0: s = 1
        elif j == 1: s = 0
        elif j == 2: x += 1
        else: x -= 1
        ts.append(t); ss.append(s); xs.append(x)
    return np.r_[ts,T], np.r_[ss,s], np.r_[xs,x]


def ajustar_primer_orden(t, y, sigma=1.0):
    """x0=0 conocido; errores gaussianos independientes, sigma conocida."""
    def residual(logtheta):
        a, d = np.exp(logtheta)
        return (primer_orden(t, a, d) - y) / sigma
    fit = least_squares(residual, np.log([5., 0.3]))
    if not fit.success:
        raise RuntimeError(fit.message)
    return np.exp(fit.x), fit


def tejido(t, x, produccion, delta=0.4, intercambio=0.8):
    # Cadena de células iguales. Bordes sin flujo. Conserva intercambio.
    flujo = intercambio * np.diff(x)
    dx = np.asarray(produccion, float) - delta * x
    dx[:-1] += flujo
    dx[1:] -= flujo
    return dx


def maduracion(t, y, produccion=5.0, k=0.4, delta=0.1):
    inmadura, madura = y
    return [produccion - (k + delta)*inmadura, k*inmadura-delta*madura]


def euler(rhs, y0, t, args=()):
    """Solo docente; no adaptar el paso ni corregir estados negativos."""
    y = np.zeros((len(t), len(y0)), dtype=float)
    y[0] = y0
    for i in range(len(t)-1):
        y[i+1] = y[i] + (t[i+1]-t[i])*np.array(rhs(t[i], y[i], *args))
    return y.T
