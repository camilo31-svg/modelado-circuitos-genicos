# Control integral biomolecular: adaptación robusta y sus límites

- Derivar las ecuaciones y justificar los supuestos del modelo presentado.
- Reproducir los cálculos y comprobar sus límites con un ejemplo resuelto.
- Relacionar las predicciones con observaciones y fuentes académicas.

## Qué se quiere mantener constante y frente a qué perturbación

Un control de expresión necesita una salida y, una referencia r, una perturbación d y una variable actuadora que pueda modificar la producción o pérdida. Define primero qué combinación se observa: proteína total, reportero maduro o una actividad. Un controlador que mantiene una señal instrumental no garantiza mantener otra variable que no está relacionada de forma estable con ella [A01], §§6.3 y 7.1; [I09].

Para una planta abstracta y'=ku−γy+d, aumentar la perturbación d cambia el equilibrio si u se mantiene fijo. Un controlador proporcional u=u₀+K(r−y) reduce esa sensibilidad, pero en general conserva error estacionario. El ajuste de un valor de producción no equivale a una estructura que detecta y corrige una perturbación [A01], §6.3; [A04].

## La identidad que explica el control integral

Introduce un estado z con z'=r−y y una actuación u=kᵢz. Si el sistema cerrado alcanza un equilibrio finito, necesariamente z'=0 y, por tanto, y*=r. La conclusión depende de alcanzar ese equilibrio; la identidad no demuestra estabilidad ni factibilidad de la actuación. Es un ejemplo de cómo separar una propiedad estacionaria de un problema dinámico [A04] [I09].

$$
z(t)=z(0)+\int_0^t[r-y(s)]\,ds.
$$

En una descripción química, una concentración no puede representar directamente un z que necesite valores positivos y negativos ilimitados. El motivo antitético utiliza dos especies no negativas cuya diferencia realiza la integración. Esa construcción conecta teoría de control y redes de reacciones [A04].

## El motivo antitético en balances explícitos

Una especie Z₁ se produce a tasa μ y otra Z₂ a tasa θy. Ambas se eliminan juntas por una interacción con tasa ηz₁z₂. Z₁ actúa sobre la producción de la salida. Un modelo determinista docente con salida de una etapa es el siguiente; no es una reproducción del modelo experimental de Aoki [A04] [I09].

$$
\frac{dz_1}{dt}=\mu-\eta z_1z_2,
\qquad
\frac{dz_2}{dt}=\theta y-\eta z_1z_2.
$$

$$
\frac{dy}{dt}=kz_1-\gamma y.
$$

Resta las ecuaciones de Z₁ y Z₂. El término de interacción desaparece porque consume las dos especies en la misma proporción. La diferencia z₁−z₂ integra μ−θy. En cualquier equilibrio finito del modelo ideal con parámetros positivos, y*=μ/θ. La invariancia se deriva del balance y no depende de conocer γ exactamente [A04].

$$
\frac{d(z_1-z_2)}{dt}=\mu-\theta y.
$$

Para μ=2 nM/h, θ=0,5 h⁻¹, k=1 h⁻¹, γ=1 h⁻¹ y η=1 nM⁻¹h⁻¹, el equilibrio docente es y*=4 nM, z₁*=4 nM y z₂*=0,5 nM. Si γ se duplica, la salida estacionaria ideal sigue en 4 nM, pero z₁* debe duplicarse y z₂* reducirse a la mitad. La compensación tiene un coste en abundancias internas [A04] [I09].

## La estabilidad no está incluida gratis

En el equilibrio define a=ηz₂* y b=ηz₁*. El polinomio característico del sistema de tres estados es λ³+(a+b+γ)λ²+γ(a+b)λ+bθk. Todos los coeficientes son positivos, pero eso no basta para un cúbico. El criterio de estabilidad exige además (a+b+γ)γ(a+b)>bθk. Es una derivación propia del Jacobiano del modelo anterior [A01], §4.2; [A04].

Un aumento de la actuación k puede mejorar la rapidez en parte del régimen y desestabilizar en otro. Si la actuación tiene etapas adicionales, saturación o retrasos, la condición cambia. No uses la identidad de integración como prueba de que cualquier conjunto de parámetros implementa adaptación estable [A04] [I09].

## Dilución: por qué la integración puede volverse imperfecta

Si Z₁ y Z₂ se diluyen con tasa δc, aparece −δcz₁ en la primera ecuación y −δcz₂ en la segunda. Al restar queda z'=μ−θy−δcz, donde z=z₁−z₂. El estado deja de acumular el error indefinidamente: se convierte en un integrador con fuga. En equilibrio, y*=μ/θ−(δc/θ)z*, que puede diferir de la referencia ideal [I09] [A04].

El artículo de Aoki y colaboradores estudió una implementación biomolecular y sus desviaciones respecto al motivo ideal. Para trasladar la idea a otro organismo, incluidos tejidos vegetales, deben examinarse dilución, recambio de las especies controladoras, saturación y mecanismo de medida. La ecuación ideal explica un principio; no constituye una validación automática de cualquier implementación [I09].

## Saturación y factibilidad

Si la producción actuada tiene máximo Vmax y la salida se pierde a tasa γy, mantener yref exige al menos que la producción disponible pueda compensar γyref y las perturbaciones relevantes. Una referencia que exceda la capacidad no puede alcanzarse simplemente aumentando ganancia. El integrador puede seguir acumulando error mientras la salida permanece saturada, fenómeno relacionado con windup en control [A04] [I09].

En el modelo de actuación kz₁/(K+z₁), el máximo es k. Una salida objetivo μ/θ con pérdida γ requiere γμ/θ<k para un equilibrio positivo finito de esa forma de actuación, en ausencia de otros términos. En la igualdad, el actuador necesitaría z₁ ilimitado para llegar al máximo exacto. Es una comprobación algebraica original que permite descartar objetivos inviables [A01] [I09].

## Diferencias entre la lectura determinista y la estocástica

En el modelo estocástico, la diferencia de cantidades conserva una identidad de expectativas porque los eventos antitéticos restan uno a ambas especies. Relacionar esa identidad con adaptación de la media estacionaria requiere condiciones de existencia de un régimen estacionario y momentos finitos. No se sigue que cada célula tenga exactamente el mismo valor en cada instante ni que disminuya automáticamente la variabilidad [A04].

El control de la media y el control del ruido pueden entrar en tensión. La dispersión depende de la red, el controlador y las tasas. Compara distribuciones y autocorrelaciones, además de trayectorias medias. Un gráfico de media que retorna a la referencia no muestra si aumentó la probabilidad de estados extremos [A04] [A07].

## Ejercicio resuelto: detectar una afirmación demasiado fuerte

Una simulación ideal conserva y*=μ/θ al variar γ y se presenta como prueba de adaptación perfecta en una planta. La conclusión válida es que el modelo ideal, dentro del régimen estable simulado, mantiene esa salida estacionaria. Para la conclusión vegetal faltan una correspondencia de estados y observables, tasas de dilución y pérdida, capacidad, parámetros informados por datos y validación de perturbaciones nuevas [A01] [I09] [P10].

En la práctica del atlas se compara el motivo ideal con un integrador con fuga y una actuación saturable. El objetivo es comprobar las identidades anteriores y mostrar cuándo dejan de cumplirse sus supuestos. No se incluyen secuencias ni procedimientos de construcción; el ejercicio trabaja exclusivamente con modelos abstractos y resultados numéricos [A04] [I09].
