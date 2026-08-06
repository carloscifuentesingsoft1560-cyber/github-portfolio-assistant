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
        Ejecuta cualquier comando Git.
        """

        command = ["git"] + arguments

        return self.runner.run(
            command,
            working_directory=self.project.path
        )

    def status(self) -> CommandResult:
        return self.execute(["status"])

    def add_all(self) -> CommandResult:
        return self.execute(["add", "."])

    def commit(self, message: str) -> CommandResult:
        return self.execute(
            ["commit", "-m", message]
        )

    def push(self) -> CommandResult:
        return self.execute(["push"])