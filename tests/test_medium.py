"""Tests for the Medium platform adapter."""

import pytest
import responses

from claude_publish.platforms.medium import MediumPlatform, API_BASE


@pytest.fixture
def medium():
    return MediumPlatform()


@responses.activate
def test_authenticate_success(medium):
    responses.get(
        f"{API_BASE}/me",
        json={"data": {"id": "user-123", "username": "testuser"}},
    )
    username = medium.authenticate("valid-token")
    assert username == "testuser"


@responses.activate
def test_authenticate_invalid_token(medium):
    responses.get(f"{API_BASE}/me", status=401)
    with pytest.raises(ValueError, match="Authentication failed"):
        medium.authenticate("bad-token")


@responses.activate
def test_publish_draft(medium):
    responses.get(
        f"{API_BASE}/me",
        json={"data": {"id": "user-123", "username": "testuser"}},
    )
    responses.post(
        f"{API_BASE}/users/user-123/posts",
        json={
            "data": {
                "id": "post-456",
                "url": "https://medium.com/@testuser/my-post-abc123",
            }
        },
    )
    medium.authenticate("token")
    result = medium.publish("My Post", "# My Post\n\nContent.", ["AI"], "draft")

    assert result.url == "https://medium.com/@testuser/my-post-abc123"
    assert result.status == "draft"
    assert result.platform == "medium"
    assert result.title == "My Post"
    assert result.post_id == "post-456"


@responses.activate
def test_publish_public(medium):
    responses.get(
        f"{API_BASE}/me",
        json={"data": {"id": "user-123", "username": "testuser"}},
    )
    responses.post(
        f"{API_BASE}/users/user-123/posts",
        json={"data": {"id": "post-789", "url": "https://medium.com/@testuser/live"}},
    )
    medium.authenticate("token")
    result = medium.publish("Live Post", "Content", ["AI"], "public")
    assert result.status == "public"


@responses.activate
def test_publish_rate_limited(medium):
    responses.get(
        f"{API_BASE}/me",
        json={"data": {"id": "user-123", "username": "testuser"}},
    )
    responses.post(f"{API_BASE}/users/user-123/posts", status=429)
    medium.authenticate("token")
    with pytest.raises(ValueError, match="Rate limited"):
        medium.publish("Post", "Content", [], "draft")


def test_publish_without_auth(medium):
    with pytest.raises(RuntimeError, match="Must call authenticate"):
        medium.publish("Post", "Content", [], "draft")


@responses.activate
def test_tags_truncated_to_five(medium):
    responses.get(
        f"{API_BASE}/me",
        json={"data": {"id": "user-123", "username": "testuser"}},
    )
    responses.post(
        f"{API_BASE}/users/user-123/posts",
        json={"data": {"id": "p1", "url": "https://medium.com/post"}},
    )
    medium.authenticate("token")
    medium.publish("Post", "Content", ["a", "b", "c", "d", "e", "f", "g"], "draft")

    # Verify only 5 tags were sent
    import json
    body = json.loads(responses.calls[1].request.body)
    assert len(body["tags"]) == 5
