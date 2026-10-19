"""Claves contextuales revisadas, no inferidas del nombre de una letra.

C = unidad de concentración elegida; T = unidad temporal elegida.
Los números de ecuación siguen el orden canónico de chapters.json.
"""
import re,hashlib,html,json,unicodedata

def E(symbol,meaning,units,role='magnitud'):
    return dict(symbol=symbol,meaning=meaning,units=units,role=role)

COMMON={
 'root':E('√','Raíz cuadrada principal; para reales requiere argumento no negativo. En autovalores puede extenderse a números complejos.','raíz de la unidad del argumento','operación'),
 'abs':E('|·|','Valor absoluto; para un complejo es su módulo. Mide tamaño y elimina el signo, sin cambiar la unidad.','misma unidad que su argumento','operación'),
 'imag':E('i','Unidad imaginaria: i²=−1. En G(iω) indica la evaluación de la respuesta en frecuencia, no un índice de dato.','1','constante matemática'),
 'atan':E('arctan','Inversa de la tangente en su rama principal; convierte una razón sin unidad en un ángulo.','rad','operación'),
 't':E('t','Tiempo transcurrido desde el origen elegido.','T','variable independiente'),
 'x':E('x, x(t)','Concentración de la especie que se sigue; x(t) es su valor en el tiempo t.','C','estado'),
 'x0':E('x₀, x(0)','Concentración al comenzar el intervalo; selecciona una trayectoria.','C','condición inicial'),
 'alpha':E('α','Producción constante por unidad de volumen y tiempo.','C/T','parámetro'),
 'delta':E('δ','Constante de pérdida de primer orden; δx es una tasa, mientras que δ es una constante.','1/T','parámetro'),
 'exp':E('e, exp, ln','e es la base del logaritmo natural; exp(a)=e elevado a a; ln es su función inversa. Sus argumentos deben ser adimensionales.','argumento y resultado sin unidad','operaciones'),
 'der':E('d/dt, prima (′)','Derivada temporal: velocidad instantánea. x′ abrevia dx/dt; se divide la unidad de x entre la de tiempo.','unidad del estado/T','operador'),
 'partial':E('∂','Derivada parcial: cambia una entrada manteniendo fijas las demás. Indica siempre respecto a cuál se deriva.','unidad de salida/unidad de entrada','operador'),
 'star':E('* en superíndice','Valor estacionario que hace cero las derivadas del modelo autónomo. No afirma estabilidad.','unidad de la variable','etiqueta'),
 'sum':E('Σ, Π e índices','Σ suma y Π multiplica sobre los índices indicados. i o j nombran componentes o datos; no son especies adicionales.','según los sumandos o factores','operadores'),
 'approx':E('≈, ≃, ∝','≈ y ≃ indican una aproximación; ∝, proporcionalidad con una constante no escrita. La hipótesis que permite usarlos se explica en el paso.','según cada miembro','relación'),
 'integral':E('∫, ds','Integral: acumula contribuciones. s es aquí un tiempo auxiliar y ds su elemento; los límites fijan el intervalo.','unidad del integrando × T','operador'),
}

BANK={}
def bank(ch,raw,base=()):
    d={k:COMMON[k] for k in base}
    for line in raw.strip().splitlines():
        if not line.strip():continue
        key,symbol,meaning,units,role=line.split('|')
        d[key]=E(symbol,meaning,units,role)
    BANK[ch]=d

