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
        """
        return self.runner.run(
            ["gh", "repo", "view", repository],
            working_directory=self.project.path,
        )