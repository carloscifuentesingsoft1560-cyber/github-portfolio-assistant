from src.github_manager import GitHubManager
from src.git_manager import GitManager
from src.project_manager import ProjectManager


project_manager = ProjectManager()

project = project_manager.load_project(
    input("Ruta del proyecto que desea publicar: ").strip()
)

github = GitHubManager(project)
git = GitManager(project)


print("\n--- Comprobar autenticación ---")

auth_result = github.auth_status()

if not auth_result.success:
    print("❌ GitHub CLI no está autenticado.")
    print(auth_result.error)
    raise SystemExit(1)

print("✅ GitHub CLI autenticado correctamente.")


print("\n--- Crear repositorio ---")

repository_name = input(
    "Nombre del nuevo repositorio: "
).strip()

confirmation = input(
    f"¿Desea crear '{repository_name}' como repositorio público? (s/n): "
).strip().lower()

if confirmation != "s":
    print("Operación cancelada.")
    raise SystemExit(0)

result = github.create_repository(
    repository_name=repository_name,
    visibility="public",
)

if not result.success:
    print("\n❌ No fue posible crear el repositorio.")

    if result.error:
        print(result.error)

    raise SystemExit(1)

print("\n✅ Repositorio creado correctamente.")

if result.output:
    print(result.output)


print("\n--- Publicar cambios ---")

push_result = git.push()

if push_result.success:
    print("✅ Proyecto publicado correctamente en GitHub.")

    if push_result.output:
        print(push_result.output)

else:
    print("❌ No fue posible publicar el proyecto.")

    if push_result.error:
        print(push_result.error)