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


def test_create_page_with_template_param(
    client: NotionClient, test_page_id: str, cleanup_ids: dict
):
    """create_page accepts a template parameter without error.

    We pass template=None (the default) and verify the page is created
    normally. A full template test requires a database with templates
    configured, so this validates the parameter plumbing.
    """
    page = client.create_page(
        parent={"type": "page_id", "page_id": test_page_id},
        properties={"title": [{"text": {"content": "Template Param Test"}}]},
        template=None,
    )
    cleanup_ids["pages"].append(page["id"])
    assert page["object"] == "page"


def test_update_page_erase_content(
    client: NotionClient, test_page_id: str, cleanup_ids: dict
):
    """Create a page with content, then erase it with erase_content=True."""
    # Create page
    page = client.create_page(
        parent={"type": "page_id", "page_id": test_page_id},
        properties={"title": [{"text": {"content": "Erase Content Test"}}]},
        children=[
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": "This will be erased"}}]
                },
            }
        ],
    )
    cleanup_ids["pages"].append(page["id"])

    # Verify content exists
    blocks = client.get_block_children(page["id"])
    assert len(blocks["results"]) >= 1

    # Erase content
    updated = client.update_page(page["id"], erase_content=True)
    assert updated["object"] == "page"

    # Verify content is gone
    blocks_after = client.get_block_children(page["id"])
    assert len(blocks_after["results"]) == 0


def test_move_page(
    client: NotionClient, test_page_id: str, cleanup_ids: dict
):
    """Create two pages, move one under the other."""
    # Create parent page
    parent_page = client.create_page(
        parent={"type": "page_id", "page_id": test_page_id},
        properties={"title": [{"text": {"content": "Move Target"}}]},
    )
    cleanup_ids["pages"].append(parent_page["id"])

    # Create page to move
    child_page = client.create_page(
        parent={"type": "page_id", "page_id": test_page_id},
        properties={"title": [{"text": {"content": "Page To Move"}}]},
    )
    cleanup_ids["pages"].append(child_page["id"])

    # Move child under parent
    moved = client.move_page(
        child_page["id"],
        parent={"type": "page_id", "page_id": parent_page["id"]},
    )
    assert moved["object"] == "page"
    assert moved["parent"]["page_id"].replace("-", "") == parent_page["id"].replace("-", "")
