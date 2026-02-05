"""Integration tests for page operations."""

from notion_sdk import NotionClient


def test_get_page(client: NotionClient, test_page_id: str):
    """GET /v1/pages/{page_id} retrieves the test page."""
    page = client.get_page(test_page_id)
    assert page["id"].replace("-", "") == test_page_id.replace("-", "")
    assert page["object"] == "page"


def test_create_and_archive_page(
    client: NotionClient, test_page_id: str, cleanup_ids: dict
):
    """Create a child page, verify it exists, then archive it."""
    page = client.create_page(
        parent={"type": "page_id", "page_id": test_page_id},
        properties={"title": [{"text": {"content": "SDK Test Page"}}]},
    )
    cleanup_ids["pages"].append(page["id"])

    assert page["object"] == "page"
    assert page["archived"] is False

    # Retrieve
    fetched = client.get_page(page["id"])
    assert fetched["id"] == page["id"]

    # Archive
    archived = client.archive_page(page["id"])
    assert archived["archived"] is True


def test_update_page_icon(
    client: NotionClient, test_page_id: str, cleanup_ids: dict
):
    """Create a page then update its icon."""
    page = client.create_page(
        parent={"type": "page_id", "page_id": test_page_id},
        properties={"title": [{"text": {"content": "Icon Test"}}]},
    )
    cleanup_ids["pages"].append(page["id"])

    updated = client.update_page(
        page["id"],
        icon={"type": "emoji", "emoji": "🧪"},
    )
    assert updated["icon"]["emoji"] == "\U0001f9ea"
