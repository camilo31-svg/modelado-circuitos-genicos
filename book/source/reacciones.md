# De las reacciones a las EDO: estequiometría, conservación y escalas

- Derivar las ecuaciones y justificar los supuestos del modelo presentado.
- Reproducir los cálculos y comprobar sus límites con un ejemplo resuelto.
- Relacionar las predicciones con observaciones y fuentes académicas.

## Una reacción es una instrucción de contabilidad

Un diagrama molecular se convierte en un modelo cuando especificas qué especies cambian, cuánto cambia cada una y a qué velocidad ocurre cada proceso. La flecha A → B retira una unidad de A y añade una de B por evento. La reacción A + B → C retira una de cada reactivo y añade una de C. La relación estequiométrica describe esos cambios; la ley cinética establece cuántos eventos ocurren por unidad de tiempo. Mezclar ambas funciones lleva a confundir una cantidad conservada con una velocidad de reacción [A01], capítulo 2.

Para A ⇌ B, escribe dos procesos con tasas v₁ = k₁a y v₂ = k₂b. Las dos tasas son no negativas; la diferencia entre ellas puede tener cualquier signo. El balance sale de sumar contribuciones, no de poner signos negativos dentro de las constantes cinéticas [A01], §2.1.

$$
\frac{da}{dt}=-k_1a+k_2b,\qquad
\frac{db}{dt}=k_1a-k_2b.
$$

Suma las ecuaciones: d(a+b)/dt = 0. Por tanto, a+b = T, con T fijado por las condiciones iniciales. No has supuesto equilibrio; la conservación vale durante toda la trayectoria. Sustituir b = T−a reduce el sistema a a' = k₂T − (k₁+k₂)a. La solución del capítulo anterior vuelve a servir, con tasa efectiva k₁+k₂ y equilibrio a* = k₂T/(k₁+k₂) [A01], §§2.1 y 2.2.

## Escribir N·v sin que la matriz se convierta en una caja negra

Ordena las especies como (A,B,C) y los procesos como (A→B, B→A, A+B→C). Cada columna de N registra un proceso; cada fila registra una especie. El siguiente bloque es una tabla de enteros de cambio, no una tabla de constantes cinéticas [A01], §§2.1 y 5.4:

```text
             v1    v2    v3
A            -1    +1    -1
B            +1    -1    -1
C             0     0    +1
```

Multiplicar N por v significa, fila a fila, combinar las tasas de todos los procesos que afectan a esa especie. Si v₃ = k₃ab, el resultado contiene a' = −v₁+v₂−v₃, b' = v₁−v₂−v₃ y c' = v₃. La escritura compacta no añade una aproximación; organiza el mismo balance y facilita comprobar que diagrama, ecuaciones y código coinciden [A01].

$$
\frac{d\mathbf{x}}{dt}=N\mathbf{v}(\mathbf{x};\theta).
$$

En Python, N puede ser un array de forma (especies, reacciones) y v un vector de longitud reacciones. `N @ v` devuelve una derivada por especie. Si intercambias el orden de dos especies en el código y no en N, el producto seguirá siendo una operación válida y producirá un modelo equivocado. Mantener nombres y órdenes explícitos evita un error que el lenguaje no puede detectar por sí solo [R03] [A01].

## Masa de acción: qué significa el producto de concentraciones

Para una reacción elemental A+B→C en un volumen bien mezclado, la ley determinista de masa de acción toma v = kab. Multiplicar por a y b expresa que el número de encuentros posibles depende de ambos reactivos. Si se agota cualquiera, la reacción se detiene. El término elemental es una hipótesis sobre un proceso concreto; una reacción global que resume varios pasos no tiene por qué obedecer la misma ley [A01], §§2.1 y 3.1.

Si a y b se expresan en nM y v en nM/h, k debe tener unidades nM⁻¹h⁻¹. Para A→B, k tiene unidades h⁻¹. La dimensión de una constante cambia con el orden de la reacción y con la unidad de concentración elegida. Un número copiado de una tabla sin unidad o sin definición de la tasa no es un parámetro utilizable [A01], capítulos 2 y 3.

En 2A→C, la reacción consume dos unidades de A. Si defines v = ka² como tasa de avance, a' = −2ka² y c' = ka². Algunas convenciones absorben factores combinatorios en k; otras no. La ecuación escrita y la definición de la constante deben acompañar al número. En el modelo estocástico discreto aparecerá además el número de pares distintos, que no coincide exactamente con n² para pocos reactivos [A01], §§2.1 y 7.6; [I02].

