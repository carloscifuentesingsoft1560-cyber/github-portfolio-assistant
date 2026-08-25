import json
import re
from pathlib import Path

from src.project_manager import Project


class ProjectAnalyzer:
    """
    Analiza la estructura y tecnologías de un proyecto.
    """
    IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    }

    def __init__(self, project: Project):
        self.project = project

    def _should_ignore(self, path: Path) -> bool:
        return any(
            part in self.IGNORED_DIRECTORIES
            for part in path.parts
    )

    def analyze(self) -> dict:
        """
        Devuelve un resumen general del proyecto.
        """

        project_path = Path(self.project.path)

        files = [
            item
            for item in project_path.rglob("*")
            if item.is_file()
            and not self._should_ignore(item)
        ]

        directories = [
            item
            for item in project_path.rglob("*")
            if item.is_dir()
            and not self._should_ignore(item)
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
            "has_gitignore": (
                project_path / ".gitignore"
            ).exists(),
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

    def _detect_technologies(
        self,
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
            suffix = file.suffix.lower()

            technology = extensions.get(suffix)

            if technology:
                technologies.add(technology)

            if suffix == ".py":
                content = self._read_python_file(file)

                self._detect_imports(
                    content,
                    technologies,
                )

            elif suffix == ".ipynb":
                content = self._read_notebook(file)

                self._detect_imports(
                    content,
                    technologies,
                )

        return sorted(technologies)

    @staticmethod
    def _read_python_file(
        file_path: Path,
    ) -> str:
        try:
            return file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except OSError:
            return ""

    @staticmethod
    def _read_notebook(
        file_path: Path,
    ) -> str:
        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            notebook = json.loads(content)

        except (
            OSError,
            json.JSONDecodeError,
        ):
            return ""

        code_parts = []

        for cell in notebook.get("cells", []):
            if cell.get("cell_type") != "code":
                continue

            source = cell.get("source", [])

            if isinstance(source, list):
                code_parts.extend(source)

            elif isinstance(source, str):
                code_parts.append(source)

        return "\n".join(code_parts)

    @staticmethod
    def _detect_imports(
        content: str,
        technologies: set[str],
    ) -> None:
        """
        Detecta librerías conocidas a partir de imports.
        """

        library_patterns = {
            "Ultralytics / YOLO": [
                r"\bfrom\s+ultralytics\b",
                r"\bimport\s+ultralytics\b",
            ],
            "OpenCV": [
                r"\bimport\s+cv2\b",
                r"\bfrom\s+cv2\b",
            ],
            "NumPy": [
                r"\bimport\s+numpy\b",
                r"\bfrom\s+numpy\b",
            ],
            "Pandas": [
                r"\bimport\s+pandas\b",
                r"\bfrom\s+pandas\b",
            ],
            "Matplotlib": [
                r"\bimport\s+matplotlib\b",
                r"\bfrom\s+matplotlib\b",
            ],
            "MediaPipe": [
                r"\bimport\s+mediapipe\b",
                r"\bfrom\s+mediapipe\b",
            ],
            "PyTorch": [
                r"\bimport\s+torch\b",
                r"\bfrom\s+torch\b",
            ],
            "TensorFlow": [
                r"\bimport\s+tensorflow\b",
                r"\bfrom\s+tensorflow\b",
            ],
            "Scikit-learn": [
                r"\bimport\s+sklearn\b",
                r"\bfrom\s+sklearn\b",
            ],
        }

        for technology, patterns in library_patterns.items():
            for pattern in patterns:
                if re.search(
                    pattern,
                    content,
                    flags=re.IGNORECASE,
                ):
                    technologies.add(technology)
                    break