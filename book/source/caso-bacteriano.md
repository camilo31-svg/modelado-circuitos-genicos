# Caso bacteriano completo: represilador, seis EDO y código explicado

- Definir cada estado, parámetro, unidad y supuesto antes de construir las ecuaciones.
- Derivar las transformaciones y explicar los pasos del programa.
- Verificar la implementación con identidades y separar ejemplo docente de evidencia publicada.

## Un caso completo: del anillo regulador a las seis variables

El represilador de Elowitz y Leibler es un caso clásico de circuito sintético en *Escherichia coli*: tres represores se conectan en un anillo y el estudio presenta un modelo con ARN y proteína. Nos servirá para practicar una reconstrucción completa. El circuito experimental motiva la arquitectura; las constantes y simulaciones de este capítulo son docentes y no se presentan como reproducción de sus datos. La referencia primaria permite contrastar el esquema y las convenciones de su modelo. [D02]

Usaremos tres unidades, llamadas 0, 1 y 2. La proteína de la unidad 2 reprime el ARN de la 0; la de la 0 reprime el de la 1; la de la 1 reprime el de la 2. No hay un inhibidor que «salte» por una flecha sin identificarse. Cada relación modifica una tasa de transcripción; no consume una proteína represora por cada ARN que deja de producirse. El libro de referencia desarrolla esta clase de balances y la diferencia entre regulación y reacción de transferencia. [A01]

### Tabla de elementos y decisiones del modelo dimensional

| Símbolo | Qué representa en este desarrollo | Unidad docente |
|---|---|---|
| M_i | ARN mensajero de la unidad i | nM |
| P_i | Proteína represora de la unidad i | nM |
| s_b | Producción basal de cada ARN | nM/h |
| s_v | Incremento máximo de producción regulada | nM/h |
| K | Escala de concentración represora | nM |
| n | Coeficiente de la función de Hill | Sin unidad |
| γ_m | Pérdida efectiva de ARN | 1/h |
| γ_p | Pérdida efectiva de proteína | 1/h |
| k_t | Producción proteica por ARN | 1/h con estas escalas molares |

Suponemos parámetros iguales para las tres unidades para estudiar la estructura del anillo. Esa simetría no afirma que tres genes reales tengan cinéticas idénticas. Suponemos además mezcla dentro del compartimento, regulación represora efectiva instantánea y ausencia de una limitación explícita de recursos. Si se quieren incluir unión lenta, crecimiento variable o ruido de bajo número de copias, hay que ampliar estados o hipótesis. [A01]

### Construir el primer balance y repetir la regla con cuidado

Para M₀, la producción es s_b+s_v/[1+(P₂/K)ⁿ]. s_b permanece incluso con mucha represión. La fracción reguladora se acerca a uno si P₂ es pequeña y a cero si es grande. La pérdida es γ_m M₀. Por tanto, M₀′=s_b+s_v/[1+(P₂/K)ⁿ]−γ_m M₀. Repetir la regla para las otras unidades cambia el índice del represor, no el significado de cada término. [A01]

$$
\frac{dM_0}{dt}=s_b+\frac{s_v}{1+(P_2/K)^n}-\gamma_mM_0.
$$

$$
\frac{dM_1}{dt}=s_b+\frac{s_v}{1+(P_0/K)^n}-\gamma_mM_1.
$$

$$
\frac{dM_2}{dt}=s_b+\frac{s_v}{1+(P_1/K)^n}-\gamma_mM_2.
$$

Para P₀, la traducción depende de M₀ y la pérdida de P₀: P₀′=k_t M₀−γ_p P₀. Las otras dos siguen su ARN correspondiente. La traducción no lleva un término −k_t M₀ en M₀′ porque el ARN funciona como plantilla; no lo estamos convirtiendo estequiométricamente en proteína. Los tres balances proteicos completan seis estados: P₁′=k_t M₁−γ_p P₁ y P₂′=k_t M₂−γ_p P₂. [A01]

