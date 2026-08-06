from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

MAX_FILE_SIZE_MB = 45
SENSITIVE_PATTERNS = {
    "Token de GitHub": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "Clave privada": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Contraseña asignada": re.compile(
        r"(?i)(password|passwd|contraseña)\s*[:=]\s*[\"'][^\"']+[\"']"
    ),
}

IGNORED_DIRECTORIES = {
    ".git", ".venv", "venv", "__pycache__", "node_modules",
    ".idea", ".vscode", "runs", "dist", "build"
}

IGNORED_EXTENSIONS = {
    ".mp4", ".avi", ".mov", ".mkv", ".pt", ".pth", ".onnx",
    ".zip", ".rar", ".7z"
}


def run(command: list[str], cwd: Path, capture: bool = False) -> str:
    """Ejecuta un comando y detiene el programa si falla."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            text=True,
            capture_output=capture,
        )
        return result.stdout.strip() if capture else ""
    except FileNotFoundError:
        print(f"\nERROR: no se encontró el comando '{command[0]}'.")
        print("Verifica que Git y GitHub CLI estén instalados.")
        sys.exit(1)
    except subprocess.CalledProcessError as error:
        print(f"\nERROR al ejecutar: {' '.join(command)}")
        if error.stdout:
            print(error.stdout)
        if error.stderr:
            print(error.stderr)
        sys.exit(error.returncode)


def is_git_repository(project: Path) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=project,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def has_remote(project: Path) -> bool:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=project,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def iter_project_files(project: Path):
    for path in project.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(project).parts
        if any(part in IGNORED_DIRECTORIES for part in relative_parts):
            continue
        yield path


def security_review(project: Path) -> list[str]:
    warnings: list[str] = []

    for path in iter_project_files(project):
        relative = path.relative_to(project)
        size_mb = path.stat().st_size / (1024 * 1024)

        if size_mb > MAX_FILE_SIZE_MB:
            warnings.append(
                f"Archivo grande ({size_mb:.1f} MB): {relative}"
            )

        if path.name == ".env" or path.suffix.lower() in {".pem", ".key"}:
            warnings.append(f"Archivo sensible: {relative}")

        if path.suffix.lower() in IGNORED_EXTENSIONS:
            warnings.append(f"Archivo pesado o binario: {relative}")

        if size_mb <= 2:
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            for label, pattern in SENSITIVE_PATTERNS.items():
                if pattern.search(content):
                    warnings.append(f"{label} posiblemente expuesto en: {relative}")

    return warnings


def choose_commit_type() -> str:
    options = {
        "1": "feat",
        "2": "fix",
        "3": "docs",
        "4": "refactor",
        "5": "test",
        "6": "chore",
    }

    print("\nTipo de cambio:")
    print("1. feat     Nueva funcionalidad")
    print("2. fix      Corrección")
    print("3. docs     Documentación")
    print("4. refactor Reorganización del código")
    print("5. test     Pruebas")
    print("6. chore    Mantenimiento")

    while True:
        choice = input("Selecciona una opción [1-6]: ").strip()
        if choice in options:
            return options[choice]
        print("Opción no válida.")


def normalize_message(text: str) -> str:
    text = " ".join(text.strip().split())
    if not text:
        raise ValueError("La descripción del cambio no puede estar vacía.")
    return text[0].lower() + text[1:] if len(text) > 1 else text.lower()


def main() -> None:
    print("=" * 58)
    print(" ASISTENTE DE PUBLICACIÓN EN GITHUB - VERSIÓN 1")
    print("=" * 58)

    raw_path = input(
        "\nPega la ruta completa de la carpeta del proyecto: "
    ).strip().strip('"')

    project = Path(raw_path).expanduser().resolve()

    if not project.exists() or not project.is_dir():
        print("\nERROR: la carpeta indicada no existe.")
        sys.exit(1)

    if not is_git_repository(project):
        print("\nERROR: esta carpeta todavía no es un repositorio Git.")
        print("En la siguiente fase automatizaremos su creación.")
        sys.exit(1)

    if not has_remote(project):
        print("\nERROR: el repositorio no tiene un remoto llamado 'origin'.")
        print("En la siguiente fase automatizaremos la creación en GitHub.")
        sys.exit(1)

    print("\nRevisando archivos sensibles y archivos grandes...")
    warnings = security_review(project)

    if warnings:
        print("\nSe encontraron advertencias:")
        for warning in warnings:
            print(f" - {warning}")

        confirmation = input(
            "\nNo se publicará nada todavía. ¿Deseas continuar? [s/N]: "
        ).strip().lower()

        if confirmation != "s":
            print("Publicación cancelada.")
            return
    else:
        print("No se encontraron alertas básicas.")

    status = run(["git", "status", "--short"], project, capture=True)

    if not status:
        print("\nNo hay cambios pendientes para publicar.")
        return

    print("\nCambios detectados:")
    print(status)

    commit_type = choose_commit_type()
    description = normalize_message(
        input("\nDescribe brevemente lo que hiciste: ")
    )
    commit_message = f"{commit_type}: {description}"

    print(f"\nCommit propuesto:\n  {commit_message}")
    confirmation = input("\n¿Confirmas el commit y el push? [s/N]: ").strip().lower()

    if confirmation != "s":
        print("Operación cancelada.")
        return

    run(["git", "add", "."], project)

    staged = run(["git", "diff", "--cached", "--name-only"], project, capture=True)
    if not staged:
        print("\nNo quedaron archivos preparados para el commit.")
        return

    run(["git", "commit", "-m", commit_message], project)

    branch = run(
        ["git", "branch", "--show-current"],
        project,
        capture=True,
    )

    if not branch:
        print("\nERROR: no fue posible identificar la rama actual.")
        sys.exit(1)

    run(["git", "push", "origin", branch], project)

    remote_url = run(
        ["git", "remote", "get-url", "origin"],
        project,
        capture=True,
    )

    print("\nPublicación completada correctamente.")
    print(f"Repositorio remoto: {remote_url}")


if __name__ == "__main__":
    main()
