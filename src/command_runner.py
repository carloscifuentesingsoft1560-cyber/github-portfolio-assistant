from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Sequence


@dataclass
class CommandResult:
    """Representa el resultado de ejecutar un comando del sistema."""

    success: bool
    output: str
    error: str
    return_code: int


class CommandRunner:
    """Ejecuta comandos del sistema de forma controlada."""

    def run(
        self,
        command: Sequence[str],
        working_directory: Path | None = None,
    ) -> CommandResult:
        try:
            result = subprocess.run(
                list(command),
                cwd=working_directory,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            return CommandResult(
                success=result.returncode == 0,
                output=(result.stdout or "").strip(),
                error=(result.stderr or "").strip(),
                return_code=result.returncode,
            )

        except FileNotFoundError:
            return CommandResult(
                success=False,
                output="",
                error=f"No se encontró el comando: {command[0]}",
                return_code=-1,
            )

        except OSError as error:
            return CommandResult(
                success=False,
                output="",
                error=str(error),
                return_code=-1,
            )