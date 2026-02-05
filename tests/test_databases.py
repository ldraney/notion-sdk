"""Integration tests for database operations — the critical tests.

In Notion API v2025-09-03 properties live on *data sources*, not on the
database object.  After creating a database we retrieve its first data source
to verify the properties round-tripped correctly.
"""

from notion_sdk import NotionClient


def test_create_database_with_properties(
    client: NotionClient, test_page_id: str, cleanup_ids: dict
):
    """THE critical test: create a database with select properties via
    initial_data_source.properties, then retrieve the data source and
    verify the properties exist."""
    db = client.create_database(
        parent={"type": "page_id", "page_id": test_page_id},
        title=[{"text": {"content": "SDK Critical Test DB"}}],
        initial_data_source={
            "properties": {
                "Name": {"type": "title", "title": {}},
                "Category": {
                    "type": "select",
                    "select": {
                        "options": [{"name": "Linux", "color": "green"}]
                    },
                },
                "Status": {
                    "type": "select",
                    "select": {
                        "options": [{"name": "Draft", "color": "yellow"}]
                    },
                },
            }
        },
    )
    cleanup_ids["databases"].append(db["id"])

    assert db["object"] == "database"
    assert "data_sources" in db and len(db["data_sources"]) >= 1

    # Retrieve the data source and verify properties survived the round-trip
    ds = client.get_data_source(db["data_sources"][0]["id"])
    assert "Category" in ds["properties"], (
        "Category property missing — initial_data_source not applied!"
    )
    assert "Status" in ds["properties"], (
        "Status property missing — initial_data_source not applied!"
    )
    assert ds["properties"]["Category"]["type"] == "select"
    assert ds["properties"]["Status"]["type"] == "select"


def test_query_database(
    client: NotionClient, test_page_id: str, cleanup_ids: dict
):
    """Create a database, add a row, query it back."""
    db = client.create_database(
        parent={"type": "page_id", "page_id": test_page_id},
        title=[{"text": {"content": "Query Test DB"}}],
        initial_data_source={
            "properties": {
                "Name": {"type": "title", "title": {}},
            }
        },
    )
    cleanup_ids["databases"].append(db["id"])

    # Add a row (page inside database)
    row = client.create_page(
        parent={"type": "database_id", "database_id": db["id"]},
        properties={
            "Name": {"title": [{"text": {"content": "Row 1"}}]},
        },
    )
    cleanup_ids["pages"].append(row["id"])

    # Query via the convenience method (resolves data source automatically)
    result = client.query_database(db["id"])
    assert result["object"] == "list"
    assert len(result["results"]) >= 1


def test_update_database_title(
    client: NotionClient, test_page_id: str, cleanup_ids: dict
):
    """Create a database then update its title."""
    db = client.create_database(
        parent={"type": "page_id", "page_id": test_page_id},
        title=[{"text": {"content": "Before Update"}}],
        initial_data_source={
            "properties": {
                "Name": {"type": "title", "title": {}},
            }
        },
    )
    cleanup_ids["databases"].append(db["id"])

    updated = client.update_database(
        db["id"],
        title=[{"text": {"content": "After Update"}}],
    )
    # The title rich-text array should reflect the change
    assert any(
        t.get("text", {}).get("content") == "After Update"
        for t in updated.get("title", [])
    )


def test_get_data_source(
    client: NotionClient, test_page_id: str, cleanup_ids: dict
):
    """Create a database and retrieve its data source directly."""
    db = client.create_database(
        parent={"type": "page_id", "page_id": test_page_id},
        title=[{"text": {"content": "Data Source Test DB"}}],
        initial_data_source={
            "properties": {
                "Name": {"type": "title", "title": {}},
                "Priority": {
                    "type": "select",
                    "select": {
                        "options": [
                            {"name": "High", "color": "red"},
                            {"name": "Low", "color": "blue"},
                        ]
                    },
                },
            }
        },
    )
    cleanup_ids["databases"].append(db["id"])

    ds_id = db["data_sources"][0]["id"]
    ds = client.get_data_source(ds_id)

    assert ds["object"] == "data_source"
    assert "Priority" in ds["properties"]
    assert ds["properties"]["Priority"]["type"] == "select"
    options = ds["properties"]["Priority"]["select"]["options"]
    option_names = {o["name"] for o in options}
    assert "High" in option_names
    assert "Low" in option_names


def test_list_data_source_templates(
    client: NotionClient, test_page_id: str, cleanup_ids: dict
):
    """Create a database and list its data source templates (may be empty)."""
    db = client.create_database(
        parent={"type": "page_id", "page_id": test_page_id},
        title=[{"text": {"content": "Templates Test DB"}}],
        initial_data_source={
            "properties": {
                "Name": {"type": "title", "title": {}},
            }
        },
    )
    cleanup_ids["databases"].append(db["id"])

    ds_id = db["data_sources"][0]["id"]
    result = client.list_data_source_templates(ds_id)
    assert result["object"] == "list"
