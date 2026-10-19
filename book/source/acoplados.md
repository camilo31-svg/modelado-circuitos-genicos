# Circuitos complejos: osciladores acoplados, sincronización y módulos compartidos

- Derivar las ecuaciones y justificar los supuestos del modelo presentado.
- Reproducir los cálculos y comprobar sus límites con un ejemplo resuelto.
- Relacionar las predicciones con observaciones y fuentes académicas.

## Usar osciladores como módulos exige comprobar su interacción

Al combinar dos osciladores, la red completa puede sincronizarse, mostrar modulación, perder la oscilación o producir dinámica más compleja. La independencia no se deduce de dibujar dos lazos separados: pueden compartir recursos o reguladores. Ingalls trata sincronización entre células; un estudio teórico reciente examina acoplamiento intracelular entre circuitos oscilatorios [A01], §7.4.3; [A06].

El artículo de Holló y colaboradores distingue regímenes de acoplamiento y predice, mediante modelos, distintos comportamientos dinámicos. Es una investigación computacional con implicaciones para trabajo experimental futuro; no debe citarse como demostración de que todos esos regímenes ya se hayan construido y observado en plantas. Su fecha en línea de 2025 y volumen editorial de 2026 se conservan en la nota bibliográfica [A06].

## Desarrollo guiado: convertir dos osciladores en una ecuación de diferencia de fase

La fase θ indica la posición a lo largo de un ciclo; aumenta 2π radianes por vuelta. No es una concentración ni una amplitud. Un oscilador de período T tiene frecuencia angular ω=2π/T. Si T está en horas, ω está en radianes por hora. La reducción de fase supone que la trayectoria permanece cerca de un ciclo estable y que las perturbaciones de amplitud se relajan suficientemente rápido. [A01] [A05]

Para dos osciladores con acoplamiento simétrico senoidal, escribe θ₁′=ω₁+K sin(θ₂−θ₁) y θ₂′=ω₂+K sin(θ₁−θ₂). K mide intensidad de acoplamiento en inversa de tiempo, con radianes tratados como adimensionales. Define φ=θ₁−θ₂ y Δω=ω₁−ω₂. Restar las ecuaciones y usar sin(−φ)=−sinφ produce φ′=Δω−2K sinφ. El factor dos aparece porque ambos osciladores responden; no se añade por convenio. [A01]

### Bloqueo no significa fases idénticas

Una diferencia de fase constante requiere sinφ*=Δω/(2K). Si |Δω|>2K no existe solución fija: la diferencia deriva. Si |Δω|<2K aparecen dos soluciones por período de fase. La derivada del campo es −2K cosφ. La solución con cosφ*>0 es estable para K>0; la otra es inestable. Bloqueo significa igual frecuencia media y una diferencia de fase constante, que puede ser distinta de cero. [A01]

Para períodos de 24 y 26 h, Δω=2π(1/24−1/26)≈0,0201 rad/h. El umbral de este modelo es K≈0,0101 h⁻¹. Con K=0,015 h⁻¹, sinφ*≈0,671 y la rama estable tiene φ*≈0,736 rad. El cálculo explica el desfase de la figura y también sus límites: son valores de un modelo de fase docente, no estimaciones de una molécula comunicante de un artículo. [A01] [A05]

### Volver a moléculas cuando la amplitud importa

Dos anillos de tres proteínas necesitan seis balances si mantienes esos estados. Un enlace cruzado represor puede modificar la producción de X₁ mediante un denominador 1+X₃ⁿ+κY₁ⁿ. κ pesa el enlace adicional y debe definirse con las escalas elegidas. Esa suma representa una ley reguladora propuesta; otra arquitectura de unión podría dar un producto u otra función. No se obtiene la función molecular a partir de la palabra «acoplamiento». [A01] [A06]

Para decidir si el movimiento es periódico, observa todas las componentes. Una proyección X₁ frente a Y₁ puede parecer un lazo mientras las otras especies siguen cambiando de una vuelta a otra. La sincronía de dos señales tampoco demuestra identidad de sus estados internos. Por eso la práctica compara trazas temporales, proyección y mapa de las seis especies, y pide repetir la ventana tras el transitorio. [A01] [A06]

## Reducir a fase: qué se conserva y qué se pierde

Si cada oscilador posee un ciclo atractivo y el acoplamiento es débil respecto a la relajación de amplitud, puedes aproximar su estado por una fase φᵢ. La velocidad de fase libre es ωᵢ y la interacción añade una función periódica. La aproximación elimina los cambios de amplitud y necesita cuidado cerca de una bifurcación, durante perturbaciones fuertes o cuando el ciclo se deforma mucho [A01], §§6.5 y 7.4; [A02].

Un modelo docente de dos fases con acoplamiento sinusoidal simétrico es φ₁'=ω₁+Ksin(φ₂−φ₁), φ₂'=ω₂+Ksin(φ₁−φ₂). Define ψ=φ₂−φ₁ y Δω=ω₂−ω₁. Al restar obtienes una sola ecuación que explica el bloqueo de fase [A01], §7.4.3.

$$
\frac{d\psi}{dt}=\Delta\omega-2K\sin\psi.
$$

Existe un equilibrio de fase si |Δω|≤2|K|. Para K>0, la rama con cosψ*>0 es estable porque la derivada es −2Kcosψ*. Si |Δω|>2K, ninguna fase relativa constante satisface la ecuación y aparece deriva. La condición vale para este modelo de fase; no constituye una fórmula general para cualquier acoplamiento molecular [A01] [A02].

## Un ejemplo de sincronización calculado

