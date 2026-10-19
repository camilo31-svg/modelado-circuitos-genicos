"""Índice de consulta compartido por libro y app; definiciones con procedencia."""
import re,html,hashlib,unicodedata
from bs4 import BeautifulSoup

EXTRA='''
## Cómo consultar una letra sin perder el contexto

Cada una de las 202 ecuaciones numeradas lleva una clave propia: significado, unidad y papel de sus símbolos. En las claves, **C** abrevia la unidad de concentración elegida y **T** la unidad temporal elegida; no son nuevas variables del circuito. Cuando se usan nM y horas, C/T significa nM/h. Una tabla puede usar T para traza o temperatura: su entrada lo dice expresamente. El símbolo **1** en la columna de unidades significa adimensional. Los conteos se conservan identificados como conteos aunque su dimensión formal sea uno. [A01] [A28]

En la app puedes abrir una definición desde la propia ecuación, consultar «Glosario y símbolos» o filtrar por lección. Busca también por nombres: «delta», «pérdida», «Hill» o «Jacobiano». En PDF y EPUB el índice siguiente reúne las definiciones por contexto y permite volver a las ecuaciones. Las entradas de una letra en capítulos diferentes se conservan separadas: elegir solo por parecido tipográfico es una fuente de errores. [A01] [A27]

## Magnitud, unidad y dimensión: tres preguntas diferentes

**Magnitud.** Propiedad que el modelo cuantifica, por ejemplo concentración libre de represor. **Unidad.** Referencia con la que expresas su valor, por ejemplo nM. **Dimensión.** Tipo de dependencia de cantidades básicas; concentración es cantidad de sustancia por volumen. Cambiar de nM a µM modifica el número y conserva la magnitud. El símbolo de una magnitud no determina por sí solo su unidad. [A28]

En una asociación A+B→C con concentraciones a y b, la tasa v=k·a·b tiene unidad de concentración/tiempo. Por tanto k tiene unidad 1/(concentración·tiempo): k no es una «velocidad» con unidad universal. En una pérdida v=δ·x, δ tiene unidad 1/tiempo. Aquí a, b y x son concentraciones; v una tasa; k y δ parámetros. Antes de comparar parámetros de dos artículos convierte unidades y comprueba si la ley usa cantidades, concentraciones o conteos. [A01] [I13]

**Prueba de consistencia.** Para x′=α−δx: x es concentración, t tiempo, α producción por volumen y tiempo, δ pérdida por molécula y tiempo. x′ y los dos términos de la derecha deben compartir unidad C/T. En exp(−δt), δt tiene unidad uno. Para sumar 1+(x/K)ⁿ, K debe compartir unidad con x y n no lleva unidad. Estas comprobaciones detectan errores; no prueban que el mecanismo describa la biología correcta. [A01] [A28]

## La ficha que debes escribir antes de simular

1. **Pregunta y alcance.** Escribe qué predicción quieres contrastar, en qué organismo, escala y condiciones. «Oscila» necesita intervalo, variable observada y criterio de persistencia. Una simulación docente y un ajuste experimental tienen evidencias distintas. [A01] [A15]
2. **Estados y fronteras.** Ordena las especies, compartimentos, cantidades o concentraciones y totales conservados. Declara qué queda fuera y qué procesos cruzan esa frontera. Si cambian volúmenes, decide si integras cantidad o concentración e incluye la conversión. [A01] [I13]
3. **Entradas, parámetros e inicio.** Separa lo prescrito desde fuera, lo que evoluciona y las constantes de una corrida. Una entrada escalón se documenta con instante y valores antes y después. Si modificas un parámetro deliberadamente, registra su ley por tramos; no describas después su cambio como una respuesta espontánea del estado. [A01] [I13]
4. **Leyes y reducciones.** Para cada término apunta reacción de origen, signo, factores, unidad y supuesto. Si eliminas un complejo rápido, conserva el modelo completo como comparación y especifica qué escala pequeña permite la reducción. [A01]
5. **Observación.** Define qué se mide, cómo se transforma el estado en señal, qué fondo y maduración intervienen y qué error se supone. Indica la unidad independiente de réplica: muchas imágenes de la misma planta no se vuelven plantas independientes. [I04] [A09] [P10]
6. **Cálculo reproducible.** Conserva versión del código, parámetros con unidades, iniciales, tolerancias, eventos y semillas cuando proceda. Registra éxito del integrador y repite con tolerancias más estrictas si hay una duda numérica concreta. La malla de dibujo no es el paso interno del solver. [R05] [A15] [A24]
7. **Contraste y límites.** Compara con solución analítica o invariantes disponibles, datos reservados y alternativas mecanísticas. Propaga incertidumbre; una curva visualmente buena no prueba identificabilidad ni un mecanismo único. [I06] [A18] [A09]

## Errores de lectura que conviene aprender a detectar

**Constante frente a flujo.** Si δ es fija, la retirada δE disminuye cuando baja la enzima E. La constante no ha cambiado: cambió uno de los factores de la tasa. En represión, una capacidad s_max fija y un regulador R variable pueden dar producción efectiva s(R) variable. Especifica siempre cuál de esas magnitudes sube o baja. [A01]

**Fin de la curva frente a equilibrio.** El último tiempo guardado es una elección numérica. Para defender un equilibrio, comprueba el campo de velocidades y escalas residuales; para un ciclo, persistencia, período y convergencia con el cálculo. Tres instantáneas ayudan a leer una curva, pero no sustituyen revisar su recorrido completo. [A01] [R05]

**Iconos frente a cantidades medidas.** En las figuras integradas, las proteínas dibujadas sugieren abundancia relativa: seis iconos no significan seis moléculas. Los indicadores verticales comparan el valor absoluto con el máximo absoluto de esa misma serie; el número impreso conserva signo y unidad. Dos indicadores llenos de series distintas no prueban igualdad de cantidades. Para una tasa o un error no se inventa una especie molecular. [A01] [A23]

**Parámetro efectivo frente a mecanismo.** Un exponente de Hill ajustado no demuestra cuántos sitios se unen; una sola tasa de pérdida puede reunir degradación y dilución; una ganancia de detector no es una eficiencia de traducción. La interpretación depende de las hipótesis y del experimento que la distingue de alternativas. [A01] [A18]

## Una forma de comprobar si ya puedes defender tu modelo

Trabaja en tres pasadas. Primero predice verbalmente qué debería ocurrir al duplicar una entrada o una constante y qué se mantendría. Después deriva esa predicción desde el balance y comprueba dimensiones, casos límite y escalas. Por último ejecuta el programa y explica cualquier desacuerdo entre cálculo, predicción y datos. Es una propuesta de estudio de este atlas que aplica los controles de modelado de [A01], [R05] y [I06]; no es una certificación de competencia.

Una defensa completa debería permitirte reconstruir una ecuación sin copiarla, relacionar cada término con una reacción, leer los ejes y el modelo de observación, explicar el algoritmo usado y reconocer qué parámetros no puedes determinar. Usa los proyectos del capítulo anterior para practicar esas decisiones con circuitos más largos y datos nuevos. [A01] [A15] [A18]
'''