No conviertas automáticamente una flecha de activación X→producción de Y en X→Y. El regulador X puede facilitar la producción y conservarse. Una representación elemental idealizada es X→X+Y, con tasa proporcional a X. El coeficiente neto de X es cero y el de Y es +1. La misma distinción explica por qué el ARN no se consume simplemente por ser traducido [A01], §7.1.

## Redes abiertas: entrar y salir de la frontera elegida

En un sistema abierto pueden entrar materia y energía desde estados que no has incluido. El símbolo ∅→X con tasa α representa una fuente externa efectiva; X→∅ con tasa δx representa una salida del conjunto de especies observado. ∅ no es una molécula y no afirma que aparezca o desaparezca materia del universo. Expresa la frontera del modelo [A01], §2.1.1.

Un reservorio mantenido a concentración fija puede generar una tasa pseudo-primer orden. Si A+B→C tiene v = kab y b ≈ b₀ durante el experimento, puedes definir k̂ = kb₀ y escribir v ≈ k̂a. Esta simplificación requiere que el consumo de B no altere apreciablemente b₀, o que un mecanismo externo lo reponga. Si B empieza a agotarse, k̂ deja de representar una constante [A01], §§2.1 y 2.2.

Al comparar dos modelos, pregunta dónde está la frontera. Un modelo puede tratar el ribosoma como reservorio fijo y otro como recurso explícito. No hay contradicción lógica entre ambos: responden a preguntas y regímenes distintos. La contradicción aparece si usas el primero para predecir competencia fuerte sin verificar su supuesto de recurso disponible aproximadamente constante [A01], capítulos 2 y 7; [I08].

## Buscar conservaciones de forma sistemática

Un vector fila ℓ identifica una combinación conservada cuando ℓᵀN = 0. Entonces d(ℓᵀx)/dt = ℓᵀNv = 0 para cualquier ley de tasas que conserve esa estequiometría. Buscar esos vectores equivale a buscar el núcleo izquierdo de N. No necesitas dominar toda el álgebra lineal para interpretar el resultado: cada coeficiente indica cuántas unidades del componente conservado contiene una especie [A01], §5.4.

En E+S⇌C→E+P, una unidad de enzima se encuentra libre como E o unida como C. Por eso E+C = Eₜ. Si el sistema está cerrado respecto al sustrato y cada producto contiene una unidad derivada de él, S+C+P = Sₜ. Observa que E+C+S+P no es una conservación útil de la misma clase: cuenta objetos de tipos distintos con pesos que no reflejan los grupos químicos conservados [A01], §§3.1 y 5.4.

La conservación puede introducir un autovalor cero en el sistema completo. Ese cero a veces expresa que elegiste una descripción con familias de estados correspondientes a distintos totales. Para estudiar estabilidad dentro del experimento, elimina una variable mediante la conservación o restringe el análisis a la clase con los totales iniciales fijados. No interpretes automáticamente ese cero como evidencia de una bifurcación biológica [A01], §§4.2 y 5.4.

## Cantidad y concentración cuando cambia el volumen

Escribir balances en cantidades permite separar reacción y crecimiento. Si n es cantidad, V volumen y x = n/V, la regla del cociente da un término de dilución que se añade al balance de concentración. Es una derivación propia del cambio de variable usado en modelos compartimentales [A01], §3.4.

$$
\frac{dx}{dt}=\frac{1}{V}\frac{dn}{dt}-\frac{1}{V}\frac{dV}{dt}x.
$$

Define μ = V'/V. Aunque n permanezca constante, x disminuye si V aumenta. Degradación y dilución pueden aparecer juntas como −(δ+μ)x, pero representan procesos diferentes. En una célula que se divide, el reparto de cantidades añade un evento; una aproximación continua de dilución no describe cada salto de división. El nivel de resolución debe coincidir con la pregunta y los datos [A01], §§3.4 y 7.1.

En un tejido con dos volúmenes desiguales, un flujo J de cantidad por tiempo resta J/V₁ de la concentración de la célula 1 y suma J/V₂ a la de la célula 2. Usar el mismo término de concentración en ambos balances conserva la suma de concentraciones, pero no necesariamente la cantidad total. La comprobación correcta multiplica cada concentración por su volumen [A01], §3.4.

