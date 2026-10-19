# Más allá de la transcripción: cascadas, fosforilación y secuestro molecular

- Derivar las ecuaciones y justificar los supuestos del modelo presentado.
- Reproducir los cálculos y comprobar sus límites con un ejemplo resuelto.
- Relacionar las predicciones con observaciones y fuentes académicas.

## Una red de regulación puede actuar sobre estados de una proteína

La transcripción es una manera de cambiar actividad, pero no la única. Una proteína puede pasar entre estados de modificación que tienen actividades distintas. El total puede permanecer casi constante mientras su fracción activa cambia rápidamente. Un modelo que usa solo proteína total no puede explicar ese cambio sin introducir un estado adicional o una función efectiva justificada [A01], capítulo 6.

En una cascada, un estado activo regula la tasa de modificación de la etapa siguiente. Las curvas y escalas se componen y pueden producir sensibilidad elevada sin que cada unión elemental sea cooperativa. Huang y Ferrell estudiaron este principio en una cascada MAPK mediante modelado y mediciones. El ejemplo docente del capítulo examina las ecuaciones sin atribuirles sus parámetros experimentales [A12] [A01], §6.2.

## Desarrollo guiado: construir una red de modificación sin perder enzimas

Un sustrato X puede estar sin modificar, con una modificación o con dos: X₀, X₁ y X₂. E añade modificaciones y F las retira. En un mecanismo distributivo, la enzima debe liberar el sustrato después de cada paso; por eso X₁ vuelve a competir por enzima libre. «Distributivo» describe esa secuencia de encuentros, no una distribución de probabilidad. Define cuatro complejos: C₀=E:X₀, C₁=E:X₁, D₁=F:X₁ y D₂=F:X₂. Los dos puntos indican unión dentro del complejo. [A01] [A16]

Cada unión tiene tres pasos de tasa: asociación k_on·enzima libre·sustrato libre, disociación k_off·complejo y catálisis k_cat·complejo. Para el primer complejo, C₀′=k_on,0 E X₀−(k_off,0+k_cat,0)C₀. En X₀′ aparecen la asociación con signo negativo, la disociación positiva y la catálisis de D₁ positiva, porque esa reacción devuelve sustrato sin modificar. La catálisis de C₀ produce X₁ y E libre, no devuelve X₀. Escribir antes la tabla de reacciones evita confundir esos destinos. [A01] [A16]

### Contar unidades de sustrato y unidades de enzima

El total de E es E+C₀+C₁; el de F, F+D₁+D₂. El total de sustrato es X₀+X₁+X₂+C₀+C₁+D₁+D₂. Cada complejo cuenta una unidad de sustrato y una de su enzima. No sumes ambos totales de enzima al total de sustrato como si fueran tres reservas de la misma sustancia. La matriz estequiométrica permite verificar que la derivada de cada total es cero. [A01] [A16]

Si observas «X₂ total», decide si incluye D₂, que contiene sustrato doblemente modificado unido a fosfatasa. Un anticuerpo o un reportero pueden responder de forma distinta a especies libres y complejadas. El programa puede predecir ambas, pero el ajuste debe usar la combinación que corresponde al ensayo. Esta elección puede cambiar la pendiente aparente de una curva de respuesta. [A01] [A09]

### De dónde sale la ultrasensibilidad de saturación

En un ciclo de una modificación, aproxima las dos tasas como v₁=V₁(1−q)/(K₁+1−q) y v₂=V₂q/(K₂+q), donde q es la fracción modificada y los K están normalizados por el total de sustrato. En equilibrio v₁=v₂. Si K₁ y K₂ son pequeños, ambas enzimas están cerca de saturación en gran parte del intervalo y una pequeña diferencia entre capacidades puede desplazar mucho q. «Ultrasensibilidad» significa una respuesta de salida más pronunciada que la referencia no cooperativa pertinente; no demuestra bistabilidad. La bistabilidad requiere múltiples equilibrios y un análisis de su estabilidad. [A13] [A16]

