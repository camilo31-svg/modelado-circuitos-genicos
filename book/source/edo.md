# Retomar las ecuaciones diferenciales: del balance a la solución

- Derivar las ecuaciones y justificar los supuestos del modelo presentado.
- Reproducir los cálculos y comprobar sus límites con un ejemplo resuelto.
- Relacionar las predicciones con observaciones y fuentes académicas.

## El punto de partida: una ley de cambio y una condición inicial

Vamos a empezar directamente donde hace falta recuperar soltura: resolver e interpretar ecuaciones diferenciales. Una ecuación diferencial ordinaria, o EDO, relaciona una función desconocida del tiempo con su derivada. En un modelo génico, la incógnita suele ser una abundancia de ARN o proteína. Escribir la ecuación es proponer cómo cambia esa abundancia; resolverla es encontrar una trayectoria que obedezca la ley en cada instante. Esta distinción entre mecanismo, ecuación y trayectoria organiza el modelado dinámico de Ingalls [A01], §§1.2 y 2.1.

Considera una proteína X producida a una tasa constante α y retirada a una tasa proporcional a su abundancia. Si x está en nM y t en horas, α se expresa en nM/h y δ en h⁻¹. La ley de balance y la condición inicial son dos datos diferentes [A01], §2.1:

$$
\frac{dx}{dt}=\alpha-\delta x,\qquad x(0)=x_0.
$$

La ecuación establece la pendiente en cualquier punto del plano tiempo–abundancia. La condición inicial escoge una trayectoria entre todas las que cumplen esa ley. Dos células con el mismo modelo y los mismos parámetros pueden seguir curvas distintas porque empiezan con cantidades distintas. El término δx no significa que en cada hora desaparezca una cantidad fija; significa que la retirada por unidad de tiempo aumenta con el número de moléculas disponibles. La aproximación de primer orden es una hipótesis cinética que debe contrastarse [A01], §2.1.

Conviene escribir el modelo general como dx/dt = f(t,x;θ), con θ el conjunto de parámetros. Una entrada u(t), por ejemplo una señal externa, puede aparecer dentro de f. Los estados necesitan condiciones iniciales; las entradas necesitan una definición temporal; los parámetros necesitan un valor o una distribución. Confundir estas tres funciones produce problemas que ningún algoritmo numérico puede corregir [A01], §§1.5 y 4.6.

## Recuperar la separación de variables sin perder soluciones

Empieza por la desaparición pura, dx/dt = −δx. Para x positivo puedes dividir por x e integrar. La manipulación separa las variables, pero recuerda que x = 0 también es solución y se perdería si dividieras por x sin examinarla. La forma correcta de usar esta técnica incluye comprobar los puntos donde el divisor se anula [F08]; el modelo de reacción que la motiva aparece en Ingalls [A01], §2.1.

$$
\frac{1}{x}\frac{dx}{dt}=-\delta
$$

Integra entre el estado inicial y el estado actual. Así evitas introducir una constante que luego haya que recuperar. El logaritmo se aplica al cociente x(t)/x₀, una cantidad sin dimensiones; escribir logaritmos de concentraciones con unidades oculta esa normalización [F08] [A01].

$$
\ln\!\left(\frac{x(t)}{x_0}\right)=-\delta t,
\qquad x(t)=x_0e^{-\delta t}.
$$

Deriva la expresión final y comprueba la condición inicial. La derivada es −δx₀e⁻ᵟᵗ, que coincide con −δx(t); al sustituir t = 0 recuperas x₀. Esta comprobación es parte de la solución, no un trámite. Si δ = 0, la trayectoria es constante y la fórmula también lo recoge. Si x₀ = 0, la solución es cero aunque la derivación con el cociente no fuera válida para ese caso [A01] [F08].

Ejemplo propio: si x₀ = 40 nM y δ = 0,2 h⁻¹, al cabo de 5 h quedan 40/e ≈ 14,72 nM. El tiempo característico es 1/δ = 5 h. La semivida es ln(2)/δ ≈ 3,47 h. Son dos maneras diferentes de resumir el mismo decaimiento; ninguna es el momento en que desaparecen todas las moléculas. Estos números son docentes y se obtienen directamente de la solución anterior [A01] [F08].

## Producción y pérdida: desplazar la incógnita

Vuelve al balance con producción. Primero busca un valor que no cambie: si dx/dt = 0, α − δx* = 0 y x* = α/δ, siempre que δ sea positivo. Ahora define z(t) = x(t) − x*. Como x* es constante, dz/dt = dx/dt. Al sustituir x = z + x*, los términos constantes se cancelan. El problema se convierte en el decaimiento que acabas de resolver [A01], §§2.1 y 4.2.

