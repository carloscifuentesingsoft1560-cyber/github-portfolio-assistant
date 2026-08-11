from src.project_analyzer import ProjectAnalyzer
from src.project_manager import ProjectManager


project_manager = ProjectManager()

project = project_manager.load_project(
    input("Ruta del proyecto: ").strip()
)

analyzer = ProjectAnalyzer(project)

result = analyzer.analyze()

print("\n--- ANÁLISIS DEL PROYECTO ---")

print("Nombre:", result["name"])
print("Ruta:", result["path"])
print("Repositorio Git:", result["is_git_repository"])
print("README:", result["has_readme"])
print(".gitignore:", result["has_gitignore"])
print("requirements.txt:", result["has_requirements"])
print("Archivos:", result["file_count"])
print("Carpetas:", result["directory_count"])
print(
    "Tecnologías:",
    ", ".join(result["technologies"])
    or "No detectadas",
)