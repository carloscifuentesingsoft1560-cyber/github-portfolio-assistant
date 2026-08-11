from src.project_manager import ProjectManager
from src.security_checker import SecurityChecker


project_manager = ProjectManager()

project = project_manager.load_project(
    input("Ruta del proyecto: ").strip()
)

checker = SecurityChecker(project)

result = checker.check()

print("\n" + "=" * 60)
print("              REVISIÓN DE SEGURIDAD")
print("=" * 60)

print(
    "Estado:",
    "SEGURO"
    if result["safe"]
    else "REQUIERE REVISIÓN",
)

print("\n--- Archivos potencialmente problemáticos detectados ---")

if result["detected_files"]:
    for item in result["detected_files"]:
        categories = ", ".join(
            item["categories"]
        )

        print(
            f"- {item['path']} "
            f"[{categories}] "
            f"({item['size_mb']} MB)"
        )
else:
    print("Ninguno.")

print("\n--- Protegidos por .gitignore ---")

if result["protected_files"]:
    for item in result["protected_files"]:
        print(f"- {item['path']}")
else:
    print("Ninguno.")

print("\n--- No protegidos ---")

if result["unprotected_files"]:
    for item in result["unprotected_files"]:
        print(f"- {item['path']}")
else:
    print("Ninguno.")

print("\n--- Advertencias ---")

if result["warnings"]:
    for warning in result["warnings"]:
        print(f"- {warning}")
else:
    print("No se encontraron advertencias.")

print("=" * 60)