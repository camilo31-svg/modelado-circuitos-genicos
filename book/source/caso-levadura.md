# Casos de levadura: autoactivación, adaptación y programa explicado

- Definir cada estado, parámetro, unidad y supuesto antes de construir las ecuaciones.
- Derivar las transformaciones y explicar los pasos del programa.
- Verificar la implementación con identidades y separar ejemplo docente de evidencia publicada.

## Dos preguntas distintas en levadura: elegir un estado y adaptarse

La levadura *Saccharomyces cerevisiae* permite estudiar tanto circuitos sintéticos como redes naturales de regulación. Becskei, Séraphin y Serrano analizaron una autoactivación sintética y respuestas de expresión con dos poblaciones. Muzzey y colaboradores estudiaron adaptación en osmorregulación. Usaremos esas preguntas para construir dos modelos docentes, con variables y constantes explícitas. Las simulaciones siguientes no se atribuyen a sus mediciones ni reemplazan sus modelos completos. [A25] [A26]

### Caso A: qué significa que un activador favorezca su propia producción

Llama m al ARN del activador, p a su proteína y u a una entrada fijada. Propón m′=b+V H(p,u)−γ_m m y p′=k_t m−γ_p p. La regulación H vale entre cero y uno y representa la actividad del promotor. Una aproximación posible es H=(a(u)p)ⁿ/[Kⁿ+(a(u)p)ⁿ], donde a(u) es una fracción activa dependiente de la entrada. Definir a(u) exige su propia hipótesis de activación; no se obtiene de la palabra «inductor». Para el análisis siguiente fijamos u y absorbemos su efecto en una escala K efectiva. [A01]

b representa producción basal de ARN, V el incremento máximo regulado, γ_m y γ_p pérdidas, k_t traducción y K una concentración de activador. La regulación positiva significa que p aumenta la producción de su ARN. Es una dependencia de tasa, no una reacción que convierta una proteína en dos. El estudio sintético de levadura motiva esta arquitectura general y la importancia de distinguir respuesta media y distribuciones celulares. [A25]

### Justificar la reducción a una sola variable

Si el ARN se relaja rápidamente respecto a la proteína y a los cambios de entrada, aproxima m≈[b+V H(p)]/γ_m. Sustituir en p′ da p′=k_t b/γ_m+(k_t V/γ_m)H(p)−γ_p p. El ARN no desaparece biológicamente: su efecto se ha reemplazado por una relación algebraica aproximada. La reducción no reproduce necesariamente el arranque ni fluctuaciones asociadas al ARN. [A01]

Normaliza x=p/K y τ=γ_p t. Con H=xⁿ/(1+xⁿ), define b₀=k_t b/(γ_mγ_pK) y a=k_t V/(γ_mγ_pK). Entonces x′=b₀+a xⁿ/(1+xⁿ)−x, con prima respecto a τ. Esta forma permite estudiar la competencia entre una producción saturante y una pérdida recta. b₀ y a son adimensionales; b y b₀ no son el mismo parámetro. [A01]

### Un ejemplo de bistabilidad que se calcula paso a paso

Empieza por b₀=0, n=2 y a=3. La ecuación de equilibrio se factoriza como x[x²−3x+1]=0 después de multiplicar por el denominador y cambiar un signo. Las raíces no negativas son 0, (3−√5)/2 y (3+√5)/2: aproximadamente 0, 0,382 y 2,618. La derivada del campo es 6x/(1+x²)²−1. En cero vale −1 y es estable. En los otros equilibrios puede simplificarse a (1−x²)/(1+x²): la raíz pequeña es inestable y la grande estable. [A01] [A02]

El equilibrio intermedio divide las condiciones iniciales: si comienzas por debajo, la trayectoria va al estado bajo; si por encima, al alto. En una EDO determinista, dos trayectorias con el mismo estado y entrada no eligen al azar entre destinos. Para describir cambios espontáneos hacen falta un proceso de saltos u otra fuente de variación explícita. Bistabilidad determinista y una distribución con dos picos no son afirmaciones intercambiables. [A01] [A07]

Con una producción basal b₀ pequeña y positiva, cero deja de ser equilibrio: allí x′=b₀>0. No concluyas que toda memoria desaparece. Busca de nuevo las raíces y clasifícalas; las dos ramas estables pueden persistir en un intervalo. Para b₀=0,02 y a=3, la práctica encuentra las tres raíces por intervalos y verifica sus derivadas. El algoritmo no declara equilibrio a cada punto donde una curva se ve lenta: resuelve f(x)=0 y comprueba el residuo. [A01]

### De una célula a una población observada

Un reportero separado r puede satisfacer r′=b_r+V_r H(p)−γ_r r. Si necesita madurar, añade estados antes de convertirlo en intensidad. Una respuesta binaria observada puede depender de dinámica, ruido, heterogeneidad y transformación de lectura. Para el caso sintético primario, la distinción entre células de expresión baja y alta es parte central de la evidencia, que aquí se usa cualitativamente. No se asigna a nuestras raíces normalizadas el significado de intensidades medidas en ese estudio. [A25] [I04]

El promedio de una mezcla puede escribirse E[Y]=w μ_alta+(1−w)μ_baja si w es la fracción en la población alta. Un aumento de la media puede proceder de aumentar w, de elevar μ_alta o de ambas cosas. Por eso medir solo una media no permite reconstruir de forma única cómo responde cada célula. El modelo de observación y la unidad de muestreo son necesarios para decidir qué se ha aprendido. [A09] [A07]

