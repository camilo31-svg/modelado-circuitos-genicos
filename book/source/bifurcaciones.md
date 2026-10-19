# Bifurcaciones y continuación: cuándo cambia la conducta del circuito

- Derivar las ecuaciones y justificar los supuestos del modelo presentado.
- Reproducir los cálculos y comprobar sus límites con un ejemplo resuelto.
- Relacionar las predicciones con observaciones y fuentes académicas.

## Seguir equilibrios cuando cambia un parámetro

Un análisis de bifurcaciones pregunta cuándo un cambio continuo de parámetros produce un cambio cualitativo de la dinámica: nace un equilibrio, cambia su estabilidad o aparece una órbita periódica. No es lo mismo que observar que una curva aumenta de amplitud. La introducción de Ingalls conecta estos cambios con la organización de estados celulares y circuitos [A01], §4.4.

Para f(x,μ)=0, imagina una rama de equilibrios x*(μ). Si ∂f/∂x no se anula, una variación pequeña de μ suele producir un desplazamiento suave de x*. Al derivar la condición estacionaria se obtiene dx*/dμ=−fμ/fx. Una pendiente muy grande puede anticipar proximidad a un punto donde la descripción de la rama como función única de μ falle [A01], §§4.4 y 4.5.

$$
\frac{dx^*}{d\mu}=-\frac{\partial f/\partial\mu}{\partial f/\partial x}.
$$

## Desarrollo guiado: de una ecuación a un diagrama de bifurcación

Una bifurcación es un cambio cualitativo de los estados o movimientos posibles al variar un parámetro. Vamos a obtenerla para x′=f(x;a)=a x²/(1+x²)−x. x y el tiempo son adimensionales. a aumenta la capacidad de autoactivación. El punto y coma separa visualmente estado y parámetro: no añade una operación matemática. [A01] [A02]

Para hallar equilibrios, iguala f a cero y factoriza x: x[a x/(1+x²)−1]=0. La primera posibilidad es x=0. Para x≠0, a x=1+x², o x²−a x+1=0. Por tanto, x₊=(a+√(a²−4))/2 y x₋=(a−√(a²−4))/2. El signo ± no representa incertidumbre: enumera dos raíces diferentes. Solo existen raíces reales adicionales si a²−4≥0; para producción a≥0, esto exige a≥2. [A01] [A02]

### Identificar la estabilidad sin simular cada punto

Deriva f respecto a x: f_x=2ax/(1+x²)²−1. En x=0 da −1, por lo que esa rama es estable. En una raíz positiva, usa a=(1+x²)/x y simplifica: f_x=2/(1+x²)−1=(1−x²)/(1+x²). La raíz pequeña, menor que uno, es inestable; la grande, mayor que uno, es estable. En a=2 ambas valen uno y f_x=0. Allí nacen juntas en un pliegue, también llamado bifurcación silla-nodo. El nombre geométrico no exige que estés representando una célula con forma de silla. [A01]

Un diagrama coloca el parámetro a en el eje horizontal y el equilibrio x* en el vertical. Cada punto pertenece a un modelo con un parámetro fijo. No es una trayectoria temporal: moverse hacia la derecha no significa avanzar el reloj. Una línea discontinua marca aquí una rama inestable, que suele no aparecer al integrar desde estados iniciales genéricos. Esa es la razón por la que un barrido de simulaciones puede ocultar parte del diagrama. [A01]

### Qué significa acercarse despacio a un equilibrio

Si una perturbación pequeña cumple ε′≈λ ε, su amplitud se multiplica por e^{λt}. Para λ<0, el tiempo de decaimiento por un factor e es −1/λ. Cerca del pliegue, λ=f_x se aproxima a cero desde valores negativos y ese tiempo aumenta. Es el enlentecimiento crítico del modelo local. No implica que cualquier señal lenta sea prueba de una bifurcación: también puede reflejar un parámetro de pérdida pequeño o una variable no observada. [A01] [A02]

