# Changelog

Todos los cambios relevantes de GitHub Portfolio Assistant se documentan en este archivo.

## [1.0.0] - 2026-08-14

### Agregado

- Arquitectura modular de la aplicación.
- Menú interactivo en consola.
- Gestión de proyectos mediante rutas locales.
- Ejecución centralizada de comandos externos.
- Integración con Git.
- Integración con GitHub CLI.
- Comprobación de autenticación con GitHub.
- Detección y validación del remoto `origin`.
- Creación de repositorios en GitHub.
- Consulta del estado Git.
- Preparación automática mediante `git add`.
- Publicación mediante `git push`.
- Análisis automático de proyectos.
- Detección de tecnologías.
- Detección de Python y Jupyter Notebook.
- Detección de NumPy, Pandas, OpenCV y Ultralytics/YOLO.
- Generación automática de README.
- Integración de generación de README en el flujo de publicación.
- Revisión preventiva de seguridad.
- Detección de archivos sensibles.
- Detección de videos, modelos de IA, datos y archivos grandes.
- Comprobación de protección mediante `.gitignore`.
- Generación automática de sugerencias de commit.
- Configuración persistente mediante `settings.json`.
- Configuración de autor por defecto.
- Configuración de visibilidad predeterminada.
- Configuración de prefijo de commit.
- Confirmación configurable antes de realizar push.
- Resumen previo a publicación.
- Pruebas funcionales de los principales componentes.
- Prueba integral del flujo completo de publicación.

### Mejorado

- Flujo de publicación de proyectos existentes.
- Manejo de repositorios que ya tienen `origin`.
- Manejo de proyectos sin README.
- Prevención de commits vacíos.
- Validaciones antes de publicar.
- Organización de mensajes mostrados en consola.
- Documentación principal del proyecto.

### Seguridad

- Advertencia antes de publicar archivos potencialmente sensibles.
- Validación de archivos protegidos mediante `.gitignore`.
- Posibilidad de cancelar la publicación antes de preparar o enviar cambios.

### Eliminado

- `src/utils.py`, módulo vacío que no era utilizado por la versión 1.0.0.

## [0.1.0]

### Agregado

- Estructura inicial del proyecto.
- Primer menú de consola.
- Configuración inicial.
- Base para integración con Git y GitHub.