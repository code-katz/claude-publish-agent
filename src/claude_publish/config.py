"""Token storage and configuration management."""

import os
import stat
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "claude-publish"
LEGACY_MEDIUM_TOKEN = Path.home() / ".medium-token"


def _ensure_config_dir() -> None:
    """Create config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _token_path(platform: str) -> Path:
    """Return the token file path for a platform."""
    return CONFIG_DIR / f"{platform}.token"


def get_token(platform: str) -> str | None:
    """Read a platform token. Returns None if not configured."""
    path = _token_path(platform)
    if not path.exists():
        return None
    token = path.read_text().strip()
    return token if token else None


def save_token(platform: str, token: str) -> Path:
    """Save a platform token with restricted permissions. Returns the path."""
    _ensure_config_dir()
    path = _token_path(platform)
    path.write_text(token.strip() + "\n")
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 600
    return path


def is_configured(platform: str) -> bool:
    """Check if a platform has a valid token."""
    return get_token(platform) is not None


def list_configured() -> list[str]:
    """Return list of platform names with valid tokens."""
    if not CONFIG_DIR.exists():
        return []
    configured = []
    for path in CONFIG_DIR.glob("*.token"):
        name = path.stem
        if path.read_text().strip():
            configured.append(name)
    return sorted(configured)


def check_legacy_medium_token() -> str | None:
    """Check for legacy ~/.medium-token file. Returns token if found."""
    if LEGACY_MEDIUM_TOKEN.exists():
        token = LEGACY_MEDIUM_TOKEN.read_text().strip()
        return token if token else None
    return None
