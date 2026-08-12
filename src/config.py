import json
from pathlib import Path


class AppConfig:
    """
    Gestiona la configuración general de la aplicación.
    """

    DEFAULT_SETTINGS = {
        "author": "",
        "default_visibility": "public",
        "default_commit_prefix": "feat",
        "confirm_before_push": True,
    }

    def __init__(self) -> None:
        self.config_path = (
            Path(__file__).resolve().parent.parent
            / "config"
            / "settings.json"
        )

    def load(self) -> dict:
        """
        Carga la configuración desde settings.json.
        """

        if not self.config_path.exists():
            return self.DEFAULT_SETTINGS.copy()

        try:
            content = self.config_path.read_text(
                encoding="utf-8"
            )

            data = json.loads(content)

        except (
            OSError,
            json.JSONDecodeError,
        ):
            return self.DEFAULT_SETTINGS.copy()

        settings = self.DEFAULT_SETTINGS.copy()
        settings.update(data)

        return settings

    def save(self, settings: dict) -> None:
        """
        Guarda la configuración en settings.json.
        """

        self.config_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.config_path.write_text(
            json.dumps(
                settings,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def update(
        self,
        key: str,
        value,
    ) -> dict:
        """
        Actualiza una configuración específica.
        """

        settings = self.load()

        if key not in self.DEFAULT_SETTINGS:
            raise KeyError(
                f"Configuración desconocida: {key}"
            )

        settings[key] = value

        self.save(settings)

        return settings
    