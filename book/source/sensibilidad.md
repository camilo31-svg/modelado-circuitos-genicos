# Sensibilidad local y global: qué controla las predicciones

- Derivar las ecuaciones y justificar los supuestos del modelo presentado.
- Reproducir los cálculos y comprobar sus límites con un ejemplo resuelto.
- Relacionar las predicciones con observaciones y fuentes académicas.

## Especificar la salida antes de preguntar qué parámetro importa

Una sensibilidad mide cómo cambia una cantidad elegida al modificar un parámetro. Esa cantidad puede ser concentración a una hora, equilibrio, período, amplitud, área o probabilidad de conmutación. El orden de importancia puede cambiar entre salidas y tiempos. No existe una clasificación única de parámetros importantes para todo el modelo [A01], §4.5.

Para y(θ), la sensibilidad dimensional es ∂y/∂θ. Su unidad depende de ambas magnitudes. La sensibilidad normalizada S=(θ/y)∂y/∂θ equivale a ∂ln y/∂lnθ cuando y y θ son positivos. Informa del cambio relativo de salida ante un cambio relativo pequeño de parámetro. Cerca de y=0, esa normalización puede divergir y dejar de ser útil [A01], §4.5.1.

## Un ejemplo analítico que separa equilibrio y tiempo

Para x(t)=α/δ·(1−e⁻ᵟᵗ), desde cero, ∂x/∂α=x/α y la sensibilidad normalizada a α es uno. La sensibilidad respecto a δ contiene tanto el cambio de equilibrio como el de velocidad. Derivar la expresión completa da el siguiente resultado original [A01], §§4.5 y 2.1.

$$
\frac{\partial x}{\partial\delta}
=-\frac{\alpha}{\delta^2}(1-e^{-\delta t})
+\frac{\alpha t}{\delta}e^{-\delta t}.
$$

En tiempos muy cortos x≈αt, de modo que el efecto de δ es pequeño. En tiempos largos x≈α/δ y la sensibilidad normalizada a δ tiende a −1. Muestrear únicamente al principio ayuda a estimar producción, pero puede informar poco sobre la pérdida. La elección de tiempos cambia lo que puedes aprender [A01], §§4.5 y 4.6; [I06].

## Integrar ecuaciones de sensibilidad

Para x'=f(x,θ,t), define Sⱼ=∂x/∂θⱼ. Deriva ambos lados respecto al parámetro y aplica la regla de la cadena: Sⱼ'=JₓSⱼ+∂f/∂θⱼ. La condición inicial es ∂x₀/∂θⱼ, que no siempre vale cero. Si estimas un estado inicial o este depende de un equilibrio previo, esa dependencia forma parte de la sensibilidad [A01], §4.5.2.

$$
\frac{dS_j}{dt}=J_xS_j+\frac{\partial f}{\partial\theta_j}.
$$

El sistema ampliado contiene los estados originales y una columna de sensibilidades por parámetro. Si observas y=h(x,φ), la sensibilidad de la salida incluye hₓSⱼ y, cuando corresponda, la derivada directa de h respecto a un parámetro de medida. Ignorar ganancia o fondo en esa derivada puede dar una impresión falsa de información sobre tasas biológicas [A01], §§4.5 y 4.6; [I06].

## Diferencias finitas y comprobaciones de derivadas

Una diferencia central aproxima ∂y/∂θⱼ por [y(θ+h eⱼ)−y(θ−h eⱼ)]/(2h). Un h grande introduce error de truncación; uno demasiado pequeño amplifica cancelación y error numérico del solver. Repite con una familia de pasos y busca una región estable, ajustando la tolerancia de integración para que no domine la diferencia [A01], §4.5; [R05].

Para parámetros positivos suele resultar más natural perturbar η=lnθ. Un paso en η representa una perturbación relativa y evita valores negativos. La derivada respecto a η es θ·∂y/∂θ. No normalices dos veces si ya has cambiado a logparámetros. Registra siempre en qué coordenadas calculaste la sensibilidad [A01], §4.5; [I05].

## Sensibilidad local no es incertidumbre paramétrica

Una derivada grande dice que una perturbación pequeña afecta a la salida. No indica cuánta incertidumbre tiene el parámetro. Un parámetro muy sensible medido con precisión puede aportar poca incertidumbre final; uno moderadamente sensible y muy incierto puede aportar más. Para propagación local, la covarianza aproximada de salida es Jθ·Cov(θ)·Jθᵀ [A01], §§4.5 y 4.6; [A09].

Las correlaciones importan. Si α y δ cambian juntos conservando α/δ, una salida estacionaria puede permanecer casi fija aunque cada parámetro varíe mucho. Propagar incertidumbre usando intervalos independientes rompe esa estructura y puede exagerar o distorsionar predicciones. Usa una distribución conjunta coherente con el ajuste o con el conocimiento previo [I06] [A10] [A09].

## Sensibilidad global y descomposición de varianza

Una sensibilidad global explora un rango o una distribución de parámetros. Debes declarar esa distribución: la conclusión depende de qué valores consideras posibles y cómo los ponderas. Variar cada parámetro por un factor dos no equivale a analizar una distribución posterior correlacionada [A08] [A10].

Para entradas independientes y salida escalar Y, un índice de primer orden de Sobol es Sᵢ=Var(E[Y|θᵢ])/Var(Y). El índice total es STᵢ=E[Var(Y|θ₋ᵢ)]/Var(Y). El primero mide la contribución individual; el total incluye interacciones con otros factores. Las fórmulas y estimadores requieren atención a independencia, muestreo y error de Monte Carlo [A08].

Si los parámetros están correlacionados, la atribución de varianza necesita otro tratamiento o una interpretación condicionada explícita. No apliques sin más una implementación que presume independencia a muestras de una posterior con correlaciones fuertes. La distribución de entrada es parte de la pregunta científica, no un detalle técnico del software [A08] [A09].

## Ejemplo global que puedes resolver a mano

Supón Y=AB, con A y B independientes y uniformes en [0,1]. E[Y]=1/4 y E[Y²]=1/9, por lo que Var(Y)=7/144. Como E[Y|A]=A/2, su varianza es 1/48. El índice de primer orden de A vale (1/48)/(7/144)=3/7; el de B es igual. El resto 1/7 corresponde a interacción. Es una derivación original de las definiciones de varianza [A08] [A09].

El índice total de A es 1−SB=4/7, y lo mismo para B. Los totales suman 8/7 porque la interacción se cuenta en ambos. Esa suma mayor que uno no es un error. En cambio, sumar contribuciones de primer orden más todas las interacciones de una descomposición válida sí recupera uno [A08].

## Cambios cualitativos y discontinuidad de la salida

Si defines la salida como probabilidad de cambiar de cuenca o como existencia de una oscilación, una pequeña variación puede cambiar la categoría. Una derivada local de concentración puede no capturar ese fenómeno. Usa diagramas de régimen y una definición precisa del evento, con tiempos de observación suficientes. Cerca de una bifurcación puede ser necesario estudiar estructura y no solo elasticidades [A01], §§4.4 y 4.5.

La práctica calcula sensibilidades analíticas y numéricas del balance lineal, integra sensibilidades de un modelo de dos etapas y compara incertidumbre con y sin correlación de parámetros. Después añade un barrido de régimen del interruptor. Esa secuencia permite identificar qué conclusión corresponde a derivadas locales y cuál a cambios de atractor [A01] [I06].
