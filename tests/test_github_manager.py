from src.github_manager import GitHubManager
from src.project_manager import ProjectManager


# --------------------------------------------------
# Cargar proyecto
# --------------------------------------------------

project_manager = ProjectManager()

project = project_manager.load_project(
    input("Ruta del proyecto: ").strip()
)

github = GitHubManager(project)


# --------------------------------------------------
# Comprobar autenticación
# --------------------------------------------------

print("\n--- Estado de autenticación ---")

auth_result = github.auth_status()

print("Éxito:", auth_result.success)

if auth_result.output:
    print(auth_result.output)

if auth_result.error:
    print(auth_result.error)


# --------------------------------------------------
# Comprobar repositorio existente
# --------------------------------------------------

print("\n--- Verificar repositorio ---")

repository = input(
    "Repositorio en formato usuario/repositorio: "
).strip()

repo_result = github.repo_exists(repository)

print("Existe:", repo_result.success)

if repo_result.output:
    print(repo_result.output)

if repo_result.error:
    print(repo_result.error)


# --------------------------------------------------
# Probar validación de create_repository
# --------------------------------------------------

print("\n--- Probar visibilidad inválida ---")

invalid_result = github.create_repository(
    repository_name="repositorio-prueba",
    visibility="oculto",
)

print("Éxito:", invalid_result.success)
print("Error:", invalid_result.error)
print("Código:", invalid_result.return_code)