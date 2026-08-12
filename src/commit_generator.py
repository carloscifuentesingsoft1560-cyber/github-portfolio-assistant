from src.git_manager import GitManager
from src.project_manager import Project


class CommitGenerator:
    """
    Genera sugerencias básicas de mensajes de commit
    a partir de los cambios detectados por Git.
    """

    def __init__(self, project: Project):
        self.project = project
        self.git = GitManager(project)

    def generate(self) -> str:
        """
        Analiza los cambios del repositorio y propone
        un mensaje de commit.
        """

        result = self.git.execute(
            ["status", "--short"]
        )

        if not result.success:
            return "chore: actualiza archivos del proyecto"

        lines = [
            line.strip()
            for line in result.output.splitlines()
            if line.strip()
        ]

        if not lines:
            return "chore: sin cambios pendientes"

        filenames = [
            line[3:].strip()
            for line in lines
            if len(line) >= 4
        ]

        if self._only_documentation(filenames):
            return "docs: actualiza documentacion del proyecto"

        if self._only_tests(filenames):
            return "test: actualiza pruebas del proyecto"

        if self._contains_readme(filenames):
            return "docs: actualiza README del proyecto"

        if self._contains_python(filenames):
            return "feat: actualiza funcionalidades del proyecto"

        if self._contains_configuration(filenames):
            return "chore: actualiza configuracion del proyecto"

        return "chore: actualiza archivos del proyecto"

    @staticmethod
    def _only_documentation(
        filenames: list[str],
    ) -> bool:
        if not filenames:
            return False

        documentation_extensions = {
            ".md",
            ".txt",
            ".rst",
        }

        return all(
            any(
                filename.lower().endswith(extension)
                for extension in documentation_extensions
            )
            for filename in filenames
        )

    @staticmethod
    def _only_tests(
        filenames: list[str],
    ) -> bool:
        if not filenames:
            return False

        return all(
            "test" in filename.lower()
            for filename in filenames
        )

    @staticmethod
    def _contains_readme(
        filenames: list[str],
    ) -> bool:
        return any(
            "readme" in filename.lower()
            for filename in filenames
        )

    @staticmethod
    def _contains_python(
        filenames: list[str],
    ) -> bool:
        return any(
            filename.lower().endswith(".py")
            for filename in filenames
        )

    @staticmethod
    def _contains_configuration(
        filenames: list[str],
    ) -> bool:
        configuration_names = {
            ".gitignore",
            "requirements.txt",
            "pyproject.toml",
            "setup.cfg",
            "settings.json",
        }

        return any(
            filename.lower().endswith(
                tuple(configuration_names)
            )
            for filename in filenames
        )