from pathlib import Path

from src.command_runner import CommandRunner
from src.project_manager import Project


class SecurityChecker:
    """
    Revisa archivos que podrían causar problemas
    antes de publicar un proyecto en GitHub.
    """

    SENSITIVE_FILENAMES = {
        ".env",
        ".env.local",
        ".env.production",
        ".env.development",
        "credentials.json",
        "secrets.json",
    }

    SENSITIVE_EXTENSIONS = {
        ".pem",
        ".key",
        ".p12",
        ".pfx",
    }

    VIDEO_EXTENSIONS = {
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
        ".wmv",
    }

    MODEL_EXTENSIONS = {
        ".pt",
        ".pth",
        ".onnx",
        ".h5",
        ".keras",
    }

    DATA_EXTENSIONS = {
        ".csv",
        ".jsonl",
        ".parquet",
    }

    LARGE_FILE_LIMIT_MB = 50

    IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    }

    def __init__(self, project: Project):
        self.project = project
        self.runner = CommandRunner()

    def _should_ignore(self, path: Path) -> bool:
        return any(
            part in self.IGNORED_DIRECTORIES
            for part in path.parts
        )

    def check(self) -> dict:
        """
        Ejecuta la revisión general del proyecto.
        """

        project_path = Path(self.project.path)

        detected_files = []

        for file_path in project_path.rglob("*"):
            if not file_path.is_file():
                continue

            if self._should_ignore(file_path):
                continue

            relative_path = file_path.relative_to(
                project_path
            )

            filename = file_path.name.lower()
            suffix = file_path.suffix.lower()

            categories = []

            if (
                filename in self.SENSITIVE_FILENAMES
                or suffix in self.SENSITIVE_EXTENSIONS
            ):
                categories.append("sensitive")

            if suffix in self.VIDEO_EXTENSIONS:
                categories.append("video")

            if suffix in self.MODEL_EXTENSIONS:
                categories.append("model")

            if suffix in self.DATA_EXTENSIONS:
                categories.append("data")

            try:
                size_mb = (
                    file_path.stat().st_size
                    / (1024 * 1024)
                )
            except OSError:
                size_mb = 0.0

            if size_mb >= self.LARGE_FILE_LIMIT_MB:
                categories.append("large")

            if not categories:
                continue

            ignored = self._is_ignored(
                relative_path
            )

            detected_files.append(
                {
                    "path": str(relative_path),
                    "categories": categories,
                    "ignored": ignored,
                    "size_mb": round(size_mb, 2),
                }
            )

        protected_files = [
            item
            for item in detected_files
            if item["ignored"]
        ]

        unprotected_files = [
            item
            for item in detected_files
            if not item["ignored"]
        ]

        warnings = self._build_warnings(
            unprotected_files
        )

        return {
            "safe": len(unprotected_files) == 0,
            "detected_files": detected_files,
            "protected_files": protected_files,
            "unprotected_files": unprotected_files,
            "warnings": warnings,
        }

    def _is_ignored(
        self,
        relative_path: Path,
    ) -> bool:
        """
        Comprueba si un archivo está protegido
        por las reglas actuales de .gitignore.
        """

        result = self.runner.run(
            [
                "git",
                "check-ignore",
                str(relative_path),
            ],
            working_directory=self.project.path,
        )

        return result.success

    @staticmethod
    def _build_warnings(
        unprotected_files: list[dict],
    ) -> list[str]:
        """
        Construye advertencias únicamente para
        archivos potencialmente problemáticos
        que Git no está ignorando.
        """

        warnings = []

        if not unprotected_files:
            return warnings

        sensitive_count = 0
        video_count = 0
        model_count = 0
        data_count = 0
        large_count = 0

        for item in unprotected_files:
            categories = item["categories"]

            if "sensitive" in categories:
                sensitive_count += 1

            if "video" in categories:
                video_count += 1

            if "model" in categories:
                model_count += 1

            if "data" in categories:
                data_count += 1

            if "large" in categories:
                large_count += 1

        if sensitive_count:
            warnings.append(
                f"{sensitive_count} archivo(s) "
                "potencialmente sensible(s) "
                "no están protegidos por .gitignore."
            )

        if video_count:
            warnings.append(
                f"{video_count} archivo(s) de video "
                "no están protegidos por .gitignore."
            )

        if model_count:
            warnings.append(
                f"{model_count} modelo(s) o peso(s) "
                "de IA no están protegidos por .gitignore."
            )

        if data_count:
            warnings.append(
                f"{data_count} archivo(s) de datos "
                "no están protegidos por .gitignore."
            )

        if large_count:
            warnings.append(
                f"{large_count} archivo(s) de 50 MB "
                "o más no están protegidos por .gitignore."
            )

        return warnings