$$
\frac{dz}{dt}=-\delta z,
\qquad z(0)=x_0-\frac{\alpha}{\delta}.
$$

$$
x(t)=\frac{\alpha}{\delta}+\left(x_0-\frac{\alpha}{\delta}\right)e^{-\delta t}.
$$

Esta forma separa tres componentes: el destino α/δ, la distancia inicial hasta ese destino y la velocidad con la que esa distancia disminuye. Si x₀ está por debajo de x*, la trayectoria sube; si está por encima, baja. El signo de la derivada depende de esa distancia. En este modelo de una variable no hay sobrepaso del equilibrio: la diferencia x − x* mantiene su signo [A01], §§2.1 y 4.2.

Ejemplo propio: α = 12 nM/h y δ = 0,3 h⁻¹ dan x* = 40 nM. Desde x₀ = 5 nM, a las 4 h se obtiene x = 40 − 35e⁻¹·² ≈ 29,46 nM. El valor 0,3 no es la pendiente inicial: esta vale 12 − 0,3·5 = 10,5 nM/h. La pendiente va disminuyendo porque la pérdida aumenta a medida que se acumula proteína. El tiempo para completar el 90 % de la distancia inicial es ln(10)/δ ≈ 7,68 h [A01].

Si δ = 0, no uses α/δ. La ecuación original queda dx/dt = α y la solución es x₀ + αt. No hay equilibrio finito si α es positivo. Examinar un límite obliga a volver a las hipótesis del modelo: una pérdida exactamente nula cambia la conducta a largo plazo [A01], §2.1.

## Factor integrante: una herramienta que sirve para entradas variables

La sustitución anterior es cómoda con producción constante. Para una tasa de producción a(t), la ecuación lineal se escribe x' + δx = a(t). Multiplica por eᵟᵗ. La regla del producto permite reconocer el lado izquierdo como una sola derivada. Esta derivación utiliza técnicas estándar de EDO lineales y prolonga el balance de primer orden de Ingalls [A01]; para el método formal, consulta [A02].

$$
e^{\delta t}x'+\delta e^{\delta t}x
=\frac{d}{dt}\left(e^{\delta t}x\right)
=e^{\delta t}a(t).
$$

Integra entre 0 y t y despeja x(t). Aparecen la memoria del estado inicial y una suma ponderada de toda la producción anterior. La ponderación depende de cuánto tiempo ha transcurrido desde que se produjo cada contribución [A01] [A02].

$$
x(t)=x_0e^{-\delta t}+\int_0^t e^{-\delta(t-s)}a(s)\,ds.
$$

El tiempo s recorre el pasado y t es el momento de observación. Una cantidad producida cerca del instante actual se conserva casi por completo; una producida hace mucho tiempo se ha reducido por degradación. Por eso una proteína funciona como un filtro temporal: su señal puede continuar elevada después de que la producción haya disminuido. Esta interpretación es válida para el modelo lineal con δ constante, sin exigir un mecanismo molecular concreto de regulación [A01], §§6.6 y 7.1.

Si la retirada también cambia con el tiempo, define D(t) = ∫₀ᵗδ(r)dr. El factor integrante pasa a ser eᴰ⁽ᵗ⁾. El balance conserva su estructura, pero la memoria ya no depende solamente de la diferencia t − s [A02].

$$
x(t)=e^{-D(t)}\left[x_0+\int_0^t e^{D(s)}a(s)\,ds\right].
$$

## Entradas por tramos y pulsos: enlazar soluciones

Supón que la producción es α hasta t = T y luego se apaga. Integra el primer tramo y calcula x(T). Ese valor es la condición inicial del segundo tramo. La concentración permanece continua si el cambio de entrada no añade ni retira instantáneamente moléculas; lo que puede saltar es la pendiente. Esta continuidad se desprende del balance, no de una preferencia estética al dibujar curvas [A01], §§2.1 y 6.3.

$$
x(t)=x(T)e^{-\delta(t-T)},\qquad t\geq T.
$$

Ejemplo propio: desde cero, α = 10 nM/h, δ = 0,5 h⁻¹ y T = 2 h producen x(T) = 20(1 − e⁻¹) ≈ 12,64 nM. Dos horas después del apagado quedan unos 4,65 nM. Un observador que solo mire la abundancia al finalizar el pulso podría interpretar que la señal de entrada sigue presente. Lo que persiste es el estado molecular. Resolver por tramos permite separar ambas cosas sin invocar memoria en el ADN ni un circuito biestable [A01].