La práctica de nueve especies conserva explícitamente enzimas y sustrato. Al comparar con una aproximación reducida, usa los mismos totales y define qué complejos se han eliminado. Una conservación numérica muy precisa comprueba contabilidad, pero no demuestra que las constantes describan una enzima real. [A01] [A16]

## Un ciclo de modificación y su conservación

Sea X una proteína inactiva y X* activa, con total Xₜ=X+X*. Una enzima activadora convierte X en X* y otra revierte el proceso. En una aproximación Michaelis–Menten, x'=V₁(Xₜ−x)/(K₁+Xₜ−x)−V₂x/(K₂+x), con x=[X*]. La conservación reduce el modelo a una variable y obliga a mantener 0≤x≤Xₜ [A01], §§3.1 y 6.2; [A13].

Si K₁ y K₂ son pequeños frente a sus sustratos disponibles en una zona interior, ambas tasas se aproximan a capacidades casi constantes. Una pequeña diferencia entre ellas puede desplazar la fracción activa desde cerca de un extremo al otro. Esa es la base de la ultrasensibilidad de orden cero. Cerca de los extremos, no puedes mantener simultáneamente la aproximación de saturación de ambas enzimas [A13] [A01], §6.2.1.

Una respuesta muy pronunciada no demuestra bistabilidad. El ciclo de una sola variable con las tasas anteriores tiene producción decreciente y pérdida creciente, por lo que la derivada neta es negativa en el interior y existe un único equilibrio bajo tasas positivas. Puede ser ultrasensible y monoestable al mismo tiempo [A01], §§4.2 y 6.2.

## Calcular la pendiente del ciclo

Define F(x,V₁)=V₁(Xₜ−x)/(K₁+Xₜ−x)−V₂x/(K₂+x). En equilibrio F=0. La sensibilidad dx*/dV₁=−F_V₁/F_x aumenta cuando |F_x| se hace pequeño, siempre que el numerador no disminuya al mismo tiempo. En saturación, ambas tasas tienen poca dependencia con x y la relajación puede hacerse lenta. La pendiente estacionaria y la velocidad temporal se conectan a través de la misma derivada [A01], §§4.2, 4.5 y 6.2.

Para Xₜ=1, K₁=K₂=0,01 y V₁=V₂=1 en unidades compatibles, x*=0,5 por simetría. F_x=−2·0,01/(0,51²)≈−0,07689 y F_V₁=0,5/0,51≈0,98039. La sensibilidad es aproximadamente 12,75 unidades de fracción por unidad de V₁. Es un cálculo original que muestra una transición pronunciada sin varios equilibrios [A01] [A13].

## Cascadas: componer ganancias

Si una primera etapa alcanza x*=h₁(u) y una segunda y*=h₂(x*), la pendiente total es h₂'(x*)h₁'(u). En sensibilidades logarítmicas positivas, las elasticidades se multiplican. La composición puede aumentar o reducir sensibilidad según el punto de operación. Una cascada de funciones hiperbólicas no se vuelve automáticamente arbitrariamente abrupta en todos sus niveles [A01], §6.2.2; [A12].

En dinámica, cada etapa añade su propio balance y tiempo de respuesta. La salida estacionaria puede parecer digital mientras una entrada corta no atraviesa toda la cascada. Saturación de enzimas y secuestro entre niveles pueden acoplarlas hacia atrás, de modo que la salida de una etapa cambia al conectarla con la siguiente [A01], capítulos 3 y 6; [I07].

## Modificación multisito y enzimas compartidas

Una proteína con estados X₀,X₁,X₂ puede sufrir dos modificaciones secuenciales. Si una enzima debe liberar el sustrato entre pasos, el mecanismo es distributivo; si permanece unida y completa varios pasos, es procesivo. Esas definiciones cambian especies, reacciones y posibilidad de competencia entre estados. Markevich y colaboradores estudiaron bistabilidad en modificación multisito bajo mecanismos determinados [A16].