Dos módulos tienen períodos libres T₁=24 h y T₂=26 h. Sus frecuencias angulares son 2π/24 y 2π/26, con |Δω|≈0,02014 h⁻¹. Si K=0,015 h⁻¹, 2K=0,03 h⁻¹ y puede haber bloqueo. La fase estable cumple sinψ*=Δω/(2K), con magnitud aproximada de 0,736 rad. El oscilador más lento necesita un desfase para recibir el empuje que compensa la diferencia [A01].

Si K baja a 0,005 h⁻¹, el máximo ajuste 2K=0,01 h⁻¹ no basta y el modelo predice deriva de fase. Para una pareja simétrica bloqueada, la frecuencia común es (ω₁+ω₂)/2, porque al sumar las ecuaciones los términos de interacción se cancelan. Esa media deja de ser la fórmula general si el acoplamiento es asimétrico [A01], §7.4.3.

## De fases a seis proteínas

Para estudiar amplitud y cambios de forma, conserva estados moleculares. Dos anillos reducidos necesitan al menos seis proteínas. Una construcción docente puede acoplar una proteína de cada anillo añadiendo represión cruzada en su función de producción. Si se multiplican factores represores, se está asumiendo una forma específica de integración; si comparten promotor con exclusión, la expresión debe derivarse de estados distintos [A01], §§7.1 y 7.5.

Un ejemplo abstracto es x₁'=a/[1+x₃ⁿ+κy₁ⁿ]−x₁, x₂'=a/(1+x₁ⁿ)−x₂, x₃'=a/(1+x₂ⁿ)−x₃, y un segundo conjunto análogo. El denominador aditivo representa pesos competitivos de represión en esta simplificación. Otro mecanismo daría otro denominador. κ controla un acoplamiento en el modelo y no se identifica automáticamente con la concentración de una sustancia [A01] [R19].

Cuando aumenta κ, no supongas que la diferencia de fase simplemente disminuye. El equilibrio y los ciclos pueden cambiar de estabilidad, las amplitudes pueden variar y pueden aparecer estados que la reducción de fase no contiene. Clasifica el régimen usando trayectorias largas, equilibrios, autovalores y análisis de ciclos, con comprobaciones numéricas [A01], capítulos 4 y 7; [A06].

## Acoplamiento entre células y observación colectiva

Danino y colaboradores estudiaron un circuito con comunicación que sincroniza oscilaciones entre células. El caso muestra que el medio y la geometría pueden formar parte de la dinámica colectiva. En una abstracción compartimental, cada célula posee estados internos y una señal extracelular recibe aportes, se intercambia y se retira [A05] [A01], §7.4.

Para una señal s del medio, una ecuación docente es s'=q·(1/N)Σᵢh(xᵢ)−δₛs, mientras cada célula recibe s en su producción. La normalización por N cambia el significado de q: con volumen del medio fijo y más células, la producción total podría aumentar en lugar de permanecer constante. El modelo debe declarar densidad, volumen y normalización antes de interpretar un cambio de tamaño de población [A01], §§3.4 y 7.4.

## Medir sincronía sin confundirla con señal grande

Para fases φᵢ, define R·eⁱΨ=(1/N)Σᵢeⁱφᵢ. R está entre cero y uno: cerca de uno indica fases concentradas; cerca de cero puede indicar dispersión o grupos equilibrados en fases opuestas. Un R bajo no significa necesariamente que cada célula haya dejado de oscilar. Este orden de fase es una medida docente de coordinación, no de amplitud molecular [A01], §7.4.3; [A06].

Si dos subpoblaciones oscilan exactamente en oposición y tienen igual tamaño y amplitud, su promedio puede ser constante aunque todas las células oscilen. Un registro de célula individual y una distribución de fases distinguen esa desincronización de una pérdida de ciclos. También debes comprobar si el procesamiento de imagen introduce un desplazamiento temporal diferente entre señales [A01], §§7.3 y 7.4; [I04].

## Complejidad, caos y qué evidencia haría falta

Una trayectoria irregular de seis o más variables no prueba caos. Puede reflejar un transitorio largo, ruido, entrada irregular o error de integración. En un modelo determinista, una afirmación de caos exige análisis adecuados, por ejemplo sensibilidad exponencial de trayectorias cercanas dentro de un atractor y estimaciones convergentes de exponentes de Lyapunov, junto con descarte de artefactos numéricos [A02] [A06].

La práctica del atlas se centra en bloqueo y deriva de fase, que permiten un control analítico claro. Los fenómenos de mayor complejidad se presentan como rutas de investigación con sus fuentes, sin fabricar una simulación irregular y etiquetarla como caos. Esa distinción ayuda a ampliar el repertorio sin rebajar el criterio de evidencia [A01] [A06].

## Ejercicio resuelto: una salida lenta a partir de dos entradas rápidas

Para cos(ω₁t)+cos(ω₂t), la identidad trigonométrica produce 2cos[(ω₁−ω₂)t/2]cos[(ω₁+ω₂)t/2]. La envolvente varía lentamente cuando las frecuencias son próximas. Ese batido matemático no requiere acoplamiento entre los generadores: puede aparecer solo al combinar sus salidas. Un circuito que integra dos osciladores puede por ello producir una escala lenta aunque cada uno conserve su frecuencia [A06] [A01], §6.6.

Con períodos de 10 y 11 h, la diferencia de frecuencias en ciclos por hora es 1/10−1/11=1/110. La escala del batido es 110 h. Si interpretaras únicamente esa salida como el período de cada módulo, atribuirías una lentitud que ninguno posee por separado. Analiza siempre los estados internos y la regla de integración de salida [A01] [A06].