bank('edo',r'''
z|z|Desviación respecto al equilibrio: z=x−α/δ. Puede ser negativa aunque x no lo sea.|C|estado desplazado
a|a(t), a(s)|Producción prescrita variable en el tiempo; a(s) es la misma función en el tiempo auxiliar s.|C/T|entrada
D|D(t), D(s)|Pérdida acumulada: D(t)=∫₀ᵗδ(s)ds; su exponente no lleva unidades.|1|función acumulada
T|T|Instante en que se retira la producción en este ejemplo por tramos; x(T) es el estado alcanzado entonces.|T|evento
E|E(t)|Concentración de la enzima del ejemplo de represión; t está en horas.|nM|estado
nums|8; 12; 1,04; 0,3; 5|8 nM es el nuevo equilibrio; 12 nM/h la capacidad de producción; 1,04=1+(1/5)² la represión inicial; 0,3/h la pérdida fija; 5 h el cambio de entrada. Los exponentes usan números expresados en estas unidades.|unidades indicadas|constantes docentes
''',('t','x','x0','alpha','delta','exp','der','integral'))
bank('reacciones',r'''
a|a, b|Concentraciones libres de dos especies que se interconvierten; cada reacción pierde una y gana la otra.|C|estados
k|k₁, k₂|Constantes de conversión A→B y B→A, respectivamente; sus productos con a o b son tasas.|1/T|parámetros
vx|x en negrita|Vector ordenado de concentraciones; cada fila sigue una especie distinta.|C por componente|estado vectorial
N|N|Matriz estequiométrica: columna j contiene el cambio neto de cada especie en la reacción j.|1 en esta convención|matriz de contabilidad
v|v(x; θ)|Vector de velocidades de reacción; θ reúne los parámetros que las determinan.|C/T por componente|flujos
V|V, V(t)|Volumen del compartimento; si crece, diluye la concentración aunque no retire cantidad.|volumen|geometría
n|n|Cantidad de sustancia de la especie; x=n/V. No es el exponente de Hill de otros capítulos.|cantidad|estado de cantidad
zt|z, τ|Concentración y tiempo normalizados: z=δx/α y τ=δt, con α y δ positivas.|1|variables adimensionales
c|c|Concentración de complejo A:B en el problema de unión; se elige la raíz que respeta 0≤c≤min(A total,B total).|C|estado de unión
nums|20, 80|Coeficientes del polinomio del ejemplo: 20 tiene unidad C y 80 tiene C². Los tres términos se comparan en C².|C y C²|coeficientes docentes
''',('t','x','der'))
bank('c08',r'''
j|j, xⱼ, xⱼ₊₁|j es el índice entero de paso; xⱼ aproxima x en tⱼ y xⱼ₊₁ en tⱼ+h.|índice 1; x en C|discretización
h|h|Paso temporal del algoritmo de Euler; no es la función de observación de otros capítulos.|T|control numérico
tol|sᵢ, atolᵢ, rtol|sᵢ escala el error permitido del componente i; atolᵢ fija tolerancia absoluta y rtol relativa. |sᵢ y atolᵢ en Cᵢ; rtol en 1|control numérico
i|i, xᵢ|i selecciona la especie; xᵢ es su estado. El valor absoluto mide tamaño sin signo.|Cᵢ|componente
nums|2; 8; 0,5; 2,943|Se evalúa a t=2 unidades de tiempo; x₀=8 unidades de concentración; δ=0,5 por unidad temporal; el resultado aproximado es 2,943 en la misma concentración.|unidades del ejemplo|sustitución numérica
''',('t','x','x0','delta','der','exp','approx'))
bank('c09',r'''
m|m, m(t), m₀, m*|Concentración de ARN; m₀ es la inicial y m*=α/γₘ la estacionaria bajo producción constante.|C de ARN|estado y valores de referencia
p|p, p(t), p₀, p*|Concentración de proteína; subíndice 0 indica inicio y asterisco equilibrio.|C de proteína|estado y valores de referencia
alpha|α|Producción de ARN en el volumen elegido.|C de ARN/T|parámetro
beta|β, k, kₜ|Constante de traducción que convierte ARN en tasa de producción proteica; son nombres alternativos en los ejemplos señalados.|C de proteína/(C de ARN·T); 1/T si comparten escala|parámetro
gm|γₘ, γₚ|Constantes de pérdida de ARN y proteína, respectivamente; no confundir con sus tasas γₘm y γₚp.|1/T|parámetros
mc|mₙ, m꜀|Concentraciones de ARN nuclear y citoplasmático; sus volúmenes son distintos.|C de ARN|estados por compartimento
gc|γₙ, γ꜀, kₑ|Pérdidas en núcleo y citoplasma, y exportación desde el núcleo, respectivamente.|1/T|parámetros
vol|Vₙ, V꜀|Volúmenes nuclear y citoplasmático; Vₙ/V꜀ convierte el mismo flujo de cantidad a tasa de concentración citoplasmática.|volumen; cociente 1|geometría
pi|pᵢ, pₘ|Proteína inmadura y madura; la maduración transfiere moléculas entre ambos estados.|C de proteína|estados
mat|kₘₐₜ, γᵢ, γₘ⁽ᵖ⁾|Constantes de maduración, pérdida inmadura y pérdida madura. γₘ⁽ᵖ⁾ se refiere a proteína madura, no a ARN.|1/T|parámetros
''',('t','der','exp','star'))
bank('c16',r'''
theta|θ|Fracción de promotores unidos al regulador: promotor ocupado/promotor total; entre cero y uno.|1|ocupación
r|r, [R], R|Concentración libre de regulador en las fórmulas de ocupación o Hill; los corchetes indican concentración.|C|entrada o estado regulador
Kd|K_d|Constante de disociación k_off/k_on; mayor valor implica menor ocupación al mismo regulador libre.|C|parámetro de unión
K|K|Escala de regulación de Hill; coincide con la mitad de la amplitud en la función escrita, no siempre con una constante molecular de disociación.|C|parámetro efectivo
n|n|Exponente de Hill que controla la forma de la curva; una estimación efectiva no cuenta automáticamente sitios físicos.|1|parámetro efectivo
rates|α_rep, α_min, α_max|Producción efectiva bajo represión, producción mínima y máxima. Las dos últimas son constantes del modelo reducido.|C/T|tasa y parámetros
h|h, H(R)|Fracción reguladora activadora entre cero y uno; su pendiente en K es n/(4K).|1; pendiente en 1/C|función
AB|A, B, a, b|A y B son reguladores; a=A/K_A y b=B/K_B son sus actividades normalizadas en el modelo de cuatro estados.|A,B en C; a,b en 1|entradas y normalización
ar|α(A,B), α₀, α_A, α_B, α_AB|Producción media ponderada y producciones de los estados vacío, solo A, solo B y ambos ocupados.|C/T|tasas de estado promotor
on|k_on, k₁|Constante bimolecular de asociación; k_on·r es una frecuencia cuando r es concentración libre.|1/(C·T)|parámetro de unión
off|k_off, k₋₁|Constante de disociación del complejo.|1/T|parámetro de unión
cat|k_cat|Frecuencia de conversión catalítica del complejo enzima-sustrato en producto.|1/T|parámetro catalítico
c|c, C|Concentración del complejo enzima-sustrato; aquí C es una variable, no la abreviatura general de unidad de concentración.|concentración|estado
ET|E_T, E|Enzima total y libre, respectivamente; E_T=E+C en este mecanismo cerrado para la enzima.|concentración|total conservado y estado libre
s|s, S|Concentración libre de sustrato en Michaelis–Menten.|concentración|estado o entrada fijada
KM|K_M|Cociente (disociación+catálisis)/asociación. Es una concentración; no equivale en general a K_d.|concentración|parámetro compuesto
v|v, V_max|v es la velocidad de formación de producto; V_max=k_cat E_T es su capacidad en la aproximación saturante.|concentración/T|tasa y capacidad
mass|k, [A], [B]|[A] y [B] son reactivos libres; k es su constante bimolecular en v=k[A][B].|A,B en C; k en 1/(C·T)|reactivos y parámetro
sv|x en negrita, S, v en negrita|Vector de estados, matriz estequiométrica y vector de velocidades. S en esta fórmula es una matriz, no sustrato.|C; 1; C/T, respectivamente|contabilidad vectorial
PR|[P], [PR], P_T|Promotor libre, complejo promotor-regulador y promotor total. P_T=[P]+[PR].|C|estados y total
freeR|[R]|Concentración libre del regulador que ocupa el promotor.|C|entrada o estado
basal|r, b, V|Aquí r es tasa de producción, b su fuga constante y V su amplitud regulada. V no es volumen en esta ecuación.|C/T|tasa y parámetros
''',('t','der','partial','approx'))
bank('c11',r'''
x|x, xᵢ, x*|Estado escalar, componente i de un sistema y equilibrio. En ejemplos normalizados su unidad es uno.|C o 1 según el ejemplo|estados
eta|η, η en negrita|Perturbación pequeña respecto al equilibrio: x−x*. Puede tener signo aunque x sea no negativo.|misma unidad que el estado|desviación
f|f, fᵢ, f′|Campo de velocidades y su componente i; f′ es su derivada respecto al estado en el caso escalar.|C/T; f′ en 1/T|campo y pendiente
alpha|α, a|Capacidad de producción en la represión de primer orden; en autoactivación normalizada a es una capacidad sin unidad.|C/T o 1 en la ecuación normalizada|parámetro
K|K, n|Escala de regulación K y exponente de Hill n.|K en C; n en 1|parámetros
J|J, Jᵢⱼ|Jacobiano del campo respecto a estados, evaluado en el equilibrio; la entrada i,j describe cómo xⱼ modifica la velocidad de xᵢ.|Cᵢ/(T·Cⱼ)|matriz local
lambda|λ, λ₁, λ₂|Autovalores del Jacobiano: tasas de crecimiento o decaimiento de perturbaciones; pueden ser complejos.|1/T o 1 en tiempo normalizado|tasas modales
TD|T, Δ|Aquí T=traza(J) y Δ=det(J); T no es tiempo y Δ no es una concentración.|T en 1/tiempo; Δ en 1/tiempo²|invariantes de matriz
theta|N, θ|N es el número de estados; θ es el vector de parámetros del campo.|N en 1; θ con unidades por componente|tamaño y parámetros
mp|m, p|ARN y proteína del ejemplo m′=4−2m, p′=3m−p; ambos comienzan en cero. Aquí t se mide en horas.|nM|estados
nums|4, 2, 3, 1; 6|4 es producción de ARN en nM/h; 2, 3 y 1 son constantes en 1/h. Los equilibrios son m*=2 nM y p*=6 nM; el 6 de p(t) es esa concentración estacionaria.|unidades indicadas|constantes docentes
b|b|Fuga de producción en la autoactivación normalizada; en las raíces mostradas se fija b=0 y a=3.|1|parámetro
roots|x*₀, x*₊, x*₋|Tres candidatos a equilibrio del ejemplo con b=0 y a=3; los signos ± etiquetan raíces, no incertidumbres.|1|equilibrios candidatos
''',('t','der','partial','star','delta','approx','exp'))
bank('c13',r'''
xy|x, y|Concentraciones normalizadas de los dos represores que se inhiben mutuamente.|1|estados
tt|t, τ|Tiempo normalizado por la constante de pérdida; aquí t también se usa en las ecuaciones normalizadas desarrolladas.|1|variable independiente
a|a, α|Capacidad normalizada de producción respecto a pérdida y escala reguladora; en el ejemplo desarrollado α=10.|1|parámetro
n|n|Exponente de Hill de la represión cruzada.|1|parámetro
J|J₁₂|Derivada de la primera velocidad respecto a y; componente fuera de diagonal del Jacobiano.|1 en tiempo normalizado|coeficiente local
nums|10, 96|α=10; 96=10²−4 es el discriminante que separa las dos soluciones asimétricas.|1|constantes del ejemplo
''',('der','star'))
bank('bifurcaciones',r'''
x|x*, x*₊, x*₋|Estado de equilibrio seguido al variar un parámetro; ± distingue dos ramas, no dos tiempos.|unidad del estado; 1 en el ejemplo de autoactivación|equilibrio
mu|μ|Parámetro de continuación; su unidad depende del parámetro que se varía.|unidad declarada del parámetro|parámetro
f|f|Velocidad escalar cuya raíz define el equilibrio; las parciales indican qué argumento se varía.|unidad del estado/T|campo
a|a|Capacidad de autoactivación normalizada; las ramas no nulas reales requieren a≥2 en el dominio positivo del ejemplo.|1|parámetro
''',('partial','approx','star'))
bank('c14',r'''
x|x₁, x₂, x₃|Tres represores normalizados en un anillo; el último inhibe al primero y se cierra el ciclo.|1|estados
t|t|Tiempo normalizado por la constante de pérdida común.|1|variable independiente
alpha|α, n|Capacidad normalizada de producción y exponente de Hill.|1|parámetros
s|s|Concentración normalizada del equilibrio simétrico x₁=x₂=x₃=s; no es una tasa de producción aquí.|1|equilibrio
g|g|Magnitud de la pendiente represora en el equilibrio, definida por n·sⁿ/(1+sⁿ); controla la ganancia local.|1|ganancia local
lambda|λ, λ₁, λ₊, λ₋|Autovalores en el tiempo normalizado; el signo de su parte real decide estabilidad local en el caso hiperbólico.|1|tasas modales normalizadas
i|i, π|i es la unidad imaginaria (i²=−1); π es la constante geométrica. Ninguna es una especie o parámetro ajustado.|1|constantes matemáticas
T|T|Período de la oscilación lineal en el umbral del ejemplo (g=2); no es el período universal del ciclo no lineal.|tiempo normalizado|predicción local
''',('der','star','approx'))
bank('c15',r'''
y|y(t)|Salida del ejemplo lineal de pulso; y(0)=0, con una entrada escalón de amplitud U.|unidad de salida|estado
U|U|Amplitud del escalón aplicado al inicio.|unidad de entrada|entrada
rates|b, e, c|b y e son constantes de relajación distintas; c convierte la señal en tasa de salida. e en e^(−bt) es la base exponencial, pero e multiplicando t es aquí una constante de relajación.|b,e en 1/T; c en salida/(entrada·T)|parámetros
freq|G(iω), ω, φ(ω)|G es la respuesta lineal en frecuencia; ω es frecuencia angular de entrada; φ es el desfase de la salida.|G en salida/entrada; ω en rad/T; φ en rad|respuesta frecuencial
k|k, δ|Ganancia de producción k y pérdida δ del filtro lineal.|k en salida/(entrada·T); δ en 1/T|parámetros
HA|H_A(A), H_B(B)|Fracciones activadoras entre cero y uno para las entradas A y B.|1|funciones de regulación
AB|A, B, K_A, K_B, n_A, n_B|A y B son entradas; K_A y K_B sus escalas de media activación; n_A y n_B exponentes de Hill.|entradas y K en C; n en 1|entradas y parámetros
z|z, β, δ|z es salida de la compuerta, β capacidad de producción y δ pérdida de primer orden.|z en C; β en C/T; δ en 1/T|estado y parámetros
uy|u, y, z, t|En los ejemplos normalizados u es entrada y y,z son estados; t es tiempo en la escala elegida. En y′=u−y la relajación está fijada a uno.|1|variables normalizadas
tau|τ_y, τ_z|Tiempos de relajación de las etapas adaptadoras; al multiplicar la derivada equilibran las unidades.|unidad del tiempo de ese ejemplo|parámetros
''',('der','exp','approx'))
bank('c17',r'''
x|x(t), x(t−τ)|Estado actual y estado en un tiempo anterior; la EDO con retraso necesita una historia inicial.|C|estado e historia
t|t, τ, τ_c|Tiempo, retraso fijo y retraso crítico de la rama calculada, respectivamente.|T|tiempo y parámetros
f|f|Producción regulada por el estado retrasado.|C/T|función de tasa
delta|δ, d|Pérdida instantánea de primer orden; nombres usados en dos escrituras de la linealización.|1/T|parámetro
gain|g, a|Magnitud de la pendiente represora retrasada en el equilibrio, con el signo negativo escrito fuera.|1/T|ganancia local
eta|η|Pequeña perturbación respecto al equilibrio.|C|desviación
lambda|λ, ω|λ es tasa modal posiblemente compleja; ω es frecuencia angular al buscar λ=iω.|1/T; ω en rad/T|análisis local
chain|y₁, yⱼ, yⱼ₋₁, m, j|y son etapas intermedias; m es el número de etapas; j su índice. Cada etapa tiene tiempo medio τ/m.|y en C; m,j en 1|estados e índices
trig|sin, cos, arccos|Funciones trigonométricas y coseno inverso; sus argumentos angulares son adimensionales. La fórmula de τ_c elige la primera rama positiva indicada.|argumentos en rad|operaciones
''',('der','exp','approx'))
bank('control',r'''
z|z(t), z(0)|Memoria integral y su valor inicial; acumula el error r−y. Su unidad incluye un factor de tiempo.|unidad de salida × T|estado de control
ry|r, y(s), y(t)|r es referencia deseada; y es salida observada en tiempo s o t. Deben medirse en la misma escala.|unidad de salida|referencia y salida
zs|z₁, z₂|Especies controladoras que se secuestran o aniquilan juntas en el modelo antitético.|C|estados
mu|μ|Producción constante de la primera especie controladora.|C/T|parámetro
theta|θ|Conversión de salida y a producción de z₂.|C de z₂/(C de y·T)|parámetro
eta|η|Constante bimolecular de secuestro compartido; ηz₁z₂ aparece igual en ambos balances.|1/(C·T)|parámetro
kg|k, γ|k convierte z₁ en producción de y; γ es pérdida de y.|k en C de y/(C de z₁·T); γ en 1/T|parámetros
y|y|Concentración de salida controlada.|C|estado
''',('t','der','integral'))
bank('c32',r'''
v|v_A, v_B|Tasas de producción asignadas a los dos módulos que comparten recurso.|C/T|flujos
resource|k_A, k_B, R_T, d_A, d_B|k son frecuencias de procesamiento; R_T es recurso total; d son demandas normalizadas. El denominador representa competencia compartida.|k en 1/T; R_T en C; d en 1|parámetros y demandas
x|x|Concentración libre de la salida a la que se conecta una carga.|C|estado libre
c|c(x), c′(x), D_T, K_d|c es concentración unida a carga; c′ su derivada respecto a x; D_T es carga total y K_d disociación. El factor 1+c′ enlentece la dinámica en esta reducción.|c,D_T,K_d en C; c′ en 1|carga y parámetros
f|f(x)|Velocidad que tendría el módulo aislado antes de conectar la carga rápida.|C/T|campo sin carga
ctl|z, K_i, r, y|z es estado controlador; K_i ganancia integral; r referencia e y salida con la misma unidad.|K_i en unidad z/(unidad y·T); z,r,y según su escala|controlador
pop|N₁(t), N₂(t), μ₁, μ₂|Tamaños de las dos poblaciones y sus tasas netas de crecimiento; el cociente cambia si sus tasas difieren.|N en conteo; μ en 1/T|estados y parámetros
chain|x, y, z, Δx, Δz, f′(x), g′(y)|x es entrada, y=f(x) intermedia y z=g(y) salida; Δ indica pequeños cambios. Las pendientes de los dos módulos se multiplican por regla de la cadena.|Δ en unidades de sus variables; pendientes en salida/entrada|propagación local
XY|X, Y|Represor intermedio y salida del ejemplo incoherente que comparten dosificación D.|C|estados
D|D|Dosificación del constructo, tratada como factor normalizado de abundancia de plantillas; no es difusión en estas ecuaciones.|1|entrada de dosificación
prod|α, β|Capacidades productivas por unidad del factor de dosificación.|C/T|parámetros
loss|δ, γ, K|Pérdida de X, pérdida de Y y escala de represión sobre la producción de Y.|δ,γ en 1/T; K en C|parámetros
''',('t','der','exp','approx','star'))
bank('acoplados',r'''
psi|ψ|Diferencia de fase entre dos osciladores; no es diferencia de concentración.|rad|estado reducido
dw|Δω|Diferencia entre frecuencias angulares naturales sin acoplar.|rad/T|parámetro
K|K|Intensidad de acoplamiento de fase. No es una constante de disociación.|1/T en la convención angular elegida|parámetro
sin|sin ψ|Seno de la diferencia de fase; la periodicidad identifica fases separadas por 2π.|1|función
''',('t','der'))
bank('c18',r'''
uv|u, v, uᵢ|Concentraciones espaciales; uᵢ aproxima u en el nodo i de una malla.|C|campos y estados discretos
space|x, r, h|x o r representan posición espacial; h es separación entre nodos. x aquí puede ser posición, no concentración.|longitud|geometría y malla
D|D, D_u, D_v|Coeficientes de difusión de las especies; en J_k la D en negrita/diagonal reúne esos coeficientes.|longitud²/T|parámetros
fg|f(u), f(u,v), g(u,v), fᵢ(xᵢ)|Términos locales de reacción para cada especie o célula, antes del intercambio.|C/T|campos de reacción
J|J en la ley de Fick|Densidad de flujo en la dirección r; el signo negativo lleva material hacia concentraciones menores.|C·longitud/T|flujo por área
Jac|J, J_k|Jacobiano local de reacción y Jacobiano del modo espacial de número de onda k. En estas fórmulas J no es flujo.|1/T si ambas especies usan igual escala|matrices de estabilidad
k|k, q|k es número de onda espacial; q=k² en el ejemplo polinómico normalizado.|k en 1/longitud; q en 1/longitud² o 1 tras normalizar|modo espacial
TD|Δ, Δ(k), f_u, g_v|Δ=det(J); Δ(k) es determinante del modo k; f_u y g_v son derivadas parciales locales respecto a u y v.|Δ en 1/T²; derivadas en 1/T|análisis modal
net|xᵢ, xⱼ, Aᵢⱼ, D|x son concentraciones celulares; A es adyacencia; D aquí es tasa efectiva de intercambio en una red, distinta de difusión continua.|x en C; A en 1; D en 1/T|red discreta
pair|x₁, x₂, 6, e^(−t)|Concentraciones de dos compartimentos del ejemplo; diferencia inicial 6 en su unidad de concentración y tasa de relajación normalizada a uno.|C; tiempo en la escala del ejemplo|solución docente
poly|1, 7, 10|Coeficientes del determinante del ejemplo de Turing después de normalizar espacio y tiempo; q es el número de onda al cuadrado.|1 en las escalas indicadas|coeficientes docentes
''',('t','der','partial','sum','exp'))
bank('c20',r'''
prob|P(X=x)|Probabilidad de que el conteo aleatorio X tome el valor entero x.|1|distribución
Pn|Pₙ, Pₙ₋₁, Pₙ₊₁|Probabilidad de tener n moléculas y probabilidades de los estados vecinos; P₋₁ se toma cero.|1|distribución
n|n, N, X, x|n y x son valores enteros; N y X variables aleatorias de conteo. No son concentraciones continuas aquí.|conteo, formalmente unidad 1|estado discreto
kd|k, δ|k es frecuencia de nacimiento independiente del estado; δ frecuencia de pérdida por molécula. δn es frecuencia total de pérdida.|k en eventos/T; δ en 1/T|parámetros
EV|E[·], Var(·)|E calcula esperanza o promedio probabilístico; Var calcula dispersión cuadrática respecto a esa media.|media en unidad X; varianza en unidad X²|operadores estadísticos
pois|m, x!|m es media de la distribución de Poisson y x! el factorial entero; m no es ARN en esta fórmula.|m en conteo; factorial en 1|parámetro y operación
bayes|A, B, P(A), P(B), P(A∣B)|A y B son eventos; P indica probabilidad; la barra significa condicionado a. Se requiere P(B)>0.|1|probabilidad
master|p(x,t), x, aⱼ(x), νⱼ|x es vector de conteos; p es probabilidad de ese estado; aⱼ su propensión de reacción j; νⱼ vector entero de cambio por evento. x−νⱼ es el estado que llega a x.|p en 1; a en 1/T; ν en conteos|proceso de saltos
wait|τ, r₁, a₀|τ es próxima espera; r₁ un uniforme estrictamente entre 0 y 1; a₀ suma de propensiones en el estado actual y debe ser positiva.|τ en T; r₁ en 1; a₀ en 1/T|muestreo de eventos
''',('t','der','sum','exp'))
bank('c21',r'''
pon|p_on|Probabilidad de que el promotor esté encendido; en expresiones estacionarias se usa su valor k_on/(k_on+k_off).|1|estado probabilístico
rates|k_on, k_off|Frecuencias de activación y apagado del promotor de dos estados; aquí ambas son de primer orden, a diferencia de k_on bimolecular de unión.|1/T|parámetros
prod|r, s|Producción de ARN mientras el promotor está ON; nombres usados en las dos escrituras del mismo mecanismo.|conteos/T|parámetro
loss|γ, d|Pérdida de primer orden por ARN; d aquí es una constante, no el símbolo de derivada.|1/T|parámetro
counts|M, N, X, m*|Variables aleatorias de conteo; m* es la media estacionaria de N.|conteos|estados y media
F|F|Factor de Fano: varianza/media para conteos con media positiva.|1 con conteos tratados como unidad 1|dispersión relativa
stat|E[·], Var(·), X∣Z|Esperanza, varianza y condicionamiento al estado o contexto Z; la identidad de varianza total separa variación interna y entre contextos.|según la variable; varianza en unidad²|operadores estadísticos
CLE|β, δ, dX, dt|En la aproximación difusiva β es frecuencia de nacimientos y δ pérdida por molécula; dX es incremento de conteo continuo aproximado durante dt.|β en conteos/T; δ en 1/T; dt en T|aproximación estocástica
W|dW₁, dW₂|Incrementos independientes de Wiener, con media cero y varianza dt; sus raíces cuadradas de propensiones escalan el ruido.|raíz de T|ruido continuo
''',('t','der','exp','sum','star','approx'))
bank('c22',r'''
UF|U, F|Proteína inmadura y fluorescente madura. F es un estado, no el factor de Fano de otro capítulo.|C|estados
s|s(t)|Producción efectiva que alimenta la proteína inmadura.|C/T|entrada de producción
rates|k_m, λ|Constantes de maduración y pérdida común, respectivamente.|1/T|parámetros
obs|E[y], b, g|Lectura media del detector, fondo aditivo y ganancia que convierte proteína madura a señal.|y,b en u.a.; g en u.a./C|modelo de observación
num|1020|Lectura media numérica en unidades arbitrarias del ejemplo; no es una concentración de proteína.|u.a.|predicción docente
''',('t','der'))
bank('sensibilidad',r'''
x|x, α, δ, t|x=α(1−exp(−δt))/δ con x₀=0; α es producción y δ pérdida. La derivada mantiene α,t e inicio fijos.|x en C; α en C/T; δ en 1/T; t en T|solución y parámetros
S|Sⱼ|Vector ∂x/∂θⱼ de sensibilidades de los estados al parámetro j. Su inicio también se deriva si depende del parámetro.|Cᵢ/unidad θⱼ por componente|estado de sensibilidad
J|J_x, f, θⱼ|J_x es Jacobiano del campo f respecto a estados; ∂f/∂θⱼ es efecto paramétrico directo; θⱼ es el parámetro elegido.|J_x en Cᵢ/(T·Cₖ); parcial en Cᵢ/(T·unidad θⱼ)|coeficientes de sensibilidad
''',('der','partial','exp','approx'))
bank('c23',r'''
theta|θ, θ estimado (sombrero)|Vector de parámetros del modelo; sombrero indica el estimador obtenido del ajuste.|por componente según el modelo|parámetros y estimador
L|L(θ), −log L|Verosimilitud de los datos y su logaritmo negativo; el log usa la densidad en la convención de unidades declarada.|densidad conjunta y objetivo numérico|criterio estadístico
data|yᵢ, μᵢ(θ), hᵢ(θ)|Dato i y predicción de su media (dos nombres); se comparan en la escala del instrumento.|unidad de observación|datos y predicción
sigma|σᵢ|Desviación típica del error del dato i; debe ser positiva; σᵢ² es varianza.|unidad de observación|modelo de error
J|J(θ)|Suma de residuos normalizados al cuadrado; aquí J es objetivo de ajuste, no Jacobiano.|1|objetivo
fit|tᵢ, yᵢ, 28,5, 14, 2,0357|En el ajuste lineal y=θt sin intercepto, tᵢ son tiempos e yᵢ datos; 28,5=Σtᵢyᵢ, 14=Σtᵢ² y 2,0357 aproxima la pendiente ajustada.|t en T; y en señal; pendiente en señal/T|ejemplo de mínimos cuadrados
bayes|p(θ∣y), p(y∣θ), p(θ), y|Posterior, verosimilitud, prior y conjunto de datos. La proporcionalidad deja implícita la evidencia normalizadora.|densidades en sus variables y unidades declaradas|inferencia bayesiana
pi|π|Constante matemática que entra en la normalización de la densidad gaussiana.|1|constante
''',('sum','exp','approx'))
bank('c24',r'''
y|y(t)|Predicción de observación; no necesariamente concentración biológica.|unidad del detector|salida
Ag|A, g|A es amplitud biológica y g ganancia del detector; en gA·exp(−kt) solo su producto se identifica de esa observación. En A(1−exp(−kt)), A ya es amplitud en unidades de salida.|A según la fórmula; g en salida/unidad biológica|parámetros
k|k|Constante de decaimiento o relajación del ejemplo; distinta de traducción o asociación de otros capítulos.|1/T|parámetro
S|S_θ(t), θ|Sensibilidad de la salida al parámetro θ: mantiene los otros parámetros y el diseño fijos.|unidad y/unidad θ|función de sensibilidad
I|I_ab|Entrada a,b de información de Fisher bajo errores normales independientes con varianzas conocidas y fijas.|1/(unidad θ_a·unidad θ_b)|información local
h|hᵢ, θ_a, θ_b, σᵢ|Media predicha del dato i, parámetros que se derivan y desviación típica de ese dato.|h,σ en salida; θ con unidades propias|observación y parámetros
''',('t','partial','sum','exp'))
bank('caso-bacteriano',r'''
M|M₀, M₁, M₂|Concentraciones de ARN de los tres genes del anillo; el subíndice identifica el gen, no un tiempo.|nM de ARN|estados
P|P₀, P₁, P₂|Concentraciones proteicas; P₂ reprime M₀, P₀ reprime M₁ y P₁ reprime M₂.|nM de proteína|estados reguladores
s|s_b, s_v|Producción basal y amplitud regulada de transcripción; permanecen constantes en la simulación declarada.|nM de ARN/h|parámetros
K|K, n, γ_m|Escala de represión, exponente de Hill y constante de pérdida del ARN, respectivamente.|K en nM de proteína; n en 1; γ_m en 1/h|parámetros
''',('t','der'))
bank('c25',r'''
n|n, s|n es cantidad de la especie y s su producción en cantidad por tiempo; no son concentración ni exponente de Hill.|n en cantidad; s en cantidad/T|estado y producción
x|x, x₁, x₂|Concentración general y concentraciones en dos células. Se obtiene x=n/V.|C|estados
V|V, dV/dt|Volumen y velocidad de crecimiento de volumen.|volumen y volumen/T|geometría
mu|μ|Tasa relativa de expansión (1/V)dV/dt; aporta pérdida de concentración por dilución.|1/T|crecimiento
alpha|α, α₁, α₂|Producción por volumen y tiempo en la célula indicada.|C/T|parámetros
k|k|Tasa efectiva de intercambio entre dos células de igual convención de volumen.|1/T|parámetro
num|6, 0,3, 20|α=6 C/T y δ+μ=0,3/T dan equilibrio 20 C; son valores docentes de ese ejemplo.|unidades indicadas|sustitución numérica
half|t₁/₂, ln 2, 2,31|Semivida de la distancia al equilibrio; ln 2 es constante sin unidad y 2,31 está en la unidad temporal elegida.|T|escala temporal
''',('t','der','delta','exp','star','approx'))
bank('c26',r'''
S|S(t), S(0), S*|Concentración del sensor actual, inicial y estacionaria; su abundancia disminuye cuando aumenta la retirada inducida.|C de sensor|estado y referencias
a|a, a(t)|Entrada que acelera la retirada del sensor; se expresa en la escala de auxina que se declare o calibre.|unidad de entrada A|entrada
p|p|Producción de sensor; aquí p no es probabilidad ni proteína de otros capítulos.|C de sensor/T|parámetro
delta|δ|Pérdida basal de primer orden del sensor.|1/T|parámetro
k|k|Conversión de entrada a pérdida adicional: ka tiene unidad 1/T.|1/(A·T)|parámetro de sensibilidad
dr|da/dr|Derivada de la entrada inferida respecto al cociente r; mide cuánto se amplifica un cambio de lectura normalizada.|unidad A por unidad de r|sensibilidad
r|r|Cociente S*(a)/S*(0), relativo al sensor en ausencia de entrada y en equilibrio.|1|lectura normalizada
''',('t','der','partial','exp','star'))
bank('c27',r'''
h|h(a), h(b)|Fracciones de activación saturantes de las dos entradas; entre cero y uno.|1|funciones
a|a, b, K, n|a,b son concentraciones de entrada; K escala de media activación y n exponente de Hill.|a,b,K en C; n en 1|entradas y parámetros
y|y, ℓ, H|Salida, nivel mínimo y máximo de la compuerta. H mayúscula aquí es nivel, no función de Hill.|unidad de salida|salida y parámetros
theta|θ|Umbral que clasifica una lectura como ON u OFF; debe estar entre los extremos indicados.|unidad de salida|criterio de lectura
margin|y_OFF,max, y_ON,min, M|Mayor salida de las condiciones OFF, menor salida de ON y margen entre ellas. M positivo permite separar con un umbral.|unidad de salida|margen de separación
spatial|yᵢ, yⱼ, αᵢ, δ, k, Nᵢ|Salidas de células; producción αᵢ; pérdida δ; intercambio k; Nᵢ conjunto de vecinas de i. Aquí k es intercambio discreto.|y en C; α en C/T; δ,k en 1/T; índices en 1|red celular
''',('t','der','sum'))
bank('c28',r'''
p|p, p(t), p_falso|Fracción o probabilidad de registro; p_falso se refiere al registro sin señal deseada.|1|estado probabilístico
lambda|λ, λ(t)|Frecuencia de registro condicionada a que aún no se haya registrado; no es probabilidad por sí sola.|1/T|tasa de evento
F|F, α₀, α₁, δ_F|Reportero continuo, producciones en configuraciones no registrada y registrada, y pérdida del reportero.|F en C; α en C/T; δ_F en 1/T|estado y parámetros
eps|ε, T|ε es frecuencia basal de registro falso; T duración de exposición. No es ruido aditivo en esta fórmula.|ε en 1/T; T en tiempo|parámetro y diseño
rho|ρ|Frecuencia de reversión desde el estado registrado al no registrado.|1/T|parámetro
''',('t','der','exp','integral'))
bank('c29',r'''
mpz|m, p, z|ARN, proteína intermedia y represor final del oscilador reducido; no reconstruyen por sí solos toda la red vegetal.|C por especie|estados
reg|α, K, n|Capacidad de transcripción, escala de represión del represor z y exponente de Hill.|α en C de ARN/T; K en C de z; n en 1|parámetros
prod|β, γ|Conversión de ARN a producción de p y de p a producción de z.|unidad de producto/(unidad de precursor·T)|parámetros
loss|δ_m, δ_p, δ_z|Constantes de pérdida de las tres especies; se multiplican por su estado correspondiente.|1/T|parámetros
curve|y(t), b, A, T, φ|Señal, fondo, amplitud, período y fase inicial del ajuste cosenoidal descriptivo.|y,b,A en señal; T en tiempo; φ en rad|ajuste de señal
phase|φ(t), ψ(t), ω, Ω, q|Fase del oscilador, diferencia φ−Ωt, frecuencia natural, frecuencia de estímulo y acoplamiento. φ(t) dinámica se distingue de la fase inicial del ajuste anterior.|fases en rad; frecuencias y q en 1/T angular|modelo de fase
pi|π, cos, sin|π es constante; seno y coseno reciben ángulos en radianes. 2πt/T es un ángulo sin dimensión.|1 o rad según la expresión|operaciones
''',('t','der','exp'))
bank('toggle-vegetal',r'''
Delta|Δ|Determinante del Jacobiano de dos estados; su signo ayuda a evaluar la estabilidad junto con la traza.|1/T²|invariante local
delta|δ_x, δ_y|Constantes de pérdida de los dos estados x e y.|1/T|parámetros
F|F_x′(y*), F_y′(x*)|Pendientes de las funciones de producción de x respecto a y y de y respecto a x, en el equilibrio indicado.|C_x/(T·C_y) y C_y/(T·C_x)|ganancias locales
''',('star',))
bank('c35',r'''
Nv|N, S, v en negrita|N o S es matriz estequiométrica y v vector de flujos. Nv=0 expresa balance estacionario, no ausencia de reacciones.|N,S en 1; v en C/T en esta convención|contabilidad de red
bounds|v_min, v_max|Límites inferior y superior por reacción; las desigualdades se aplican componente a componente.|misma unidad de v|restricciones
x|x|Vector de estados químicos en dx/dt=Sv.|C por componente|estado vectorial
energy|wᵢ, Eᵢ, k_B, T|wᵢ es peso de Boltzmann; Eᵢ energía del estado; k_B constante de Boltzmann; T temperatura absoluta (no tiempo). Eᵢ/(k_B T) es adimensional.|w en 1; E en energía; k_B en energía/K; T en K|pesos estadísticos
prob|Pᵢ, wᵢ, wⱼ|Probabilidad normalizada y pesos positivos; el denominador suma sobre todos los estados incluidos.|1|distribución
q|q, k_abre, k_cierra|Fracción de cromatina accesible y frecuencias de apertura y cierre del modelo de dos estados.|q en 1; k en 1/T|estado y parámetros
f|f, s|Fracción de una variante y diferencia de crecimiento neto que actúa como coeficiente de selección constante.|f en 1; s en 1/T|estado y parámetro
''',('t','der','sum','exp'))
bank('c33',r'''
class|TP, FP, FN|Número de enlaces verdaderos recuperados, enlaces falsos propuestos y enlaces verdaderos omitidos, respecto a la referencia declarada.|conteos|evaluación
score|precision, recall|Precisión es fracción correcta entre predicciones positivas; recall es fracción recuperada entre positivos reales. Requieren denominador no nulo.|1|métricas
''')
bank('c31',r'''
y|y_bpi, μ|Lectura de la célula/medida i en planta p del lote b, y media poblacional del modelo jerárquico.|unidad de señal|dato y media
random|u_b, v_bp, ε_bpi|Efectos de lote, planta dentro del lote y residuo de lectura; su estructura de dependencia debe declararse.|unidad de señal|efectos aleatorios
design|D_grupo, m, ρ|Factor de diseño de grupo, tamaño común del grupo y correlación intragrupo. D_grupo multiplica la varianza de la media bajo los supuestos del ejemplo.|1|dependencia y diseño
''')

