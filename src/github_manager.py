from src.command_runner import CommandRunner, CommandResult
from src.project_manager import Project


class GitHubManager:
    """
    Gestiona operaciones relacionadas con GitHub mediante GitHub CLI.
    """

    def __init__(self, project: Project):
        self.project = project
        self.runner = CommandRunner()

    def auth_status(self) -> CommandResult:
        """
        Comprueba si GitHub CLI está autenticado.
        """
        return self.runner.run(
            ["gh", "auth", "status"],
            working_directory=self.project.path,
        )

    def repo_exists(self, repository: str) -> CommandResult:
        """
        Comprueba si un repositorio existe en GitHub.

        repository debe utilizar el formato:
        usuario/repositorio
        """
        return self.runner.run(
            ["gh", "repo", "view", repository],
            working_directory=self.project.path,
        )

    def create_repository(
        self,
        repository_name: str,
        visibility: str = "public",
    ) -> CommandResult:
        """
        Crea un repositorio nuevo en GitHub utilizando
        la carpeta del proyecto como repositorio local.
        """

        if visibility not in {"public", "private"}:
            return CommandResult(
                success=False,
                output="",
                error="La visibilidad debe ser 'public' o 'private'.",
                return_code=-1,
            )

        return self.runner.run(
            [
                "gh",
                "repo",
                "create",
                repository_name,
                f"--{visibility}",
                "--source=.",
                "--remote=origin",
            ],
            working_directory=self.project.path,
        )
    