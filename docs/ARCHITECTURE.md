# Arquitectura de GitHub Portfolio Assistant

## Objetivo

GitHub Portfolio Assistant es una aplicación de consola desarrollada en Python para automatizar tareas relacionadas con el análisis, documentación, preparación y publicación de proyectos en GitHub.

La versión 1.0.0 utiliza una arquitectura modular basada en separación de responsabilidades.

## Estructura general

```text
github-portfolio-assistant/
|
|-- app.py
|-- README.md
|-- requirements.txt
|-- .gitignore
|
|-- config/
|   `-- settings.json
|
|-- docs/
|   |-- ARCHITECTURE.md
|   |-- CHANGELOG.md
|   `-- ROADMAP.md
|
|-- src/
|   |-- command_runner.py
|   |-- commit_generator.py
|   |-- config.py
|   |-- github_manager.py
|   |-- git_manager.py
|   |-- menu.py
|   |-- project_analyzer.py
|   |-- project_manager.py
|   |-- readme_generator.py
|   |-- security_checker.py
|   `-- __init__.py
|
`-- tests/
```

## Componentes principales

### `app.py`

Punto de entrada de la aplicación.

Su responsabilidad principal es iniciar el menú del asistente.

### `menu.py`

Coordina la interacción con el usuario y orquesta los diferentes módulos.

Gestiona el flujo principal de publicación:

```text
Proyecto
   |
   v
Análisis
   |
   v
README
   |
   v
Git / GitHub
   |
   v
Seguridad
   |
   v
Preparación de cambios
   |
   v
Commit
   |
   v
Confirmación
   |
   v
Push
```

### `project_manager.py`

Carga una ruta local y representa el proyecto que será gestionado.

También permite determinar si la ruta corresponde a un repositorio Git.

### `project_analyzer.py`

Analiza la estructura del proyecto.

Entre sus responsabilidades se encuentran:

- detectar archivos y carpetas;
- comprobar archivos importantes;
- detectar tecnologías;
- generar información utilizada por otros módulos.

### `command_runner.py`

Centraliza la ejecución de comandos externos.

Permite ejecutar Git, GitHub CLI y otros comandos desde Python manteniendo una respuesta estructurada con salida, errores y código de retorno.

### `git_manager.py`

Encapsula las operaciones relacionadas con Git, entre ellas:

- consultar estado;
- preparar cambios;
- crear commits;
- consultar `origin`;
- realizar `push`.

### `github_manager.py`

Gestiona la integración con GitHub mediante GitHub CLI.

Entre sus responsabilidades se encuentran:

- comprobar autenticación;
- verificar repositorios;
- crear repositorios;
- validar parámetros relacionados con GitHub.

### `security_checker.py`

Realiza una revisión preventiva antes de publicar.

Detecta archivos potencialmente problemáticos y comprueba su relación con `.gitignore`.

### `readme_generator.py`

Genera documentación inicial `README.md` utilizando los resultados proporcionados por `ProjectAnalyzer`.

### `commit_generator.py`

Analiza los cambios del repositorio y propone mensajes de commit según el tipo de modificación detectada.

### `config.py`

Gestiona la configuración persistente de la aplicación mediante `config/settings.json`.

## Flujo entre componentes

```text
Menu
 |
 +--> ProjectManager
 |
 +--> ProjectAnalyzer
 |
 +--> ReadmeGenerator
 |
 +--> SecurityChecker
 |
 +--> GitManager ------> CommandRunner
 |
 +--> GitHubManager ---> CommandRunner
 |
 +--> CommitGenerator
 |
 `--> AppConfig
```

`Menu` funciona como coordinador principal, mientras que los demás módulos mantienen responsabilidades específicas.

## Configuración

La configuración persistente se almacena en:

```text
config/settings.json
```

Permite administrar valores como autor, visibilidad predeterminada, prefijo de commit y confirmación previa al push.

## Pruebas

La carpeta `tests/` contiene pruebas funcionales de los principales componentes.

Las pruebas permiten validar de manera independiente las operaciones antes de integrarlas en el flujo principal.

## Principios de diseño

La arquitectura sigue principalmente estos principios:

- separación de responsabilidades;
- modularidad;
- reutilización;
- bajo acoplamiento entre operaciones;
- validación antes de ejecutar acciones críticas;
- control del usuario antes de publicar;
- documentación del proyecto;
- posibilidad de evolución futura.