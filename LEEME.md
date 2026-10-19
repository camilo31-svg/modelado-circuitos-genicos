# Modelado matemático de circuitos génicos

**Edición 2.1 — consulta bibliográfica hasta el 19 de octubre de 2026.**

Recorrido en español que da por conocidas derivadas e integrales y empieza directamente en ecuaciones diferenciales. Se han retirado las lecciones previas de aritmética, funciones, exponenciales y cálculo elemental. El foco es derivar modelos, entender sus supuestos, analizar dinámica, programar, inferir parámetros y evaluar evidencia, con ejemplos de bacterias, levaduras y plantas. Cada capítulo añade desarrollo guiado de símbolos, unidades, fórmulas y pasos; las prácticas incluyen lectura del código.

- 36 capítulos y unas 87,432 palabras de lecciones, además de leyendas y lecturas por paneles.
- PDF de 446 páginas y EPUB refluible con las mismas lecciones.
- 69 figuras: 12 láminas moleculares y 57 gráficos y esquemas. Las 20 nuevas de esta revisión conectan reacción, pasos matemáticos y curvas.
- 25 cuadernos Jupyter y scripts equivalentes; modelos básicos y avanzados.
- 94 referencias utilizadas, notas de consulta, BibTeX y mapa de fuentes por sección.
- App móvil con categorías, índice interno de capítulo, fuentes, búsqueda de texto y figuras, notas, progreso, simulador y lectura sin conexión.

