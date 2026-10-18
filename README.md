# Modelado matemático de circuitos génicos

Atlas de estudio en español, desde las matemáticas iniciales hasta modelos de circuitos, inferencia y biología sintética de plantas. Edición 1.1; corte de la selección bibliográfica: **18 de octubre de 2026**.

- 38 capítulos, unas 35.000 palabras de lecciones, además de las lecturas visuales y 210 ecuaciones.
- Libro PDF de 191 páginas y EPUB refluible.
- 38 figuras originales: 26 gráficos y esquemas (PNG/SVG) y 12 láminas moleculares planas (PNG de alta resolución).
- 10 cuadernos Jupyter y sus scripts Python equivalentes.
- 72 entradas bibliográficas con enlaces, DOI cuando existe y notas de verificación.
- App adaptable a móvil: búsqueda conjunta de lecciones, figuras y fuentes, notas, marcadores, progreso, simulador y descarga para lectura sin conexión.

## Abrir el material

[App y GitHub Pages](https://camilo31-svg.github.io/modelado-circuitos-genicos/)

[Libro PDF](docs/downloads/modelado-circuitos-genicos.pdf) · [Libro EPUB](docs/downloads/modelado-circuitos-genicos.epub)

La app y los libros tienen las mismas lecciones. Las nuevas láminas M01–M12 incluyen leyenda, lectura por paneles, límites del esquema y relación con las ecuaciones. En el atlas de figuras puedes filtrar por «Láminas moleculares» y abrir la versión de alta resolución. Empieza por el capítulo 00 y usa la ruta del capítulo 37. Los temas avanzados son una puerta hacia cursos de posgrado, lectura de artículos y trabajo de investigación con revisión especializada.

## Ejecutar las prácticas

Instala Python 3.12 o posterior desde su distribución oficial. Desde esta carpeta, crea un entorno e instala las dependencias. En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r python\requirements.txt
.venv\Scripts\python.exe python\cuadernos\01_python.py
.venv\Scripts\python.exe -m unittest discover -s python -p test_modelos.py
.venv\Scripts\python.exe -m jupyterlab python\cuadernos
```

En Linux o macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r python/requirements.txt
.venv/bin/python python/cuadernos/01_python.py
.venv/bin/python -m unittest discover -s python -p test_modelos.py
.venv/bin/python -m jupyterlab python/cuadernos
```

Los cuadernos se ejecutan desde `python/cuadernos/` o `python/`. Los scripts resuelven el módulo con su propia ubicación y también pueden ejecutarse desde la raíz del repositorio. Conserva la carpeta `python` completa: un cuaderno aislado necesita `circuitos.py`.

Se incluyen instrucciones y resultados esperados en cada práctica. Los cuadernos se entregan sin salidas precalculadas para que puedas producirlas; los diez scripts se han ejecutado durante la validación. `VERIFICACION.json` registra sus resultados y límites. `python/entorno-validado.txt` identifica las versiones de la ejecución original; `requirements.txt` expresa intervalos compatibles para instalaciones nuevas.

## App local y sin conexión

```bash
python -m http.server 8765 --directory docs
```

Abre `http://localhost:8765`. Evita abrir `index.html` mediante `file://`: la carga del contenido y el service worker necesitan un servidor. En la app publicada, pulsa **Descargar para leer sin conexión** y espera el mensaje de finalización. Se guardan lecciones, ecuaciones, figuras PNG, SVG y prácticas; PDF y EPUB se descargan por separado. Si el navegador elimina la caché por falta de espacio, vuelve a descargar.

Las notas y el avance pertenecen a cada navegador, sin cuenta ni sincronización. En **Mis notas**, exporta una copia JSON e impórtala en otro dispositivo. Las ilustraciones planas fueron generadas con la herramienta integrada de imágenes y revisadas para comprobar relaciones y etiquetas. Son esquemas didácticos, sin estructuras atomísticas ni tamaños a escala; no contienen activos de BioRender. La app no incorpora analítica ni carga bibliotecas o imágenes desde CDN. Los enlaces a artículos abren sus sitios de origen.

## Reconstruir y ampliar

Los datos originales están en `book/chapters.json` y `book/references.json`. `book/visuals.json` conserva las doce láminas, sus lecturas por paneles y las secciones insertadas en el texto; `book/visual_references.json` añade sus fuentes. `book/image-generation.json` documenta especificaciones, procedencia, prompts conservados y hashes de las imágenes. Los Markdown de consulta están en `book/source`. Para cambiar contenido, edita el JSON original y vuelve a construir; no edites solo el HTML de `docs/chapters.json`.

```bash
python -m pip install -r tools/requirements-build.txt
python tools/crear_figuras.py
python tools/construir_libro.py
python tools/empaquetar.py
```

El PDF se construye con ReportLab y fuentes incrustadas; si no hay fuentes de Windows usa DejaVu. Las figuras se calculan con NumPy/SciPy y se dibujan con Matplotlib. Las ecuaciones se renderizan localmente. `tools/empaquetar.py` vuelve a generar los paquetes, copia las prácticas para la app y actualiza la versión de caché según los archivos publicados. No hay compilación JavaScript ni dependencias web.

Para GitHub Pages, el origen es **main → /docs**. Tras reconstruir, revisa el PDF renderizado, el EPUB y la app, confirma los cambios y haz push. La publicación se actualiza con ese directorio.

## Alcance, evidencia y límites

Los valores, series y figuras son **ejemplos docentes originales** salvo que se indique expresamente una observación publicada. No constituyen ajustes de los artículos citados. Cada caso distingue observación, explicación y límites de transferencia entre organismos. Las notas bibliográficas dicen cuándo se pudo consultar el texto completo o solo un resumen/registro.

La bibliografía es una selección razonada y actualizada a la fecha indicada, no una revisión sistemática exhaustiva. La formación cubre fundamentos y múltiples rutas avanzadas; no contiene todo el conocimiento existente ni garantiza un nivel experto por sí sola. La revisión especializada independiente completa está pendiente. Trabajar con datos nuevos, discutir supuestos y recibir crítica son parte de la ruta de aprendizaje.

El material se generó con Codex y se revisó mediante comprobaciones bibliográficas, pruebas numéricas y revisión de formato. No se atribuye autoría o revisión a investigadores que no han participado. El aspecto de las figuras usa convenciones científicas; no hay afiliación con Nature.

## Organización

| Carpeta | Contenido |
|---|---|
| `book/` | Fuente editorial, Markdown y registro de ecuaciones |
| `docs/` | App publicable, recursos y descargas |
| `python/` | Modelos, pruebas y diez prácticas |
| `tools/` | Generadores reproducibles de figuras y formatos |

Contenido y figuras originales: CC BY 4.0. Código: MIT. Los artículos enlazados conservan sus propias licencias; aquí no se redistribuyen sus textos ni sus figuras.
