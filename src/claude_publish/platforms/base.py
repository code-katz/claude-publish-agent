"""Abstract base class for platform adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PublishResult:
    """Result of a publish operation."""
    url: str
    status: str         # "draft" or "public"
    platform: str       # "medium", "linkedin"
    title: str
    post_id: str | None = None


class Platform(ABC):
    """Base class for publishing platform adapters."""

    name: str
    display_name: str

    @abstractmethod
    def authenticate(self, token: str) -> str:
        """Validate credentials and return display username.

        Raises requests.HTTPError or ValueError on failure.
        """
        ...

    @abstractmethod
    def publish(
        self,
        title: str,
        content: str,
        tags: list[str],
        publish_status: str = "draft",
    ) -> PublishResult:
        """Publish content to the platform. Returns result with URL."""
        ...