# Lista explícita: cada ecuación recibe únicamente los significados pertinentes.
USE={}
def use(start,ch,rows):
    for i,row in enumerate(rows.strip().splitlines(),start):USE[i]=(ch,row.split())
use(1,'edo','''t x x0 alpha delta der
x delta der
t x x0 delta exp
t z x0 alpha delta der
t x x0 alpha delta exp
t x delta a der exp
t x x0 delta a exp integral
t x x0 D a exp integral
t x T delta exp
t E nums exp''')
use(11,'reacciones','''t a k der
t vx N v der
t x V n der
zt der
c nums''')
use(16,'c08','''x nums exp approx
t x delta der
j h delta
h delta
tol i''')
use(21,'c09','''t m p alpha beta gm der
t p m beta gm exp star
t p m beta gm exp star
t mc gc vol alpha der
t pi mat m beta der
t m alpha gm der
t p m beta gm der
m alpha gm star
p alpha beta gm star''')
use(30,'c16','''theta r Kd
rates r K n
h r K n partial
ar AB
t theta on off r der
c ET s KM on off cat approx
v cat c s KM ET approx
v mass
sv der
on off PR r
Kd on off
theta PR r Kd
basal freeR Kd
t c ET s on off cat der
c ET s KM approx
KM on off cat
v cat c s KM ET approx
h r K n''')
use(48,'c11','''t eta f x der approx star
f x alpha K delta
lambda TD
t x f theta der
t mp nums der
t mp nums der
t mp nums exp
t mp nums exp
t eta J der approx
J f x partial star
lambda TD
t x alpha K delta der
f x alpha K delta star
t x alpha b der
roots b star
roots b star
f x b''')
use(65,'c13','''xy tt a n der
xy tt a der
xy tt a der
xy a
xy a
xy
xy a nums
J xy a''')
use(73,'bifurcaciones','''x mu f partial star
x a star''')
use(75,'c14','''lambda g
t x alpha der
t x alpha der
t x alpha der
alpha s star
g alpha s
lambda g
lambda g i
T i approx''')
use(84,'c15','''t y U rates exp
freq k
HA AB
t z HA AB der
uy der
uy exp
uy tau der
uy tau der''')
use(92,'c17','''lambda delta gain t exp
t x f delta der
t eta gain delta der
lambda delta gain t exp
delta gain lambda t trig
lambda gain t trig
lambda gain delta
t gain delta trig
t chain x der
t chain der''')
use(102,'control','''t z ry integral
t zs mu theta eta y der
t y zs kg der
t zs mu theta y der''')
use(106,'c32','''v resource
t x c f der
t ctl der
t pop exp
chain approx
t XY prod D loss der
t XY prod D loss der
XY prod D loss star
XY prod D loss star
XY prod loss star approx''')
use(116,'acoplados','''t psi dw K sin der''')
use(117,'c18','''t uv D space fg partial
t uv D space fg der
TD k D
J D uv space partial
t uv fg D space partial
t uv fg D space partial
t net fg sum der
t pair exp
Jac k D
Jac k poly''')
use(127,'c20','''t Pn n kd der
t n kd EV der
n EV prob sum
n EV
n pois prob exp
bayes
t master sum der
wait exp''')
use(135,'c21','''t pon rates der
F counts stat prod rates loss
counts stat prod pon rates loss star
stat
pon rates
F prod rates loss
CLE W counts''')
use(142,'c22','''t UF s rates der
t UF rates der
UF obs num''')
use(145,'sensibilidad','''x partial exp
S J der partial''')
use(147,'c23','''L theta data sigma sum exp pi
J theta data sigma sum
theta fit sum
bayes theta approx''')
use(151,'c24','''t y Ag k exp
t S y partial
t y Ag k exp
I h sum partial''')
use(155,'caso-bacteriano','''t M P s K der
t M P s K der
t M P s K der''')
use(158,'c25','''t n delta der
t x n V delta der
mu V der
t x alpha delta mu der
t x alpha delta k der
t x alpha delta k der
x alpha delta mu num star
half exp approx''')
use(166,'c26','''t a S p delta k der
t S p delta k a der
S p delta k a star
r S delta k a star
a delta k r
a delta k r dr
t S delta k a exp star''')
use(173,'c27','''h a
y h a
margin theta
margin
t spatial sum der''')
use(178,'c28','''t p lambda der
t p lambda exp
t p lambda exp integral
t p lambda exp
t F p der
p eps exp
t p lambda rho der''')
use(185,'c29','''t mpz reg loss der
t mpz prod loss der
t mpz prod loss der
t curve pi
t phase pi der
t phase pi der''')
use(191,'toggle-vegetal','''Delta delta F star''')
use(192,'c35','''Nv bounds
energy exp
prob sum
t x Nv der
Nv
t q der
t f der''')
use(199,'c33','''class score
class score''')
use(201,'c31','''y random
design''')

