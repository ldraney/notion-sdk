"""Main Notion API client."""

from __future__ import annotations

import os
from typing import Any

import httpx
from dotenv import load_dotenv

from .pages import PagesMixin
from .databases import DatabasesMixin
from .blocks import BlocksMixin
from .users import UsersMixin
from .comments import CommentsMixin
from .search import SearchMixin

load_dotenv()

NOTION_BASE_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2025-09-03"


class NotionClient(
    PagesMixin,
    DatabasesMixin,
    BlocksMixin,
    UsersMixin,
    CommentsMixin,
    SearchMixin,
):
    """Synchronous Python client for the Notion API v2025-09-03."""

    def __init__(self, api_key: str | None = None, base_url: str = NOTION_BASE_URL):
        if api_key is None:
            api_key = os.environ.get("NOTION_API_KEY")
            if not api_key:
                raise ValueError(
                    "No API key provided. Pass api_key= or set NOTION_API_KEY env var."
                )
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._http = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    # ---- low-level helpers ------------------------------------------------

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._http.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._http.post(path, json=json or {})
        resp.raise_for_status()
        return resp.json()

    def _patch(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._http.patch(path, json=json or {})
        resp.raise_for_status()
        return resp.json()

    def _delete(self, path: str) -> dict[str, Any]:
        resp = self._http.delete(path)
        resp.raise_for_status()
        return resp.json()

    def close(self) -> None:
        self._http.close()