En varios estados, la continuación numérica busca soluciones de f(x;a)=0 mientras ajusta a. Si la rama se dobla, imponer siempre a como variable independiente puede fallar. El método de pseudoarco añade una condición sobre la distancia recorrida en el espacio conjunto de estado y parámetro, de modo que el algoritmo puede seguir alrededor del pliegue. «Pseudoarco» no es una nueva ley biológica: es una elección de coordenada para resolver ecuaciones. [A01]

## Silla-nodo: crear o destruir una pareja

La forma local x'=μ−x² tiene dos equilibrios si μ>0: x*=±√μ. La derivada −2x* hace estable la raíz positiva e inestable la negativa. Para μ<0 no hay equilibrio real. En μ=0 ambas ramas se tocan y el autovalor es cero. Es una forma normal matemática; sus coordenadas pueden ser desviaciones respecto a una concentración positiva y no concentraciones absolutas [A01], §4.4; [A02].

No basta encontrar f=0 y fx=0 para certificar una silla-nodo genérica. En esta forma, fμ≠0 y fxx≠0 aseguran que el parámetro despliega el cruce y que hay curvatura de segundo orden. Si esos términos también se anulan, puede haber una degeneración y se necesita otro análisis. En redes de varias variables, el análogo exige estudiar el autovalor crítico y los demás modos [A02] [A01].

El tiempo local de relajación cerca de la raíz estable es 1/(2√μ). Crece cuando μ se acerca a cero desde arriba. Ese enlentecimiento explica por qué un barrido numérico con un tiempo de espera fijo puede dar la impresión de que el sistema aún no se ha estabilizado cerca del umbral. El ruido y el régimen de observación complican cualquier uso experimental del enlentecimiento como indicador de transición [A01], §§4.2 y 4.4.

## Una bifurcación que se puede calcular en una autoactivación

Considera x'=a·x²/(1+x²)−x, con x≥0. El origen es equilibrio para todo a. Los equilibrios positivos cumplen a·x=1+x² y, por tanto, x²−ax+1=0. Si a>2 hay dos raíces positivas; en a=2 se unen en x=1; si a<2 no hay raíces positivas. Es un ejemplo original de autoactivación que aplica las herramientas de Ingalls [A01], §§4.4 y 7.1.2.

$$
x_\pm^*=\frac{a\pm\sqrt{a^2-4}}{2}.
$$

En una raíz positiva, sustituir a=(1+x²)/x en f' da f'=(1−x²)/(1+x²). La raíz menor que uno es inestable y la mayor es estable. El origen tiene f'(0)=−1 y permanece estable. Para a>2 coexisten un estado bajo en cero y un estado alto, separados por el equilibrio inestable. Una producción basal positiva desplaza la rama de cero y modifica los umbrales; debes recalcularlos [A01].

Para a=3, las raíces son (3±√5)/2≈0,382 y 2,618. Un estado inicial por debajo de 0,382 converge al origen, y uno por encima converge al estado alto en este modelo escalar. La figura de bifurcación utiliza líneas continuas para ramas estables y discontinuas para inestables; esas convenciones deben explicarse en la leyenda [A01], §4.4.

## Horquilla y transcrítica: reconocer la simetría y sus límites

En x'=μx−x³, el equilibrio x=0 existe siempre. Para μ>0 aparecen x=±√μ. La simetría x↦−x organiza una horquilla supercrítica. Una asimetría pequeña, por ejemplo añadir una constante, puede romper esa estructura. En un interruptor perfectamente simétrico puede surgir una organización relacionada, pero una célula real no tiene por qué conservar esa simetría exacta [A02] [A01].

La forma x'=μx−x² contiene las ramas x=0 y x=μ, que intercambian estabilidad al cruzarse: es una bifurcación transcrítica. Si la variable representa concentración, la rama negativa no pertenece al dominio físico. Dibujar todo el diagrama matemático puede ser útil para entender la estructura, siempre que se marque qué parte es biológicamente admisible [A02].