NOTES={
 2:'Dividir entre x requiere x≠0 en el tramo considerado; el caso x=0 se comprueba por separado.',
 3:'La escritura logarítmica requiere x y x₀ positivos; x₀=0 se trata directamente en la ecuación diferencial.',
 8:'En esta fórmula la pérdida puede depender del tiempo; D integra esa pérdida, no es una constante de difusión.',
 10:'La fórmula numérica usa t en horas y devuelve E en nM; la entrada R pasa de 1 a 10 nM en t=5 h. K=5 nM y n=2 permanecen fijos.',
 16:'Se omiten unidades dentro de la sustitución numérica por brevedad; la clave las conserva.',
 19:'Condición de estabilidad de Euler para pérdida pura con δ>0. No es una condición de estabilidad biológica del circuito.',
 22:'Se asumen ARN y proteína iniciales cero y γₘ≠γₚ; la coincidencia de tasas se calcula por el límite.',
 23:'Válida para γₘ≠γₚ; si coinciden, la fracción se sustituye por su límite t·exp(−γₚt).',
 33:'El término ab presupone el modelo de ocupación independiente escrito; una interacción extra necesita otro peso.',
 35:'La aproximación exige la separación de escalas y condiciones descritas; K_M no se sustituye sin más por K_d.',
 61:'Todo está normalizado; no se suman directamente x² y una concentración dimensional sin dividir por una escala.',
 73:'Requiere ∂f/∂x≠0. Cerca de un pliegue esa división falla y se cambia el método de continuación.',
 83:'Es un cálculo local en el umbral del modelo normalizado, no una medida experimental de período.',
 84:'Se asume b≠e. Si son iguales, el límite es cU·t·exp(−bt). La letra e tiene aquí dos usos que se distinguen por posición.',
 91:'La división requiere y>0; la historia inicial no debe introducir una singularidad artificial.',
 99:'Se requiere a>d>0 para esta rama crítica. El coseno inverso tiene otras ramas; no se seleccionan sin analizar.',
 107:'Modelo reducido de unión rápida con totales y dominio físico declarados, no una ley universal para toda carga.',
 115:'Límite de dosificación alta: αD/(δK)≫1, con los demás parámetros fijos.',
 127:'En n=0 no hay pérdida hacia −1; la probabilidad P₋₁ se define cero.',
 134:'Si a₀=0, no hay próximo evento mientras no cambien externamente las propensiones.',
 136:'Expresión estacionaria del promotor de dos estados bajo las hipótesis del capítulo; no describe cualquier forma de ráfaga.',
 141:'Aproximación continua de conteos, no SSA exacto. Requiere cuidado cerca de cero y de poblaciones pequeñas.',
 147:'Supone errores normales independientes con σᵢ conocidas. Si dependen de θ, el término logarítmico también interviene en el ajuste.',
 154:'Expresión para varianzas conocidas y sin dependencia paramétrica; un modelo de error más general cambia la información.',
 166:'Requiere S>0 y una estimación fiable de su derivada; derivar datos ruidosos puede amplificar el error.',
 175:'La desigualdad estricta exige margen positivo; no garantiza robustez ante ruido no incluido.',
 181:'Inversión para λ constante positiva y 0≤p<1; p=1 requiere un tiempo infinito en este modelo.',
 193:'La temperatura es absoluta y la energía debe usar la misma unidad que k_B T; este peso no es una tasa de transición.',
 198:'s es selección, no producción; f está entre cero y uno bajo el modelo declarado.',
 202:'Factor de diseño para grupos de igual tamaño y correlación común; no se aplica automáticamente a estructuras temporales o jerárquicas arbitrarias.'
}

