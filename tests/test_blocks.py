"""Integration tests for block operations."""

from notion_sdk import NotionClient


def test_get_block(client: NotionClient, test_page_id: str):
    """GET /v1/blocks/{block_id} — a page is also a block."""
    block = client.get_block(test_page_id)
    assert block["id"]
    assert block["object"] == "block"


def test_get_block_children(client: NotionClient, test_page_id: str):
    """GET /v1/blocks/{block_id}/children returns a list."""
    result = client.get_block_children(test_page_id)
    assert result["object"] == "list"
    assert "results" in result


def test_append_update_delete_block(
    client: NotionClient, test_page_id: str, cleanup_ids: dict
):
    """Append a paragraph block, update it, then delete it."""
    # Append
    appended = client.append_block_children(
        test_page_id,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "Hello from SDK"}}]
                },
            }
        ],
    )
    block_id = appended["results"][0]["id"]
    cleanup_ids["blocks"].append(block_id)

    # Update
    updated = client.update_block(
        block_id,
        paragraph={
            "rich_text": [{"type": "text", "text": {"content": "Updated from SDK"}}]
        },
    )
    assert updated["id"] == block_id

    # Delete
    deleted = client.delete_block(block_id)
    assert deleted["archived"] is True
    # Already deleted, remove from cleanup
    cleanup_ids["blocks"].remove(block_id)
