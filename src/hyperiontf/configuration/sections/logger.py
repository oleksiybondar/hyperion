import os
from pathlib import Path
from ..section import Section


class Logger(Section):
    """
    Represents the [log] section in the config.
    """

    def __init__(self):
        self._log_folder: str = ""
        self.intercept_selenium_logs = True
        self.intercept_playwright_logs = True
        self.intercept_appium_logs = True
        # Initialize via setter to enforce invariants
        self.log_folder = self._fetch_default_log_folder_value()

    @staticmethod
    def _fetch_default_log_folder_value():
        value = os.environ.get("HYPERION_LOG_FOLDER", None)
        if not value:
            return "logs"

        return value

    @property
    def log_folder(self) -> str:
        return self._log_folder

    @log_folder.setter
    def log_folder(self, value: str) -> None:
        folder = self._resolve_log_folder(value)
        self._ensure_folder_exists(folder)
        self._log_folder = str(folder)

    @staticmethod
    def _resolve_log_folder(value: str) -> Path:
        """
        Resolve log folder path according to context-aware rules:

        - "~/" is expanded to home
        - absolute paths are used as-is
        - relative paths are resolved under PWD
        """
        raw = str(value).strip()

        if raw.startswith("~"):
            return Path(raw).expanduser()

        path = Path(raw)
        if path.is_absolute():
            return path

        return Path(os.getcwd()) / path

    @staticmethod
    def _ensure_folder_exists(path: Path) -> None:
        """
        Ensure the log folder exists (mkdir -p behavior).
        """
        normalized = Path(os.path.normpath(str(path)))
        normalized.mkdir(parents=True, exist_ok=True)
