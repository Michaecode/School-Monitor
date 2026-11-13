"""Load and validate the local INI configuration."""

from configparser import ConfigParser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / ".school-monitor.conf"


class ConfigurationError(RuntimeError):
    """Raised when required local configuration is missing or invalid."""


def load_config() -> ConfigParser:
    if not CONFIG_FILE.is_file():
        raise ConfigurationError(
            f"Configuration file not found: {CONFIG_FILE}. "
            "Copy school-monitor.conf.example to .school-monitor.conf."
        )

    parser = ConfigParser()
    parser.read(CONFIG_FILE, encoding="utf-8")

    required = {
        "clickedu": ("url", "username", "password"),
        "telegram": ("bot_token", "chat_id"),
        "settings": ("timezone",),
    }

    missing = [
        f"{section}.{key}"
        for section, keys in required.items()
        for key in keys
        if not parser.has_option(section, key)
        or not parser.get(section, key).strip()
    ]

    if missing:
        raise ConfigurationError(
            "Missing configuration values: " + ", ".join(missing)
        )

    return parser
