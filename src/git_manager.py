from pathlib import Path
import subprocess

from src.project_manager import Project


class GitManager:
    """
    Gestiona operaciones básicas de Git.
    """

    def __init__(self, project: Project):
        self.project = project

    def status(self) -> str:
        """
        Devuelve el resultado de git status.
        """

        resultado = subprocess.run(
            ["git", "status"],
            cwd=self.project.path,
            capture_output=True,
            text=True
        )

        return resultado.stdout