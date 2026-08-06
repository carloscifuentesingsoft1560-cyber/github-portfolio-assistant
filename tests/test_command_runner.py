from pathlib import Path

from src.command_runner import CommandRunner


runner = CommandRunner()

result = runner.run(
    ["git", "--version"],
    working_directory=Path.cwd(),
)

print("Éxito:", result.success)
print("Salida:", result.output)
print("Error:", result.error)
print("Código:", result.return_code)