[Abrir la app](https://camilo31-svg.github.io/modelado-circuitos-genicos/) · [PDF](docs/downloads/modelado-circuitos-genicos.pdf) · [EPUB](docs/downloads/modelado-circuitos-genicos.epub)

## Recorrido

1. EDO: soluciones lineales y por tramos, balances, estequiometría, conservación, escalas, reducción, Python y cinética de regulación.
2. Dinámica no lineal: Jacobianos, cuencas, bifurcaciones, Goodwin, represilador, doble retroalimentación, feedforward, retrasos, control integral, recursos, osciladores acoplados y reacción–difusión.
3. Ruido e inferencia: ecuación maestra, Gillespie, ráfagas y momentos, observación, sensibilidad, verosimilitud, Bayes, perfiles e identificabilidad.
4. Casos biológicos: represilador bacteriano completo y dos casos de levadura, además de plantas: contexto y variación, sensores de auxina, lógica espacial, memoria, reloj de Arabidopsis e interruptor vegetal de 2025.
5. Investigación: cascadas y modificación multisito, metabolismo y otros niveles, inferencia de redes, software reproducible y proyectos con soluciones.

El archivo aportado de Ingalls se identifica como versión de autor fechada el 23-12-2015, con 406 páginas PDF, diferenciada de la edición impresa de 2013. Es la referencia A01. No se incluye ese PDF en el repositorio. Las explicaciones, números, ejercicios y figuras del atlas son propios; cuando se explica un artículo se distingue resultado publicado y desarrollo docente. Las notas bibliográficas indican si se consultó resumen, texto, metadatos o documentación. La selección no se presenta como una revisión sistemática exhaustiva ni sustituye revisión experta independiente.

## Ejecutar las prácticas

Con Python 3.12 o posterior, desde esta carpeta en PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r python\requirements.txt
.venv\Scripts\python.exe python\cuadernos\11_union.py
.venv\Scripts\python.exe -m unittest discover -s python -p "test*.py"
.venv\Scripts\python.exe -m jupyterlab python\cuadernos
```

En Linux/macOS, usa `.venv/bin/python` y separadores `/`. Los cuadernos se entregan sin salidas precalculadas para que el lector las produzca; los scripts se ejecutan en la validación. Los parámetros son docentes y no están calibrados a los artículos. El móvil permite leer y usar el simulador; para ejecutar Python utiliza un entorno Jupyter compatible.

## Reconstruir libros y figuras

Instala además `tools/requirements-build.txt`. Los datos canónicos están en `book/chapters.json`, `book/references.json`, `book/visuals.json` y `book/edition.json`; `book/source/` expone los capítulos en Markdown. El constructor utiliza los JSON canónicos.

```text
python tools/crear_cuadernos.py
python tools/crear_practicas_avanzadas.py
python tools/crear_casos_detallados.py
python tools/ampliar_practicas.py
python tools/crear_figuras.py
python tools/crear_figuras_avanzadas.py
python tools/crear_figuras_casos.py
python tools/crear_figuras_pasos.py
python tools/construir_libro.py
python tools/validar_material.py
python tools/empaquetar.py
```

Para revisión visual se usa Poppler (`pdftoppm`), disponible por separado. `VERIFICACION.json` registra resultados y alcance; `python/entorno-validado.txt` registra las versiones usadas. Las pruebas incluyen soluciones conocidas, conservaciones, identidades de control, umbrales y momentos. No equivalen a validación experimental de todos los modelos.

## Fuentes y procedencia

- `book/bibliografia.bib`: bibliografía académica exportable.
- `book/source-map.json`: referencias de cada apartado con contenido.
- `book/research-log.json`: temas consultados, comprobación de DOI y alcance.
- `book/image-generation.json`: procedencia y especificaciones de las doce láminas generadas con la herramienta integrada. Son esquemas planos, no estructuras atomísticas; no reutilizan activos de BioRender.
- `tools/crear_figuras_avanzadas.py`: genera los doce gráficos avanzados desde ecuaciones y parámetros explícitos.

## App, notas y uso sin conexión

Abre `docs/` mediante un servidor HTTP o usa GitHub Pages. Descarga previamente los recursos desde el botón de la app para leer sin conexión; los libros se descargan por separado. No hay analítica ni sincronización automática de notas. Estas se guardan en el navegador y pueden exportarse. Las notas de lecciones retiradas siguen accesibles en el archivo de notas de la edición anterior, sin volver a incluir sus lecciones.

GitHub Pages publica la carpeta `/docs` de `main`. Se conservan los identificadores de lecciones pertinentes y alias de las que se integraron en otro capítulo; la numeración visible sigue el nuevo orden.

## Desarrollo de la edición 2.1

Los dos casos completos definen cada estado y tasa, derivan normalización y estabilidad y explican los índices del código. Las 25 prácticas tienen guías compartidas entre el libro, los cuadernos y la app, almacenadas en `book/practice-guides.json`. `python/circuitos_casos.py` añade transformaciones de unidades y soluciones comprobables; `python/test_casos.py` verifica diez consecuencias analíticas y de implementación. Las constantes de los ejemplos se identifican como docentes. No se redistribuye el libro aportado ni figuras de artículos.

## Referencias dentro del desarrollo

Las ecuaciones llevan número y una llamada en la prosa. Cada figura tiene una llamada y un destino junto al paso que acompaña. La app conserva esos saltos sin abandonar la lección; PDF y EPUB incluyen enlaces internos. `tools/figuras_en_texto.py` aplica la misma colocación en los tres formatos. Las secuencias visuales nuevas de `tools/crear_figuras_pasos.py` reúnen mecanismo, fórmula y curva; el campo `after_heading` permite asociarlas a un apartado concreto.

## Lecturas visuales de las curvas

Las 56 figuras con curvas incluyen 123 lecturas gráficas complementarias para 235 series: inicio, punto intermedio y final, con los mismos colores y valores que el gráfico. Los iconos muestran abundancia relativa; las magnitudes abstractas usan barras. No representan conteos moleculares. `tools/lectura_curvas.py` extrae las coordenadas dibujadas y genera los PNG/SVG, con indicación de ejes temporales, constantes, entradas y cambios deliberados. Los valores redondeados no convierten el último punto en un equilibrio. Las lecturas gráficas pueden ampliarse desde la app.
