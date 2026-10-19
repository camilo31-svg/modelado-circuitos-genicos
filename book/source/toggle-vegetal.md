# Un interruptor genético en plantas: lectura matemática de un caso de 2025

- Derivar las ecuaciones y justificar los supuestos del modelo presentado.
- Reproducir los cálculos y comprobar sus límites con un ejemplo resuelto.
- Relacionar las predicciones con observaciones y fuentes académicas.

## Qué aporta el caso de 2025

Kassaw y colaboradores estudiaron un interruptor genético vegetal utilizando funciones de transferencia cuantitativamente caracterizadas y modelos para guiar la composición del circuito. El resumen informa funcionamiento conforme a las predicciones en plantas estables, incluidas etapas de diferenciación de tejidos y órganos. El valor del caso para este curso es conectar caracterización de componentes, análisis matemático y prueba de un dispositivo completo [A11].

La fuente consultada para ese resultado es el resumen primario y la información editorial del artículo. No se afirma aquí haber reproducido sus parámetros ni su conjunto de datos. El desarrollo siguiente es un ejercicio de lectura matemática de un interruptor vegetal con ecuaciones explícitas y supuestos propios, que permite formular preguntas pertinentes al estudiar el artículo completo [A11] [A01], §7.2.3.

## Desarrollo guiado: utilizar un caso vegetal sin cambiar el significado de las ecuaciones

Para cualquier interruptor de represión cruzada, define primero qué produce cada unidad reguladora y qué especie actúa sobre la otra. Un modelo dimensional mínimo es x′=b_x+V_x/[1+(y/K_y)ⁿ]−δ_xx y y′=b_y+V_y/[1+(x/K_x)ᵐ]−δ_yy. x e y son concentraciones activas efectivas, no necesariamente fluorescencias. b representa fuga; V, incremento de producción; K, escala de regulación; δ, pérdida efectiva. Los parámetros necesitan unidades y una relación explícita con lo que se midió. [A01] [A11]

Para normalizar, define X=x/K_x, Y=y/K_y y τ=δ_xt. Entonces dX/dτ=(1/K_xδ_x)dx/dt. Sustituir el primer balance produce B_x+A_x/(1+Yⁿ)−X, con B_x=b_x/(K_xδ_x) y A_x=V_x/(K_xδ_x). Para Y, aparece ρ[B_y+A_y/(1+Xᵐ)−Y], con ρ=δ_y/δ_x y las amplitudes definidas respecto a δ_y. El cociente ρ se mantiene porque no has supuesto igual velocidad de pérdida. Cada coeficiente normalizado procede de agrupar cantidades dimensionales, no de borrar unidades al final. [A01]

### Interpretar una curva medida

Si una respuesta experimental relaciona señal de reportero con una entrada reguladora, debes comprobar si es una función de producción o una abundancia estacionaria. En el segundo caso ya contiene la pérdida del reportero. Introducirla como tasa y añadir otra pérdida sin convertir sus unidades duplica o mezcla procesos. Esta cautela se aplica por igual a transferencias obtenidas en bacterias, levaduras y plantas. [A01] [I04] [I06]

El caso vegetal de 2025 se utiliza para discutir qué evidencia respalda las funciones de transferencia y la memoria del circuito. Las ecuaciones reducidas de este desarrollo son docentes; no se atribuyen sus constantes al dispositivo publicado. Para reproducir cuantitativamente un resultado experimental harían falta los datos, su calibración, los parámetros, el código y las condiciones exactas de observación. [A11] [A01]

## Funciones de transferencia como módulos cuantitativos

Una curva Fₓ(y) describe cómo la actividad de un regulador Y afecta a la producción efectiva de X dentro de un contexto de caracterización. Para componer un interruptor, escribe x'=Fₓ(y)−δₓx e y'=Fᵧ(x)−δᵧy. Los equilibrios satisfacen x=Fₓ(y)/δₓ e y=Fᵧ(x)/δᵧ. La curva de producción y la nulclina de concentración coinciden solo si has incluido correctamente la pérdida y las unidades [A01], §§4.1 y 7.2.3.

Si las curvas originales están en unidades arbitrarias de reportero, una constante de conversión puede separar reportero y regulador activo. Dos módulos medidos con ganancias diferentes no se conectan simplemente identificando sus valores numéricos. La unidad de entrada del segundo debe corresponder a la salida biológica del primero [A01], §4.6; [I06].

## Una condición local para amplificación por doble represión

El Jacobiano del sistema de dos proteínas tiene diagonales −δₓ y −δᵧ y pendientes cruzadas Fₓ'(y*),Fᵧ'(x*), ambas negativas. Su determinante es δₓδᵧ−Fₓ'Fᵧ'. Si el producto de magnitudes de las pendientes supera δₓδᵧ, el equilibrio es una silla. Un estado intermedio inestable puede separar dos atractores si la estructura global contiene las ramas correspondientes [A01], §§4.2 y 7.2.3.

