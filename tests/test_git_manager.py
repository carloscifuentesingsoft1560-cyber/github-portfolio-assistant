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

print("\n--- Remote origin ---")

origin_result = git.get_remote_origin()

print("Éxito:", origin_result.success)

if origin_result.success:
    print("Origin:", origin_result.output)
else:
    print("No existe origin configurado.")

    if origin_result.error:
        print("Detalle:", origin_result.error)