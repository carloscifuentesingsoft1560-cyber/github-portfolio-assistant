from src.github_manager import GitHubManager
from src.project_manager import ProjectManager


project_manager = ProjectManager()

project = project_manager.load_project(
    input("Ruta del proyecto: ")
)

github = GitHubManager(project)

print("\n--- Estado de autenticación ---")

auth_result = github.auth_status()

print("Éxito:", auth_result.success)

if auth_result.output:
    print(auth_result.output)

if auth_result.error:
    print(auth_result.error)


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