from src.project_manager import ProjectManager
from src.readme_generator import ReadmeGenerator


project_manager = ProjectManager()

project = project_manager.load_project(
    input("Ruta del proyecto: ").strip()
)

generator = ReadmeGenerator(project)

print("\n--- README GENERADO ---\n")

content = generator.generate_content()

print(content)