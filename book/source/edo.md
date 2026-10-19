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

## Desarrollo guiado: leer, transformar y verificar una EDO

Una ecuación no se entiende solamente por reconocer su nombre. Vamos a recorrer el balance x′=α−δx como si lo hubiéramos propuesto nosotros. La letra x representa una concentración; x(t) recuerda que su valor depende del tiempo. El símbolo prima significa derivar respecto al tiempo y equivale a dx/dt. α, que se lee «alfa», representa una entrada de concentración por tiempo. δ, «delta», es una constante de pérdida por tiempo. Un parámetro es una cantidad que el modelo mantiene fija durante esta simulación; no significa que la naturaleza la mantenga fija en cualquier circunstancia. El estado x necesita un valor inicial; los parámetros necesitan valores, unidades y un ámbito de validez. [A01] [A02]

| Elemento | Qué significa aquí | Unidad si x está en nM y t en h |
|---|---|---|
| t | Tiempo desde el inicio del registro | h |
| x(t) | Concentración que queremos predecir | nM |
| x₀ | Concentración al comenzar | nM |
| α | Producción constante por volumen | nM/h |
| δ | Probabilidad efectiva de retirada por unidad de tiempo | 1/h |
| δx | Pérdida total de concentración por tiempo | nM/h |
| x* | Un valor del estado que no cambia | nM |

Las unidades de α y δ son diferentes porque representan mecanismos diferentes. Si δ=0,2 h⁻¹ y x=10 nM, la pérdida instantánea es 2 nM/h. Si x pasa a 30 nM, la pérdida pasa a 6 nM/h aunque δ permanezca igual. La retirada por primer orden es una hipótesis sobre cada molécula o sobre una aproximación efectiva del mecanismo. El producto δx no es un término que se añade para que la curva tenga buena forma. [A01]

### Por qué se empieza buscando un equilibrio

El asterisco no es multiplicación: etiqueta un estado estacionario. Estacionario significa que su derivada vale cero. Por tanto, sustituimos x′ por cero, despejamos δx*=α y dividimos entre δ, siempre que δ≠0. Aparece x*=α/δ. La operación responde a una pregunta física: ¿a qué concentración la producción iguala a la pérdida? Ese número no dice cuánto se tarda en llegar ni si todas las trayectorias llegarán. [A01] [A02]

Para resolver la trayectoria completa, resta ese equilibrio. Define z=x−x*. Como x* es constante, z′=x′. Sustituir x=z+x* en α−δx da α−δz−δx*. Ya sabemos que δx*=α: los dos términos constantes se cancelan. Queda z′=−δz. No hemos supuesto que z sea pequeña; para esta ecuación lineal la transformación es exacta. En modelos no lineales, una aproximación alrededor del equilibrio será local y habrá que distinguirla de esta igualdad. [A01] [A02]

### Integrar sin esconder la constante inicial

Para z≠0, divide por z: z′/z=−δ. La regla de la cadena dice que la derivada de ln|z(t)| es z′/z. Integra desde 0 hasta t: ln|z(t)|−ln|z(0)|=−δt. La diferencia de logaritmos equivale al logaritmo del cociente de sus argumentos. Al exponenciar, |z(t)|=|z(0)|e⁻ᵟᵗ. La solución no atraviesa cero en tiempo finito cuando z(0)≠0, por lo que conserva el signo inicial. Recuperas z(t)=z(0)e⁻ᵟᵗ. Si z(0)=0, la solución es z=0 directamente, sin dividir por ella. [A02]

Finalmente sustituye z(0)=x₀−α/δ y suma x*. Así se obtiene la fórmula de producción y pérdida. Cada pieza tiene una función: α/δ fija el destino; x₀−α/δ fija la distancia inicial con signo; la exponencial reduce esa distancia. Una exponencial que multiplica una distancia no significa que toda la concentración esté creciendo exponencialmente. [A01]

### Tres comprobaciones que sustituyen a memorizar

Primera: en t=0, e⁰=1, y la fórmula debe devolver exactamente x₀. Segunda: deriva toda la expresión; su derivada debe ser α−δx(t) al sustituir la solución. Tercera: si δ>0 y t aumenta mucho, la exponencial tiende a cero y queda α/δ. Si cualquiera de estas comprobaciones falla, no ajustes números para disimularlo: revisa el signo, el factor δ o la condición inicial. Un caso con α=0 debe reducirse al decaimiento puro. El caso δ=0 se resuelve en la ecuación original porque la expresión α/δ deja de existir. [A01] [A02]

