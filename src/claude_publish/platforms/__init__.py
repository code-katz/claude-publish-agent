"""Platform registry."""

from claude_publish.platforms.base import Platform
from claude_publish.platforms.medium import MediumPlatform

PLATFORMS: dict[str, type[Platform]] = {
    "medium": MediumPlatform,
}


def get_platform(name: str) -> Platform:
    """Get a platform adapter by name."""
    cls = PLATFORMS.get(name)
    if cls is None:
        available = ", ".join(sorted(PLATFORMS))
        raise ValueError(f"Unknown platform: {name}. Available: {available}")
    return cls()
