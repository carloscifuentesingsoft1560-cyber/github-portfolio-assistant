from src.command_runner import CommandRunner, CommandResult
from src.project_manager import Project


class GitManager:
    """
    Gestiona operaciones básicas de Git.
    """

    def __init__(self, project: Project):
        self.project = project
        self.runner = CommandRunner()

    def execute(self, arguments: list[str]) -> CommandResult:
        """
        Ejecuta un comando Git dentro del proyecto.
        """
        return self.runner.run(
            ["git"] + arguments,
            working_directory=self.project.path,
        )

    def status(self) -> CommandResult:
        """
        Consulta el estado del repositorio.
        """
        return self.execute(["status"])

    def add_all(self) -> CommandResult:
        """
        Agrega todos los cambios al área de preparación.
        """
        return self.execute(["add", "."])

    def commit(self, message: str) -> CommandResult:
        """
        Crea un commit con el mensaje indicado.
        """
        return self.execute(
            ["commit", "-m", message]
        )

    def push(self) -> CommandResult:
        """
        Publica la rama actual en origin y configura upstream.
        """
        return self.execute(
            ["push", "-u", "origin", "HEAD"]
        )

    def get_remote_origin(self) -> CommandResult:
        """
        Devuelve la URL configurada para el remoto origin.
        """
        return self.execute(
            ["remote", "get-url", "origin"]
        )