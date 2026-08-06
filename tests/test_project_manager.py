from src.project_manager import ProjectManager

manager = ProjectManager()

proyecto = manager.load_project(
    input("Ruta del proyecto: ")
)

print("\nNombre:", proyecto.name)
print("Ruta:", proyecto.path)
print("¿Tiene Git?:", proyecto.is_git_repository)