Antes de resolver, comprueba la frontera: si M_i=0, su derivada es una producción no negativa; si P_i=0, su derivada es k_t M_i≥0. El campo apunta hacia el dominio no negativo o lo bordea. Eso es una propiedad de estas ecuaciones, no una razón para recortar automáticamente resultados negativos de un solver. Los parámetros de pérdida deben ser positivos para las escalas siguientes. [A01] [A02]

### Adimensionalizar sin perder ninguna constante

Elegimos τ=γ_m t como reloj, p_i=P_i/K como proteína normalizada y m_i=k_t M_i/(γ_p K) como ARN normalizado. m_i y p_i pueden compararse numéricamente como estados normalizados, pero no son la misma cantidad molecular. Para cualquier variable normalizada q(t), dq/dτ=(1/γ_m)dq/dt: ese factor procede de la regla de la cadena. [A01] [A02]

Sustituye P_i=Kp_i en la regulación. El cociente P_j/K se convierte en p_j. Para el ARN, dm_i/dτ=[k_t/(γ_p Kγ_m)]dM_i/dt. La pérdida de ARN pasa a −m_i. Define α₀=k_t s_b/(γ_p Kγ_m) y α=k_t s_v/(γ_p Kγ_m). Ambos son adimensionales. Así aparece m_i′=α₀+α/(1+p_jⁿ)−m_i, donde la prima de este párrafo deriva respecto a τ. [A01]

Para la proteína, dp_i/dτ=[k_t M_i−γ_p P_i]/(Kγ_m). Sustituye M_i=(γ_p K/k_t)m_i y P_i=Kp_i: obtienes (γ_p/γ_m)(m_i−p_i). Define β=γ_p/γ_m. No es una tasa de traducción: es el cociente de pérdidas. Esta definición concuerda con la convención de β utilizada en el modelo simétrico primario, aunque las magnitudes dimensionales docentes se eligen aquí para aprender la transformación. [A01] [D02]

### De los símbolos a los índices de Python

Guardaremos el estado como `[m0,m1,m2,p0,p1,p2]`. Las posiciones cero a dos son ARN; tres a cinco, proteínas. Un array auxiliar `[2,0,1]` especifica qué proteína reprime a cada unidad. `p[[2,0,1]]` devuelve las proteínas en ese orden. Si usáramos `[1,2,0]`, cambiaríamos la orientación del anillo; si usáramos `[0,1,2]`, convertiríamos el circuito en tres autorrepresores. El índice implementa una relación biológica. [R21] [A01]

```python
import numpy as np
from scipy.integrate import solve_ivp

def circuito(t, estado, alfa, basal, beta, n):
    m = estado[:3]                 # ARN 0, 1, 2
    p = estado[3:]                 # proteína 0, 1, 2
    represores = p[[2, 0, 1]]      # regulador de cada ARN
    actividad = 1.0 / (1.0 + represores**n)
    dm = basal + alfa * actividad - m
    dp = beta * (m - p)
    return np.concatenate([dm, dp])

inicial = np.array([0.1, 0.2, 0.3, 1.0, 2.0, 3.0])
tiempos = np.linspace(0.0, 300.0, 1501)
sol = solve_ivp(
    circuito, (0.0, 300.0), inicial,
    args=(60.0, 0.01, 0.2, 2.0),
    t_eval=tiempos, rtol=1e-8, atol=1e-10,
)
if not sol.success:
    raise RuntimeError(sol.message)
proteinas = sol.y[3:, :]
```

La línea `estado[:3]` corta antes de la posición tres; `estado[3:]` empieza en tres. `**n` eleva cada componente del array al exponente n. La expresión `1.0/(...)` opera componente a componente. Sumar `basal`, un escalar, a tres tasas añade la misma producción a cada unidad: NumPy extiende el escalar a las posiciones compatibles. `concatenate` junta primero tres pendientes de ARN y después tres de proteína, conservando exactamente el orden del estado inicial. No se suman ARN y proteína entre sí. [R21] [R03] [R20]

La función recibe t aunque no use el reloj: el sistema es autónomo y el integrador requiere esa firma. `args` envía los cuatro parámetros en el orden declarado. `tiempos` define dónde se guardan resultados; el algoritmo usa sus propios pasos internos. `proteinas` selecciona tres filas y todos los tiempos. Sus números son p_i, no P_i en nM. Para volver a concentración multiplica por K; para volver a horas divide τ por γ_m. [R05] [R21]