$$
\Delta=\delta_x\delta_y-F_x'(y^*)F_y'(x^*).
$$

Esta prueba utiliza pendientes locales en el punto de intersección, no solo el máximo cambio de la curva. Una regulación muy fuerte en otra región no garantiza que el equilibrio intermedio tenga ganancia suficiente. La posición de las curvas, fuga y degradación importan conjuntamente [A01], §§4.4 y 7.2.3.

## Normalizar sin borrar asimetrías

Define X=x/Kₓ, Y=y/Kᵧ y τ=δₓt. En una versión de Hill, X'=bₓ+aₓ/(1+Yⁿ)−X e Y'=ρ[bᵧ+aᵧ/(1+Xᵐ)−Y], donde ρ=δᵧ/δₓ si las amplitudes se definieron respecto a sus propias pérdidas. El cociente de tiempos permanece y afecta a trayectorias aunque no cambie la posición de nulclinas en esa parametrización [A01], §§2.2 y 7.2.3.

Si ρ≪1, Y cambia lentamente. Un pulso que modifica X puede terminar antes de que Y atraviese la región necesaria para conmutar. Un análisis exclusivamente estacionario identificaría coexistencia de estados, pero no el tiempo de entrada requerido para llegar de uno al otro. La conmutación es una pregunta de trayectoria y cuenca [A01], §§4.1, 4.4 y 7.2.3.

## Variación entre células y robustez del dispositivo

Asigna distribuciones de tasas o umbrales si hay evidencia de variación. El circuito puede ser biestable en la célula nominal y monoestable en otras. La fracción de células que conserva dos atractores depende de la distribución conjunta de parámetros, no de un rectángulo arbitrario con extremos independientes. Una evaluación de robustez debe declarar ese conjunto [A09] [I06] [A10].

En un tejido, las entradas, crecimiento y observación pueden variar espacialmente. Que un modelo explique una población inicial no significa que sus parámetros permanezcan constantes durante diferenciación. Para estudiar transferencia de contexto, permite dependencias justificadas y contrasta predicciones fuera del ajuste. Esa es una pregunta que el caso de 2025 pone en primer plano [A11] [P10].

## Un análisis de conmutación con observable separado

Conserva un reportero r'=kᵣx−δᵣr. Al terminar un pulso de entrada, x puede regresar a una cuenca baja mientras r sigue alto por su vida media. Clasificar memoria con r a un único tiempo puede sobreestimar conmutación. También puede ocurrir lo contrario si la lectura aún no ha madurado [A01], §§7.1 y 7.2; [I04].

Un ensayo de simulación informativo registra estado final de reguladores, trayectoria de reportero y destino tras retirar la entrada. Repite desde ambas cuencas y con distintas duraciones. El objetivo no es buscar un pulso que produzca un gráfico bonito, sino separar respuesta transitoria, cruce de separatriz y persistencia del atractor [A01], §7.2.3.

## Ejercicio resuelto: degradación cambia la condición local

Supón Fₓ'=-1,2 h⁻¹, Fᵧ'=-1,5 h⁻¹, δₓ=δᵧ=1 h⁻¹ en un equilibrio. El producto regulador es 1,8 h⁻² y Δ=−0,8 h⁻²: hay una silla. Si δᵧ aumenta a 2 h⁻¹ manteniendo hipotéticamente esas pendientes en el nuevo punto, Δ=0,2 h⁻² y la traza es −3 h⁻¹, compatible con estabilidad local [A01], §4.2.

La cláusula sobre las pendientes importa: al cambiar δᵧ también cambia en general la intersección y, por tanto, las pendientes evaluadas allí. La práctica debe resolver primero el nuevo equilibrio y después clasificarlo. Mantener un Jacobiano antiguo mientras se modifica un parámetro que desplaza el estado es una aproximación que puede dar una conclusión equivocada [A01], §§4.2 y 4.5.

## Cómo estudiar el artículo con este capítulo

Al leer el trabajo completo, identifica la definición de las funciones de transferencia, las variables medidas, las unidades, el contexto de caracterización, la regla de composición y las condiciones que se reservaron para prueba. Recalcula las nulclinas del modelo publicado antes de juzgar las trayectorias. Una ficha separa resultados consultados del artículo, cálculos propios y preguntas pendientes [A11] [A15].

Después pregunta qué cambio mínimo de estructura o contexto explicaría una desviación entre predicción y observación. Proponer una explicación no equivale a haberla identificado: contrasta modelos alternativos y datos que los distingan. Esta lectura utiliza matemáticas para evaluar evidencia y no para atribuir al artículo detalles que no se han verificado [A01], §§1.5 y 4.6; [I06].