Cuando programes pulsos, integra cada intervalo de forma explícita o controla el paso del integrador cerca de cada discontinuidad. Pedir resultados en t = T con `t_eval` no obliga a que el algoritmo haya usado un paso interno justo allí. La documentación de `solve_ivp` distingue los tiempos de salida de los pasos de integración [R05].

## Ecuaciones no lineales: saber qué deja de funcionar

La ecuación x' = α/(1 + x/K) − δx sigue siendo una EDO de una sola variable, pero ya no es lineal en x. El principio de sumar soluciones deja de ser válido. Que cada término por separado resulte sencillo no garantiza una expresión cerrada manejable para toda la trayectoria. Puedes estudiar equilibrio, signo de la derivada y estabilidad sin resolverla explícitamente [A01], §§4.1, 4.2 y 7.1.2.

Una diferencia importante aparece entre ecuación y sistema. Para ARN m y proteína p, conocer p no determina por sí solo su pendiente si la producción depende de m. El estado completo debe incluir ambos. Escribir una sola ecuación para p exige una aproximación que elimine m, o una ecuación de orden superior acompañada de condiciones iniciales adicionales. La reducción de variables debe justificarse por escalas o por una relación algebraica apropiada [A01], §§2.2 y 7.1.

## Existencia, unicidad y dominio biológico

En regiones donde f es continua y suficientemente regular respecto al estado, un problema de valor inicial tiene una solución local única. La palabra local importa: algunas ecuaciones pueden crecer sin límite en tiempo finito. El criterio habitual de regularidad es una condición de Lipschitz local; no hace falta demostrarla desde cero en cada modelo polinómico, pero sí examinar singularidades y denominadores que puedan anularse [A02].

La no unicidad se puede ver sin biología: x' = √|x|, x(0) = 0, admite permanecer en cero durante un tiempo y empezar a crecer después. La función de la derecha no es Lipschitz en cero. En contraste, los balances de masa de acción con un número finito de especies son funciones polinómicas y son localmente regulares. Eso no demuestra por sí solo que toda solución exista para cualquier tiempo; la conservación o una cota de crecimiento puede proporcionar la protección adicional [A01] [A02].

Para concentraciones no negativas, revisa cada frontera xᵢ = 0: allí la derivada no debería apuntar hacia valores negativos si el resto de los estados es válido. En x' = α − δx, f(0) = α ≥ 0. En un modelo de consumo, una reacción que necesita X debe detenerse cuando X = 0. Un integrador puede dar pequeños valores negativos por error numérico aunque la ecuación conserve positividad; recortar automáticamente todos los negativos oculta la causa y puede romper la conservación [A01], §§2.1 y 2.2; [R05].

## Problema completo con solución razonada

Una proteína parte de x₀ = 2 nM. Durante 3 h se produce a 6 nM/h y se retira con δ = 0,25 h⁻¹. Después la producción pasa a 1 nM/h. Calcula la abundancia a las 5 h y decide si seguirá subiendo. Es un ejercicio original de aplicación del balance lineal [A01] [A02].

En el primer tramo x* = 24 nM y x(3) = 24 − 22e⁻⁰·⁷⁵ ≈ 13,61 nM. En el segundo, el nuevo equilibrio es 4 nM. Transcurridas otras 2 h, x(5) = 4 + [x(3) − 4]e⁻⁰·⁵ ≈ 9,83 nM. La pendiente en ese instante es 1 − 0,25·9,83 ≈ −1,46 nM/h. La proteína disminuye aunque todavía se produzca. El signo del balance neto depende de ambas tasas [A01].

Comprueba ahora tres límites: con un segundo tramo muy largo, x tiende a 4; si la producción del segundo tramo fuera cero, tendería a cero; si ambas tasas de producción fueran iguales, la unión por tramos recuperaría una sola trayectoria. Estas pruebas detectan errores de signo, de unidades y de desplazamiento del tiempo. Puedes realizarlas con papel antes de programar [A01] [R05].

## Qué debes poder hacer antes de continuar

No necesitas memorizar todas las fórmulas. Debes poder reconstruir la solución de producción y pérdida, identificar la condición inicial, enlazar un pulso sin inventar saltos, comprobar unidades y explicar qué conserva memoria del pasado. Las técnicas de análisis cualitativo y la simulación se añaden a esta base; no sustituyen la lectura de cada término del balance [A01], capítulos 2 y 4.
