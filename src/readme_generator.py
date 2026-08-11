from pathlib import Path

from src.project_manager import Project
from src.project_analyzer import ProjectAnalyzer


class ReadmeGenerator:
    """
    Genera un README.md básico a partir del análisis del proyecto.
    """

    def __init__(self, project: Project):
        self.project = project
        self.analyzer = ProjectAnalyzer(project)

    def generate_content(self) -> str:
        """
        Genera el contenido del README sin escribirlo todavía.
        """

        data = self.analyzer.analyze()

        technologies = data["technologies"]

        if technologies:
            technologies_text = "\n".join(
                f"- {technology}"
                for technology in technologies
            )
        else:
            technologies_text = "- No detectadas"

        repository_status = (
            "Sí"
            if data["is_git_repository"]
            else "No"
        )

        gitignore_status = (
            "Sí"
            if data["has_gitignore"]
            else "No"
        )

        requirements_status = (
            "Sí"
            if data["has_requirements"]
            else "No"
        )

        content = f"""# {data["name"]}

Proyecto gestionado y documentado con GitHub Portfolio Assistant.

## Descripción

Este repositorio contiene el proyecto **{data["name"]}**.

La documentación inicial fue generada automáticamente a partir de la estructura detectada en el proyecto.

## Tecnologías detectadas

{technologies_text}

## Información del proyecto

- Archivos detectados: {data["file_count"]}
- Carpetas detectadas: {data["directory_count"]}
- Repositorio Git: {repository_status}
- .gitignore: {gitignore_status}
- requirements.txt: {requirements_status}

## Instalación

Clona el repositorio utilizando la URL correspondiente de GitHub.

Después entra en la carpeta del proyecto:

    cd {data["name"]}

Si existe requirements.txt, instala las dependencias:

    pip install -r requirements.txt

## Uso

Consulta los archivos principales del proyecto para conocer su forma de ejecución.

## Estado del proyecto

Proyecto en desarrollo.

## Autor

README generado inicialmente con GitHub Portfolio Assistant.
"""

        return content

    def write(
        self,
        overwrite: bool = False,
    ) -> Path:
        """
        Crea README.md en la raíz del proyecto.

        Si ya existe y overwrite=False,
        no reemplaza el archivo existente.
        """

        readme_path = (
            Path(self.project.path)
            / "README.md"
        )

        if readme_path.exists() and not overwrite:
            raise FileExistsError(
                "README.md ya existe en el proyecto."
            )

        content = self.generate_content()

        readme_path.write_text(
            content,
            encoding="utf-8",
        )

        return readme_path