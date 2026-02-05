"""Integration tests for the search endpoint."""

from notion_sdk import NotionClient


def test_search_returns_results(client: NotionClient):
    """POST /v1/search returns a paginated list."""
    result = client.search()
    assert "results" in result
    assert isinstance(result["results"], list)


def test_search_with_query(client: NotionClient):
    """POST /v1/search with a query string."""
    result = client.search(query="Test")
    assert "results" in result


def test_search_filter_pages(client: NotionClient):
    """POST /v1/search filtered to pages only."""
    result = client.search(filter={"value": "page", "property": "object"})
    assert "results" in result
    for item in result["results"]:
        assert item["object"] == "page"
