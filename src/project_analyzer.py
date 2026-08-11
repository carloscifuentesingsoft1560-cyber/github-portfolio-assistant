from pathlib import Path

from src.project_manager import Project


class ProjectAnalyzer:
    """
    Analiza la estructura básica de un proyecto.
    """

    def __init__(self, project: Project):
        self.project = project

    def analyze(self) -> dict:
        """
        Devuelve un resumen general del proyecto.
        """

        project_path = Path(self.project.path)

        files = [
            item
            for item in project_path.rglob("*")
            if item.is_file()
            and ".git" not in item.parts
        ]

        directories = [
            item
            for item in project_path.rglob("*")
            if item.is_dir()
            and ".git" not in item.parts
        ]

        technologies = self._detect_technologies(files)

        return {
            "name": project_path.name,
            "path": str(project_path),
            "is_git_repository": self.project.is_git_repository,
            "has_readme": self._exists_case_insensitive(
                project_path,
                "README.md",
            ),
            "has_gitignore": (project_path / ".gitignore").exists(),
            "has_requirements": (
                project_path / "requirements.txt"
            ).exists(),
            "file_count": len(files),
            "directory_count": len(directories),
            "technologies": technologies,
        }

    @staticmethod
    def _exists_case_insensitive(
        project_path: Path,
        filename: str,
    ) -> bool:
        target = filename.lower()

        return any(
            item.is_file()
            and item.name.lower() == target
            for item in project_path.iterdir()
        )

    @staticmethod
    def _detect_technologies(
        files: list[Path],
    ) -> list[str]:
        technologies = set()

        extensions = {
            ".py": "Python",
            ".ipynb": "Jupyter Notebook",
            ".js": "JavaScript",
            ".html": "HTML",
            ".css": "CSS",
            ".sql": "SQL",
        }

        for file in files:
            technology = extensions.get(
                file.suffix.lower()
            )

            if technology:
                technologies.add(technology)

        return sorted(technologies)