def actualizar(chapters,symbols,formulas):
    c=next(c for c in chapters if c['id']=='c36')
    start='<!-- INDICE_CONTEXTUAL_INICIO -->';end='<!-- INDICE_CONTEXTUAL_FIN -->'
    c['body']=re.sub(re.escape(start)+'.*?'+re.escape(end),'',c['body'],flags=re.S).rstrip()
    lines=[start,EXTRA,'\n## Índice de símbolos por contexto y ecuación\n',
        'Las definiciones siguientes corresponden a la notación de este atlas. Cada bloque cita las fuentes de su lección; los números enlazan las ecuaciones donde se usa la entrada. [A01] [A27] [A28]\n']
    for ch in chapters:
        entries=[s for s in symbols if s['chapter']==ch['id']]
        if not entries:continue
        lines.extend(['\n### '+ch['number']+' · '+ch['title']+'\n',
            'Fuentes del contexto: '+', '.join('['+x+']' for x in ch['refs'])+'.\n',
            '| Símbolo y ecuaciones | Qué significa aquí | Unidad y papel |', '|---|---|---|'])
        for s in entries:
            bynum={f['number']:f for f in formulas.values()}
            nums=', '.join('[('+str(n)+')]('+bynum[n]['chapter']+'.xhtml#'+bynum[n]['anchor']+')' for n in s['equations'])
            cells=['['+s['symbol']+'](notacion:'+s['id']+') · '+nums,s['meaning'],s['units']+'; '+s['role']]
            lines.append('| '+' | '.join(x.replace('|','∣') for x in cells)+' |')
    lines.append(end);c['body']+='\n\n'+'\n'.join(lines)+'\n'
    c['refs']=list(dict.fromkeys(c.get('refs',[])+['A28','I13','A15','A18','I06','A23','A24','R05','P10','I04','A09']))

def entradas(chapters,symbols,formulas):
    out=[]
    for s in symbols:
        obj=dict(s);obj['name']=s['symbol'];obj['links']=[dict(number=f['number'],chapter=f['chapter'],anchor=f['anchor']) for f in formulas.values() if f['number'] in s['equations']]
        out.append(obj)
    ch=next(c for c in chapters if c['id']=='c36')
    text=ch['body'].split('## Índice de símbolos por contexto y ecuación')[0]
    for paragraph in re.split(r'\n\s*\n',text):
        refs=list(dict.fromkeys(re.findall(r'\[([A-Z]\d{2})\]',paragraph))) or ch['refs']
        for m in re.finditer(r'\*\*([^*]+)\*\*\s*(.*?)(?=\*\*|\Z)',paragraph,flags=re.S):
            name=m[1].strip().rstrip('.');body=m[2].strip()
            if len(body)<12:continue
            clean=BeautifulSoup(body,'html.parser').get_text(' ',strip=True)
            slug=''.join(x for x in unicodedata.normalize('NFD',name.lower()) if not unicodedata.combining(x))
            slug=re.sub(r'[^a-z0-9]+','-',slug).strip('-')[:55]
            out.append(dict(id='term-'+slug+'-'+hashlib.sha256(name.encode()).hexdigest()[:5],kind='concepto',name=name,meaning=clean,chapter='c36',chapter_title=ch['title'],refs=refs))
    return list({x['id']:x for x in out}.values())

def anclar(raw,symbols,formulas):
    soup=BeautifulSoup(raw,'html.parser')
    for a in soup.select('a[href^="notacion:"]'):
        sid=a['href'].split(':',1)[1];s=next(s for s in symbols if s['id']==sid)
        f=next(f for f in formulas.values() if f['number']==s['equations'][0])
        a['id']=sid;a['href']=f['chapter']+'.xhtml#'+f['anchor'];a['class']='symbol-index-link'
    return str(soup)