### Un juego dimensional que produce exactamente el mismo modelo

Elige γ_m=0,5 h⁻¹, γ_p=0,1 h⁻¹, K=10 nM y k_t=2 h⁻¹. Para α=60 necesitas s_v=α γ_p Kγ_m/k_t=15 nM/h. Para α₀=0,01, s_b=0,0025 nM/h. Un τ de 10 corresponde a 20 h; p=2 corresponde a 20 nM. Son números docentes deliberadamente definidos, no tasas experimentales asignadas al organismo. [A01]

Para convertir el estado inicial, P_i=Kp_i y M_i=(γ_p K/k_t)m_i. Integrar las seis EDO dimensionales a los tiempos t=τ/γ_m y transformar después las salidas debería coincidir con la simulación normalizada dentro del error numérico. La práctica 24 comprueba esa equivalencia. Esa prueba detecta errores de escala que pueden quedar ocultos si solo dibujas curvas sin unidades. [A01] [R05]

### Equilibrio simétrico y origen de la estabilidad

En equilibrio, dp_i/dτ=0 impone m_i=p_i. Si además las tres unidades están en el mismo estado s, queda s=α₀+α/(1+sⁿ). La función de la izquierda aumenta y la producción represora de la derecha disminuye, por lo que hay un único cruce simétrico positivo. Define g=αn sⁿ⁻¹/(1+sⁿ)². Es la magnitud de la pendiente de la regulación. [A01]

El Jacobiano tiene bloques: −I para ARN respecto a ARN, −gC para ARN respecto a proteínas, βI para proteína respecto a ARN y −βI para proteína respecto a proteína. C es la matriz que reordena proteínas como `[2,0,1]`. En lugar de aceptar ese bloque por su nombre, lee una fila: la pendiente de m₀ disminuye una unidad por cada aumento de m₀ y disminuye g por cada aumento de p₂; las otras entradas son cero. La fila de p₀ tiene β en m₀ y −β en p₀. [A01] [A27]

Si una perturbación tiene la forma e^{λτ}, eliminar su ARN y proteína de cada unidad conduce a [(λ+1)(λ+β)]³+(βg)³=0. Cada factor (λ+1) y (λ+β) refleja una relajación de ARN o proteína. Este polinomio tiene grado seis porque el sistema conserva seis estados. No se reemplaza por el cúbico de un modelo de tres proteínas sin justificar la reducción. La práctica calcula autovalores y contrasta el Jacobiano analítico con diferencias finitas, que mueven una entrada cada vez. [A01] [A27]

### Qué puedes y qué no puedes concluir de las curvas

Al iniciar todas las unidades exactamente iguales, la simetría se conserva en la solución determinista ideal. Para observar la respuesta a diferencias entre ellas, el estado inicial docente introduce una asimetría pequeña. Una perturbación o ruido real también podría romper esa coincidencia. No debes confundir esta decisión numérica con una afirmación sobre cómo se prepara una célula. [A01]

Compara varios ciclos tras la relajación, cambia tolerancias y estudia si amplitud y período se mantienen. Una pareja compleja inestable indica que el equilibrio pierde estabilidad, pero no demuestra por sí sola el tipo final de movimiento no lineal. Además, la fluorescencia experimental requiere una ecuación de reportero; el vector p no es automáticamente una traza de GFP. Para reproducir una observación, añade maduración, escala y fondo según los datos disponibles. [A01] [I04] [D02]

### Ejercicio con respuesta explicada

Si duplicas γ_m dejando todas las constantes dimensionales restantes iguales, β se reduce a la mitad, α y α₀ también se reducen a la mitad y la relación entre τ y horas cambia. No has movido «solo el reloj»: has alterado la abundancia media de ARN y la relación de escalas temporales. Si en cambio multiplicas todas las tasas dimensionales por el mismo factor c de forma coherente, puedes conservar la trayectoria normalizada y cambiar la rapidez en horas. Esta distinción explica por qué no conviene interpretar un parámetro adimensional aislado sin volver a su definición. [A01]