## Hopf: cuando la estabilidad se pierde mediante un modo oscilatorio

Una bifurcación de Hopf implica que una pareja de autovalores complejos cruza el eje imaginario, con frecuencia no nula y condiciones adicionales de no degeneración. En dos dimensiones, T=0 y Δ>0 son condiciones lineales candidatas. No bastan para decidir si nace un ciclo estable ni su amplitud: los términos no lineales deciden el tipo y la estabilidad de la órbita [A01], §§4.3 y 4.4; [A02].

La forma radial r'=μr−r³, junto con φ'=ω, ilustra el caso supercrítico. Para μ<0 el origen atrae; para μ>0 aparece r*=√μ, un ciclo atractivo de período 2π/ω. Si cambia el signo del término cúbico y se añaden términos que limiten la amplitud, pueden aparecer ramas inestables e histéresis. No todo comienzo de oscilación es gradual ni todo ciclo se detecta desde una sola condición inicial [A02] [A01].

## Continuación numérica frente a un barrido de simulaciones

Un barrido integra el sistema para muchos valores de un parámetro y registra el resultado alcanzado. Normalmente muestra atractores; las ramas inestables no se alcanzan de manera robusta. La continuación resuelve f(x,μ)=0 y sigue la rama, incluso cuando es inestable, mientras calcula autovalores o indicadores equivalentes. Ambas técnicas responden a preguntas distintas [A01], §4.4.

El procedimiento más sencillo usa el equilibrio del parámetro anterior como arranque del siguiente. Puede fallar en un pliegue porque x deja de ser una función univaluada de μ. La continuación por pseudo-longitud de arco trata estado y parámetro como incógnitas y añade una condición geométrica que permite doblar el pliegue. Es una herramienta avanzada; un barrido denso no es un sustituto equivalente [A02] [A01].

Para un tutorial en Python, puedes comprobar el caso escalar calculando las raíces analíticas y clasificándolas con f'. En un circuito mayor, empieza por buscadores de raíces desde varios arranques y verifica el residuo ‖f(x*,μ)‖. Después usa un programa de continuación adecuado si necesitas ramas completas. Ningún buscador de raíces garantiza haber encontrado todas las soluciones solo porque informa convergencia [A01], §§4.4 y 4.6; [R15].

## Criterios de lectura de un diagrama

Identifica qué eje es una entrada controlada y cuál es un parámetro interno. Si la entrada real altera simultáneamente varias tasas, recorrer una sola constante puede representar una intervención que no existe. Comprueba además si los estados se muestran en unidades físicas o normalizados y si la curva corresponde a equilibrios, máximos de ciclos o una muestra a tiempo fijo [A01], capítulos 1 y 4.

En una órbita periódica, mostrar máximo y mínimo por parámetro resume amplitud, pero no informa por sí solo del período ni distingue oscilaciones complejas de ruido. Para sospechas de duplicación de período o caos, hacen falta observaciones de largo plazo, convergencia numérica y análisis adicionales. El estudio teórico de osciladores acoplados muestra por qué conviene separar esas categorías [A06].

## Problema resuelto y práctica computacional

Para la autoactivación del ejemplo, a=2,5 da raíces x=0,5 y x=2. Sus pendientes son 0,6 y −0,6, respectivamente; el origen tiene pendiente −1. El estado inicial 0,4 cae al origen y el estado 0,6 se acerca a 2. Aumentar a no obliga al sistema que está exactamente en cero a salir de allí, porque la producción también es cero en ese estado. Una fuga o perturbación cambia ese detalle [A01].

La práctica propuesta calcula residuos de todas las raíces, clasifica estabilidad y compara un barrido ascendente con otro descendente usando el estado final anterior. Repite con un tiempo de espera mayor. Si el lazo cambia por no haber relajado, has observado un efecto dinámico; si persiste en el límite lento y hay ramas coexistentes, puedes relacionarlo con la estructura estacionaria. Es una comprobación original que aplica los criterios de los apartados anteriores [A01] [A02].
