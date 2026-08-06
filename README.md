# GitHub Portfolio Assistant

Herramienta en Python para revisar cambios, crear commits ordenados y publicar
proyectos existentes en GitHub desde Visual Studio Code.

## Requisitos

- Python 3.10 o superior
- Git
- GitHub CLI
- Una sesión iniciada con `gh auth login`

## Primera versión

Esta versión funciona con proyectos que:

1. Ya son repositorios Git.
2. Ya tienen un remoto llamado `origin`.
3. Ya están conectados con GitHub.

## Ejecución

```bash
python asistente_github.py
```

El programa solicitará la ruta completa de la carpeta que deseas publicar.

## Seguridad

Antes de publicar, realiza una revisión básica de:

- archivos `.env`;
- claves privadas;
- posibles tokens de GitHub;
- archivos mayores de 45 MB;
- videos, modelos y comprimidos.

Esta revisión ayuda, pero no reemplaza una inspección manual de los cambios.
