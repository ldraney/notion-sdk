"""Search operation."""

from __future__ import annotations

from typing import Any


class SearchMixin:
    """Mixin providing search API method."""

    def search(
        self,
        query: str | None = None,
        filter: dict[str, Any] | None = None,
        sort: dict[str, Any] | None = None,
        start_cursor: str | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        """POST /v1/search — Search pages and databases."""
        body: dict[str, Any] = {}
        if query is not None:
            body["query"] = query
        if filter is not None:
            body["filter"] = filter
        if sort is not None:
            body["sort"] = sort
        if start_cursor is not None:
            body["start_cursor"] = start_cursor
        if page_size is not None:
            body["page_size"] = page_size
        return self._post("/search", json=body)
