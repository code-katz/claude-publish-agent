"""Medium platform adapter."""

import requests

from claude_publish.platforms.base import Platform, PublishResult

API_BASE = "https://api.medium.com/v1"

DEFAULT_TAGS = ["Claude", "Claude Code", "AI Development", "Developer Tools", "AI Agents"]


class MediumPlatform(Platform):
    """Publish markdown to Medium via their API."""

    name = "medium"
    display_name = "Medium"

    def __init__(self) -> None:
        self._user_id: str | None = None
        self._username: str | None = None

    def authenticate(self, token: str) -> str:
        """Authenticate with Medium and return username."""
        resp = requests.get(
            f"{API_BASE}/me",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )

        if resp.status_code == 401:
            raise ValueError(
                "Authentication failed. Your token may be invalid or expired.\n"
                "Run 'claude-publish setup medium' to update it."
            )
        resp.raise_for_status()

        data = resp.json()["data"]
        self._user_id = data["id"]
        self._username = data.get("username", "unknown")
        self._token = token
        return self._username

    def publish(
        self,
        title: str,
        content: str,
        tags: list[str],
        publish_status: str = "draft",
    ) -> PublishResult:
        """Publish a markdown post to Medium."""
        if not self._user_id:
            raise RuntimeError("Must call authenticate() before publish()")

        # Medium limits to 5 tags
        tags = tags[:5]

        resp = requests.post(
            f"{API_BASE}/users/{self._user_id}/posts",
            headers={
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
            },
            json={
                "title": title,
                "contentFormat": "markdown",
                "content": content,
                "tags": tags,
                "publishStatus": publish_status,
            },
            timeout=30,
        )

        if resp.status_code == 429:
            raise ValueError("Rate limited by Medium. Try again in a few minutes.")
        resp.raise_for_status()

        data = resp.json()["data"]
        return PublishResult(
            url=data["url"],
            status=publish_status,
            platform=self.name,
            title=title,
            post_id=data.get("id"),
        )
