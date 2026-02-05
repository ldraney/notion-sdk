"""Integration tests for user operations."""

from notion_sdk import NotionClient


def test_get_users(client: NotionClient):
    """GET /v1/users returns a list."""
    result = client.get_users()
    assert result["object"] == "list"
    assert "results" in result


def test_get_self(client: NotionClient):
    """GET /v1/users/me returns the bot user."""
    bot = client.get_self()
    assert bot["object"] == "user"
    assert bot["type"] == "bot"
