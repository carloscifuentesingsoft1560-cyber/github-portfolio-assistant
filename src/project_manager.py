from dataclasses import dataclass
from pathlib import Path


@dataclass
class Project:
    """
    Representa un proyecto almacenado en el equipo.
    """

    path: Path

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def is_git_repository(self) -> bool:
        return (self.path / ".git").exists()


class ProjectManager:
    """
    Administra la selección y validación de proyectos.
    """

    def load_project(self, project_path: str) -> Project:
        path = Path(project_path).expanduser().resolve()

        if not path.exists():
            raise FileNotFoundError(
                f"La ruta '{project_path}' no existe."
            )

        if not path.is_dir():
            raise NotADirectoryError(
                f"'{project_path}' no es una carpeta."
            )

        return Project(path)