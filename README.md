# GitHub Portfolio Assistant

Aplicación en Python para automatizar la organización, documentación y publicación de proyectos personales en GitHub.

El objetivo del proyecto es reducir el tiempo dedicado a tareas repetitivas como crear repositorios, revisar archivos, generar documentación, preparar commits y publicar cambios.

## Estado del proyecto

En desarrollo.

Versión actual: `0.1`

## Funcionalidades actuales

- Menú principal en consola.
- Arquitectura modular.
- Integración inicial con Git y GitHub CLI.
- Validación básica de archivos sensibles.
- Publicación de cambios mediante commits y push.
- Documentación técnica del proyecto.

## Funcionalidades planificadas

- Crear repositorios automáticamente.
- Analizar tecnologías utilizadas en cada proyecto.
- Generar archivos `README.md`.
- Crear mensajes de commit organizados.
- Detectar archivos pesados y credenciales.
- Publicar proyectos nuevos y existentes.
- Generar una interfaz gráfica.
- Integrar herramientas de inteligencia artificial.
- Actualizar automáticamente un portafolio web.

## Tecnologías

- Python 3.10
- Git
- GitHub
- GitHub CLI
- Visual Studio Code

## Estructura del proyecto

```text
github-portfolio-assistant/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── menu.py
│   ├── git_manager.py
│   ├── github_manager.py
│   ├── project_analyzer.py
│   ├── security_checker.py
│   ├── readme_generator.py
│   ├── commit_generator.py
│   ├── config.py
│   └── utils.py
│
├── config/
├── templates/
├── assets/
├── docs/
└── tests/
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

Verifica Python:

```bash
python --version
```

## Ejecución

Ejecuta:

```bash
python app.py
```

## Uso actual

Al iniciar la aplicación aparece el menú:

```text
1. Crear proyecto
2. Publicar proyecto existente
3. Generar README
4. Analizar proyecto
5. Revisar seguridad
6. Configuración
7. Salir
```

Por ahora, las opciones están preparadas para implementarse progresivamente durante los siguientes sprints.

## Documentación

La documentación técnica está disponible en:

- `docs/ARCHITECTURE.md`
- `docs/ROADMAP.md`
- `docs/CHANGELOG.md`

## Roadmap resumido

- `v0.1`: arquitectura y menú principal.
- `v0.2`: gestión de operaciones Git.
- `v0.3`: integración con GitHub.
- `v0.4`: generación automática de README.
- `v0.5`: análisis de proyectos.
- `v0.6`: revisión de seguridad.
- `v0.8`: interfaz gráfica.
- `v1.0`: primera versión estable.

## Autor

**Carlos Eduardo Cifuentes Sanabria**

Estudiante de Ingeniería de Software con interés en automatización, Machine Learning, inteligencia artificial y visión por computador.