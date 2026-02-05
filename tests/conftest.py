"""Shared pytest fixtures for Notion SDK integration tests."""

from __future__ import annotations

import pytest
from notion_sdk import NotionClient

TEST_PAGE_ID = "2fec2a37-9fe0-81c0-a47e-cced7c656073"


@pytest.fixture(scope="session")
def client() -> NotionClient:
    """Return a configured NotionClient (reads NOTION_API_KEY from .env)."""
    c = NotionClient()
    yield c
    c.close()


@pytest.fixture(scope="session")
def test_page_id() -> str:
    """The page ID the integration has access to."""
    return TEST_PAGE_ID


@pytest.fixture()
def cleanup_ids(client: NotionClient):
    """Collect IDs of objects to archive/delete after a test.

    Yields a dict with keys "pages", "databases", "blocks".
    After the test, everything listed is cleaned up.
    """
    ids: dict[str, list[str]] = {"pages": [], "databases": [], "blocks": []}
    yield ids

    for page_id in ids["pages"]:
        try:
            client.archive_page(page_id)
        except Exception:
            pass

    for db_id in ids["databases"]:
        try:
            client.archive_database(db_id)
        except Exception:
            pass

    for block_id in ids["blocks"]:
        try:
            client.delete_block(block_id)
        except Exception:
            pass