Para un mecanismo distributivo abstracto, enumera cuatro conversiones con enzimas: E+X₀⇌C₁→E+X₁; E+X₁⇌C₂→E+X₂; F+X₂⇌D₂→F+X₁; F+X₁⇌D₁→F+X₀. Cada flecha reversible representa dos reacciones y cada paso catalítico otra, para un total de doce procesos. Las tasas de masa de acción se escriben antes de cualquier reducción [A01], capítulos 2, 3 y 6; [A16].

Los totales son Eₜ=E+C₁+C₂, Fₜ=F+D₁+D₂ y Xₜ=X₀+X₁+X₂+C₁+C₂+D₁+D₂. Conservas nueve especies y tres restricciones independientes. Si sustituyes enzima libre por enzima total en todas las tasas sin tener en cuenta complejos, eliminas precisamente parte de la competencia que puede producir no linealidad [A01], §§3.1 y 5.4; [A16].

No toda fosforilación doble es biestable. La propiedad depende de estructura, conservaciones y parámetros. Para investigarla, calcula varias soluciones estacionarias en la clase de totales fijada, verifica dominios y estabilidad y compara trayectorias desde distintas condiciones iniciales. Un único ajuste de una curva sigmoide no demuestra dos atractores [A16] [A01], §4.4.

## Secuestro estequiométrico como umbral

Si un activador A se une con fuerza a un inhibidor I en un complejo inactivo, el A libre puede permanecer bajo mientras el inhibidor no esté saturado. Cuando el total de activador excede la capacidad de unión, aumenta la fracción libre. La unión y las conservaciones generan un umbral sin exigir una unión cooperativa de orden elevado [A01], §§3.3 y 6.2.

Para un equilibrio A+I⇌C, Aₜ=a+c, Iₜ=i+c y Kd=ai/c. Resuelve la ecuación cuadrática del complejo usando la raíz físicamente admisible. La aproximación a≈max(Aₜ−Iₜ,0) corresponde al límite de unión muy fuerte, pero no reemplaza la curva continua para Kd finita. La zona cerca del umbral es precisamente donde una aproximación por partes necesita comprobarse [A01], capítulos 2 y 3.

## Redes excitable y oscilatoria no son sinónimos

Una red activadora con recuperación lenta puede responder a un estímulo con una excursión grande y después regresar a un único equilibrio estable. Ese comportamiento excitable se distingue de un oscilador que recorre ciclos sin estímulos sucesivos. Los modelos de señalización y excitabilidad de Ingalls permiten comparar esos mecanismos con circuitos reguladores [A01], §§6.5 y 8.2.

Antes de etiquetar un pulso como oscilación, retira el estímulo y observa el destino. Examina si el sistema tiene un único equilibrio, un umbral de excitación y un tiempo de recuperación. En un modelo con ruido, eventos excitables espontáneos pueden producir intervalos irregulares sin un ciclo determinista atractivo [A01], capítulos 4, 6 y 8.

## Ejercicio resuelto: conservación antes que ajuste

Supón que el código de modificación doble inicia Eₜ=2, Fₜ=1 y Xₜ=10 en unidades de cantidad. Cada evaluación debe conservar los tres totales mientras las reacciones definidas no tengan fuentes ni sumideros. Si E+C₁+C₂ cae de 2 a 1,8, revisar tasas no es el primer paso: busca un signo o coeficiente que no devuelve enzima tras catálisis [A01], §§2.1 y 5.4.

La práctica construye N y v, comprueba conservaciones simbólicas por producto de vectores y verifica que las trayectorias mantengan los totales dentro de tolerancia. Esa prueba se realiza antes de estudiar respuestas ultrasensibles. Una no linealidad visible producida por un error de balance no es un fenómeno del circuito [A01] [A16].