### Caso B: construir un control de adaptación como aproximación local

En osmorregulación, una perturbación externa puede provocar una respuesta transitoria que luego se adapta. El trabajo de Muzzey y colaboradores relaciona adaptación de la respuesta de Hog1 y volumen celular con un mecanismo integrador que depende de su actividad y afecta a síntesis de glicerol. A continuación construimos una analogía lineal local para entender la propiedad de control; sus dos estados no son una descripción molecular completa de esa red. [A26]

Llama u a una perturbación externa en una escala normalizada; h a una desviación de la respuesta reguladora respecto al basal; g a una compensación acumulada en una escala compatible. Define h′=a(u−g)−b h y g′=c h. a y b tienen unidades inversa de tiempo si h,u,g comparten escala; c también las tiene. g reduce el error de entrada efectivo y h impulsa el aumento de compensación. Como h y g son desviaciones, h puede tomar valores negativos sin implicar una cantidad negativa de proteína. [A01]

### Derivar la adaptación antes de dibujarla

Para u constante, un equilibrio debe cumplir c h*=0. Si c>0, h*=0. Sustituir en la primera ecuación impone g*=u. La respuesta reguladora vuelve a su basal mientras la compensación mantiene un desplazamiento que contrarresta la entrada. Al integrar g′=c h, g(t)=g(0)+c∫h(s)ds. Ese estado almacena la integral de la desviación. La adaptación se obtiene de una identidad del balance, no ajustando una exponencial a una curva que vuelve hacia abajo. [A01] [A04]

¿Es estable ese equilibrio? El Jacobiano para (h,g) tiene filas (−b,−a) y (c,0). Su polinomio es λ²+bλ+ac. Para a,b,c positivos, los autovalores tienen parte real negativa. Si b²<4ac, son complejos conjugados y la aproximación vuelve mediante oscilaciones amortiguadas; si b²>4ac, las tasas de relajación son reales. «Amortiguadas» significa que disminuye su amplitud, no que exista un reloj autosostenido. [A02] [A27]

### Encontrar una solución analítica para comprobar el programa

Deriva h′ cuando u es constante: h″=−a g′−b h′=−ac h−b h′. Para h(0)=g(0)=0 y un escalón u₀ aplicado en cero, h′(0)=a u₀. Si ω=√(ac−b²/4) es real y positiva, la solución es h(t)=(a u₀/ω)e^{−bt/2}sin(ωt). La amplitud inicial de seno se elige para que su derivada en cero sea a u₀. Calcula después g=u₀−(h′+b h)/a a partir de la primera ecuación. [A02]

Elige a=b=c=u₀=1 en unidades coherentes. Entonces ω=√3/2. La señal h aumenta desde cero, alcanza un máximo y regresa al basal; g tiende a uno. La práctica 25 compara la integración con esta solución, lo que detecta signos o intercambio de estados en el código. Estos números y esta solución son docentes. [A02] [R05]

### Programar dos balances sin ocultar sus significados

```python
import numpy as np
from scipy.integrate import solve_ivp

def adaptacion(t, estado, a, b, c, entrada):
    h, g = estado
    error_efectivo = entrada - g
    dh = a * error_efectivo - b * h
    dg = c * h
    return np.array([dh, dg])

sol = solve_ivp(
    adaptacion, (0.0, 20.0), [0.0, 0.0],
    args=(1.0, 1.0, 1.0, 1.0),
    t_eval=np.linspace(0.0, 20.0, 401),
    rtol=1e-9, atol=1e-11,
)
if not sol.success:
    raise RuntimeError(sol.message)
respuesta = sol.y[0, :]
compensacion = sol.y[1, :]
```

`h, g = estado` desempaqueta dos valores en el orden acordado. Si inviertes esa línea sin cambiar todas las ecuaciones, mezclas los dos mecanismos. `error_efectivo` da un nombre a la diferencia entrada−compensación; ayuda a revisar el signo del lazo. `dh` y `dg` son tasas. El array retornado conserva primero h y después g. El solver no conoce la palabra «adaptación»: solo calcula a partir de esas dos funciones. [R20] [R05]

La entrada es constante en este tramo. Para un pulso o un cambio posterior, integra por intervalos con la entrada correspondiente y encadena estados. Añadir una fuga −δ_g g produce g′=c h−δ_g g. En equilibrio h*=δ_g u/[c+δ_g b/a], que no es cero para una entrada distinta de cero y fuga positiva. La derivación sale de sustituir g*=c h*/δ_g en el primer balance. Así se ve por qué una memoria que se pierde puede dejar un error residual. [A01] [A04]

### Qué une estos casos y qué los diferencia

La autoactivación y la adaptación usan el mismo método de trabajo: definir estados, construir tasas, buscar equilibrios, derivar estabilidad, programar y comprobar. Una genera dos posibles destinos bajo ciertas condiciones; la otra compensa una perturbación y recupera una respuesta basal. La palabra «feedback» no decide el comportamiento. Lo deciden la arquitectura, las leyes, las escalas y las hipótesis que has escrito. Los casos bacterianos, de levadura y vegetales se utilizan a lo largo del atlas para practicar ese razonamiento. [A01] [A25] [A26]
