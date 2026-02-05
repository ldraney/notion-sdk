"""Comment operations."""

from __future__ import annotations

from typing import Any


class CommentsMixin:
    """Mixin providing comment API methods."""

    def create_comment(
        self,
        parent: dict[str, Any],
        rich_text: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """POST /v1/comments — Create a comment."""
        body: dict[str, Any] = {"parent": parent, "rich_text": rich_text}
        body.update(kwargs)
        return self._post("/comments", json=body)

    def get_comments(
        self,
        block_id: str,
        start_cursor: str | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        """GET /v1/comments?block_id={block_id} — List comments on a block."""
        params: dict[str, Any] = {"block_id": block_id}
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        if page_size is not None:
            params["page_size"] = page_size
        return self._get("/comments", params=params)
