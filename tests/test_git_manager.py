from src.git_manager import GitManager
from src.project_manager import ProjectManager

manager = ProjectManager()

project = manager.load_project(
    input("Ruta del proyecto: ")
)

git = GitManager(project)

resultado = git.status()

print("\nÉxito:", resultado.success)
print("\nSalida:\n")
print(resultado.output)

if resultado.error:
    print("\nError:")
    print(resultado.error)