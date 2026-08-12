from src.commit_generator import CommitGenerator
from src.project_manager import ProjectManager


project_manager = ProjectManager()

project = project_manager.load_project(
    input("Ruta del proyecto: ").strip()
)

generator = CommitGenerator(project)

message = generator.generate()

print("\n--- MENSAJE DE COMMIT SUGERIDO ---")
print(message)