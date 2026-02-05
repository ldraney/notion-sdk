"""Integration tests for comment operations."""

from notion_sdk import NotionClient


def test_create_and_get_comments(
    client: NotionClient, test_page_id: str
):
    """Create a comment on the test page, then list comments."""
    # Create
    comment = client.create_comment(
        parent={"page_id": test_page_id},
        rich_text=[{"type": "text", "text": {"content": "SDK test comment"}}],
    )
    assert comment["object"] == "comment"
    assert comment["parent"]["page_id"] == test_page_id

    # List
    comments = client.get_comments(block_id=test_page_id)
    assert comments["object"] == "list"
    assert len(comments["results"]) >= 1
