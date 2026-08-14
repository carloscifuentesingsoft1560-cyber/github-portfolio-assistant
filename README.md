# GitHub Portfolio Assistant

GitHub Portfolio Assistant es una aplicación de consola desarrollada en Python para automatizar tareas frecuentes relacionadas con la organización, análisis, documentación y publicación de proyectos en GitHub.

El proyecto permite trabajar con repositorios locales desde un flujo guiado, integrando operaciones de Git, GitHub CLI, análisis del proyecto, generación de documentación, revisión preventiva de seguridad y creación de mensajes de commit.

## Estado del proyecto

**Versión:** `1.0.0`  
**Estado:** versión estable inicial.

## Funcionalidades

### Publicación de proyectos

El asistente permite gestionar la publicación de un proyecto mediante un flujo guiado que incluye:

- selección de un proyecto mediante su ruta local;
- análisis automático del proyecto;
- comprobación de autenticación con GitHub CLI;
- consulta del estado de Git;
- detección y validación del remoto `origin`;
- creación de repositorios en GitHub cuando sea necesario;
- preparación automática de cambios mediante `git add`;
- generación de mensajes de commit;
- creación del commit;
- confirmación previa;
- publicación mediante `git push`.

### Análisis automático

GitHub Portfolio Assistant puede inspeccionar la estructura de un proyecto y obtener información como:

- nombre y ruta;
- existencia de repositorio Git;
- presencia de `README.md`;
- presencia de `.gitignore`;
- presencia de `requirements.txt`;
- cantidad de archivos y carpetas;
- tecnologías detectadas.

El analizador puede reconocer tecnologías a partir de extensiones, archivos y contenido del proyecto, incluyendo Python, Jupyter Notebook, NumPy, Pandas, OpenCV y Ultralytics/YOLO, entre otras reglas implementadas.

### Generación de README

El programa puede generar automáticamente un `README.md` inicial utilizando la información obtenida durante el análisis del proyecto.

Si ya existe un README, el usuario conserva el control sobre su reemplazo.

Durante el flujo de publicación, si el proyecto no contiene README, el asistente puede ofrecer su generación antes de continuar.

### Revisión de seguridad

Antes de publicar, el sistema realiza una revisión preventiva para detectar archivos que podrían requerir atención, entre ellos:

- archivos `.env`;
- credenciales;
- certificados y claves;
- videos;
- modelos o pesos de inteligencia artificial;
- archivos de datos;
- archivos de gran tamaño.

También comprueba si los archivos detectados están protegidos mediante `.gitignore`.

Si encuentra un archivo potencialmente problemático sin protección, advierte al usuario antes de continuar.

> La revisión automática es una medida preventiva y no sustituye una inspección manual del contenido que será publicado.

### Generación de commits

El asistente analiza los cambios del repositorio y propone mensajes de commit organizados según el tipo de modificación detectada.

Por ejemplo:

```text
docs: actualiza documentacion del proyecto
feat: actualiza funcionalidades del proyecto
```

El usuario puede aceptar la sugerencia o escribir su propio mensaje antes de crear el commit.

### Configuración

La aplicación dispone de configuración persistente para definir valores como:

- autor por defecto;
- visibilidad predeterminada del repositorio;
- prefijo de commit;
- confirmación antes de realizar `push`.

La configuración se almacena en:

```text
config/settings.json
```

## Flujo principal

El proceso automatizado de publicación sigue, de manera general, este flujo:

```text
Proyecto local
      |
      v
Análisis del proyecto
      |
      v
Comprobación de README
      |
      v
Validación de GitHub y Git
      |
      v
Revisión de origin
      |
      v
Revisión de seguridad
      |
      v
Preparación de cambios
      |
      v
Generación de commit
      |
      v
Resumen previo
      |
      v
Confirmación del usuario
      |
      v
Push a GitHub
```

## Requisitos

- Python 3.10 o superior
- Git
- GitHub CLI
- Cuenta de GitHub
- Sesión iniciada mediante GitHub CLI

Puedes comprobar las herramientas instaladas con:

```bash
python --version
git --version
gh --version
```

Para autenticar GitHub CLI:

```bash
gh auth login
```

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/carloscifuentesingsoft1560-cyber/github-portfolio-assistant.git
```

Entra en la carpeta:

```bash
cd github-portfolio-assistant
```

El núcleo de esta versión utiliza la biblioteca estándar de Python, por lo que no requiere instalar paquetes Python externos para su funcionamiento actual.

## Ejecución

Ejecuta:

```bash
python app.py
```

El menú principal permite acceder a:

```text
1. Publicar proyecto existente
2. Consultar estado Git
3. Agregar cambios (git add .)
4. Analizar proyecto
5. Generar README
6. Revisar seguridad
7. Configuración
8. Salir
```

## Estructura

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
    |-- test_command_runner.py
    |-- test_commit_generator.py
    |-- test_create_repository.py
    |-- test_github_manager.py
    |-- test_git_manager.py
    |-- test_project_analyzer.py
    |-- test_project_manager.py
    |-- test_readme_generator.py
    `-- test_security_checker.py
```

## Arquitectura

El proyecto utiliza una arquitectura modular en la que cada componente tiene una responsabilidad específica.

Entre sus componentes principales se encuentran:

- `Menu`: coordina la interacción con el usuario.
- `ProjectManager`: carga y valida proyectos locales.
- `ProjectAnalyzer`: analiza estructura y tecnologías.
- `GitManager`: gestiona operaciones Git.
- `GitHubManager`: integra las operaciones relacionadas con GitHub CLI.
- `SecurityChecker`: realiza comprobaciones preventivas antes de publicar.
- `ReadmeGenerator`: genera documentación inicial.
- `CommitGenerator`: propone mensajes de commit.
- `AppConfig`: administra la configuración persistente.
- `CommandRunner`: centraliza la ejecución de comandos externos.

## Pruebas

El proyecto incluye pruebas funcionales para sus componentes principales.

Entre las validaciones realizadas para la versión `1.0.0` se encuentran:

- compilación de los módulos Python;
- ejecución de comandos;
- carga de proyectos;
- operaciones Git;
- integración con GitHub CLI;
- análisis de proyectos;
- generación de README;
- revisión de seguridad;
- generación de commits;
- flujo integral de publicación en un repositorio de prueba.

## Seguridad

Nunca deben publicarse deliberadamente credenciales, tokens, claves privadas o información sensible.

GitHub Portfolio Assistant incorpora comprobaciones preventivas, pero la decisión final sobre qué archivos publicar continúa siendo responsabilidad del usuario.

## Documentación

La documentación complementaria se encuentra en:

- `docs/ARCHITECTURE.md`
- `docs/ROADMAP.md`
- `docs/CHANGELOG.md`

## Próximas mejoras

La versión `1.0.0` establece la base funcional del proyecto. Posibles evoluciones futuras incluyen:

- interfaz gráfica;
- ampliación de reglas de análisis;
- pruebas automatizadas con un framework dedicado;
- integración opcional con herramientas de inteligencia artificial;
- generación de documentación más avanzada;
- integración con un portafolio web.

## Autor

**Carlos Eduardo Cifuentes Sanabria**

Proyecto desarrollado como parte de un proceso de fortalecimiento de habilidades en Ingeniería de Software, automatización, Python, Git y GitHub.