## Adimensionalizar para ver los grupos que importan

La adimensionalización se introduce aquí como herramienta de análisis de EDO, sin regresar a un curso previo de aritmética. En x' = α−δx, elige la escala de abundancia X = α/δ y la de tiempo T = 1/δ. Define z = x/X y τ = t/T. Sustituye x = Xz y dx/dt = (X/T)dz/dτ; después divide por X/T. Se obtiene una ecuación sin parámetros explícitos [A01], apéndice B y capítulo 4.

$$
\frac{dz}{d\tau}=1-z.
$$

Esto demuestra que todos los modelos de esta forma, con tasas positivas y la misma condición inicial normalizada, comparten una curva adimensional. No demuestra que dos células usen el mismo mecanismo molecular. Al comparar modelos con dos especies aparecen cocientes de escalas que ya no se eliminan: por ejemplo, δₘ/δₚ informa de la relación entre tiempos de recambio de ARN y proteína [A01], §§2.2 y 7.1.

Para una autorrepresión x' = α/[1+(x/K)ⁿ]−δx, elige z = x/K y τ = δt. Queda dz/dτ = β/(1+zⁿ)−z, con β = α/(δK). Cambiar simultáneamente α, δ y K manteniendo β conserva la dinámica normalizada, aunque cambia la escala física. Esta observación anticipa problemas de identificabilidad cuando solo se observan datos normalizados [A01], §§4.4, 4.6 y 7.3.

## Separar escalas sin confundir equilibrio rápido y estado cuasiestacionario

Considera εz' = g(x,z) y x' = f(x,z), con ε pequeño tras adimensionalizar. La variable z puede relajarse rápidamente hacia una relación g(x,z) = 0 mientras x cambia poco. El sistema reducido sustituye z por la solución z = h(x). La idea requiere una rama rápida atractiva, una separación de tiempos suficiente y evitar zonas donde la relajación rápida deje de ser rápida [A01], §2.2.

El equilibrio rápido aproxima el balance entre procesos reversibles rápidos. El estado cuasiestacionario aproxima que un intermediario cambia poco porque entradas y salidas casi se compensan, aunque haya flujo neto hacia producto. En E+S⇌C→E+P, ignorar el paso catalítico en el equilibrio de unión da una constante de disociación; conservarlo al imponer C'≈0 da Kₘ=(k₋₁+kcat)/k₁. Las dos aproximaciones solo coinciden bajo condiciones adicionales [A01], §§2.2 y 3.1; [D08].

Un valor pequeño de ε no autoriza usar el modelo reducido desde cualquier condición inicial. Puede existir una capa inicial rápida en la que el intermediario se reajusta. Tampoco autoriza ignorar errores cerca de bifurcaciones o durante entradas muy rápidas. Comparar la solución completa y la reducida en la variable observable es una comprobación más informativa que mirar solo la magnitud de una constante [A01], §2.2.

## Ejercicio resuelto: unión y conservación

Para A+B⇌C, supón Aₜ = a+c = 10 nM, Bₜ = b+c = 8 nM y Kd = k₋/k₊ = 2 nM. En equilibrio, k₊ab = k₋c. Sustituye a = 10−c y b = 8−c: (10−c)(8−c) = 2c. El ejercicio usa números originales para aplicar el modelo de unión de Ingalls [A01], capítulos 2 y 3.

$$
c^2-20c+80=0.
$$

Las raíces son 10±√20, aproximadamente 5,53 y 14,47 nM. La segunda viola c≤min(Aₜ,Bₜ)=8 y se descarta. La primera da a≈4,47 nM y b≈2,47 nM; su producto dividido por c es aproximadamente 2 nM. Encontrar dos raíces algebraicas no implica dos equilibrios biológicamente accesibles. Primero se aplica el dominio y después se analiza la dinámica [A01].

El balance completo del complejo es c' = k₊(Aₜ−c)(Bₜ−c)−k₋c. Su derivada respecto a c es −k₊(Aₜ+Bₜ−2c)−k₋, negativa en el intervalo válido. El equilibrio físico es localmente estable y el campo apunta hacia el intervalo en ambos extremos. Has comprobado conservación, dominio, unicidad dentro del intervalo y estabilidad sin integrar ninguna trayectoria [A01], capítulos 2 y 4.
