from src.project_manager import ProjectManager
from src.git_manager import GitManager


manager = ProjectManager()

project = manager.load_project(
    input("Ruta del proyecto: ")
)

git = GitManager(project)

print()

print(git.status())