Para el problema por tramos, x(3)=24−22e⁻⁰·⁷⁵ es un resultado del primer intervalo, no un parámetro nuevo. Ese valor pasa a ser el estado inicial del segundo. El segundo reloj es t−3: a las 5 h del experimento han pasado 2 h desde el cambio. Este cambio de origen temporal es la causa de muchos errores al programar pulsos. Puedes dibujar dos ejes de tiempo alineados y escribir debajo «experimento: 0,3,5» y «segundo intervalo: 0,2». [A01] [R05]

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


## Leer el inicio, el recorrido y el final de una curva

Una curva no representa necesariamente «un parámetro que cambia». **Estado** es una cantidad que el modelo calcula a lo largo del tiempo, como la concentración de una enzima E(t). **Parámetro constante** es una cantidad fijada para una simulación, como una tasa de pérdida δ. **Entrada** es una condición que imponemos al modelo, como un represor R(t). Una **tasa efectiva** es un flujo calculado con estados o entradas: puede cambiar aunque sus parámetros permanezcan constantes. Lee estas cuatro funciones antes de interpretar una subida o una bajada [A01], §§2.1, 3 y 7.1; [A02].

En las figuras cuantitativas del atlas, un círculo señala el primer punto trazado, un cuadrado uno intermedio y un rombo el último. Debajo de la figura se indican sus coordenadas, las unidades de ambos ejes, el rango recorrido y las condiciones que permanecen fijas o cambian. Los valores proceden de los mismos datos que generan los gráficos; se redondean para facilitar la lectura. **Último punto dibujado no significa equilibrio**: una oscilación continúa y una relajación puede acercarse al límite sin alcanzarlo. Los símbolos de extremos no convierten una nulclina o una distribución en una evolución temporal [A01], §§4.1–4.4; [A02].

Considera una enzima producida bajo represión. Usaremos un balance reducido E′=s(R)−δE. E se mide en nM y s en nM/h; δ se mide en h⁻¹. La producción efectiva es s(R)=smax/[1+(R/K)ⁿ]. smax=12 nM/h fija la capacidad máxima, K=5 nM la escala de entrada, n=2 la forma de la regulación y δ=0,3 h⁻¹ la pérdida por unidad de enzima. Estas cuatro constantes **no cambian durante el ejemplo**. La representación resume la expresión sin un estado explícito de ARN y no describe la catálisis de un sustrato por la enzima [A01], §§7.1–7.2; [D07].

Al inicio fijamos R=1 nM. Entonces R/K=0,2, su cuadrado vale 0,04 y s=12/1,04≈11,538 nM/h. Elegimos E(0)=s/δ≈38,462 nM. Producción y pérdida coinciden: δE≈11,538 nM/h; por eso E permanece horizontal hasta que cambie la condición. No está desapareciendo enzima neta, aunque hay producción y retirada simultáneas [A01], §§2.1 y 4.2.

En t=5 h hacemos subir R a 10 nM. Ahora R/K=2, su cuadrado vale 4 y s=12/5=2,4 nM/h. R sube y s baja de inmediato según nuestra hipótesis de regulación instantánea. E sigue siendo aproximadamente 38,462 nM justo después del cambio: su balance tiene tasas finitas, de modo que su concentración no salta. La nueva pendiente es 2,4−0,3·38,462≈−9,138 nM/h. Esa resta explica el inicio del descenso [A01], §§2.1, 4.1 y 7.1; [A02].

Para t≥5 h, el nuevo equilibrio es E*=2,4/0,3=8 nM. La solución por tramos conserva el estado alcanzado en el instante del cambio:

$$E(t)=8+\left(\frac{12}{1.04\cdot0.3}-8\right)e^{-0.3(t-5)},\qquad t\geq5.$$

En t=25 h han transcurrido 20 h desde el escalón. El exceso inicial respecto a 8 nM se multiplica por exp(−6), y queda E(25)≈8,076 nM. Su pendiente todavía es ligeramente negativa. **No ha disminuido δ**: ha disminuido E, y con ella la tasa de pérdida δE. Tampoco ha disminuido smax: ha aumentado la represión y por ello se utiliza una fracción menor de esa capacidad. Esta diferencia entre constante, entrada, estado y flujo es la lectura que debes reproducir en otros modelos [A01], §§2.1 y 7.1; [A02].

Cuando un gráfico compara varias δ o varios K, cada curva suele mantener un valor fijo distinto. Eso es una comparación entre simulaciones. Para afirmar que δ cambia durante una misma curva hay que definir δ(t), indicar el instante o la regla del cambio y resolver ese modelo. Del mismo modo, en una curva de Hill el eje horizontal recorre valores de una entrada, y en una bifurcación recorre un parámetro: moverse de izquierda a derecha no representa automáticamente el paso del tiempo [A01], §§3.3 y 4.4; [A02].