def formula_key(tex):
    tex=re.sub(r'\s+',' ',tex.strip());tex=re.sub(r'\\frac(\d)(\d)',r'\\frac{\1}{\2}',tex)
    return hashlib.sha256(tex.encode()).hexdigest()[:18]

def preparar(chapters):
    formulas={};symbols={};n=0
    for ch in chapters:
        for m in re.finditer(r'\$\$(.*?)\$\$',ch['body'],re.S):
            n+=1;cid,keys=USE[n];assert cid==ch['id'],(n,cid,ch['id'])
            entries=[]
            if r'\sqrt' in m[1]:keys=keys+['root']
            if '|' in m[1] and n in [19,20,85]:keys=keys+['abs']
            if n==85:keys=keys+['imag','atan']
            if 'dt' in m[1] and 't' not in keys:keys=keys+['t']
            for key in keys:
                d=dict((COMMON|BANK[cid])[key]);sid='sym-'+cid+'-'+key
                entry=symbols.setdefault(sid,dict(id=sid,kind='símbolo',chapter=cid,chapter_title=ch['title'],refs=ch.get('refs',[]),equations=[],**d))
                entry['equations'].append(n);entries.append(dict(id=sid,**d))
            key=formula_key(m[1]);formulas[key]=dict(number=n,chapter=cid,anchor='eq-'+cid+'-'+key,symbols=entries,note=NOTES.get(n,''),refs=ch.get('refs',[]))
    assert n==len(USE)==202,(n,len(USE))
    return formulas,list(symbols.values())

def clave_html(key,formulas):
    f=formulas[key]
    entries=''.join('<p><a class="symbol-lookup" data-glossary="'+d['id']+'" href="c36.xhtml#'+d['id']+'"><strong>'+html.escape(d['symbol'])+'</strong></a>: '+html.escape(d['meaning'])+' <span class="symbol-unit">Unidad: '+html.escape(d['units'])+'. Papel: '+html.escape(d['role'])+'.</span></p>' for d in f['symbols'])
    note='<p class="symbol-note"><strong>Condición de lectura.</strong> '+html.escape(f['note'])+'</p>' if f['note'] else ''
    return '<details class="symbol-key" open><summary>Qué significa cada símbolo · ecuación ('+str(f['number'])+')</summary><p class="notation-convention">En las unidades: C = concentración; T = tiempo; 1 = adimensional.</p>'+entries+note+'</details>'
