"""Block operations."""

from __future__ import annotations

from typing import Any


class BlocksMixin:
    """Mixin providing block API methods."""

    def get_block(self, block_id: str) -> dict[str, Any]:
        """GET /v1/blocks/{block_id} — Retrieve a block."""
        return self._get(f"/blocks/{block_id}")

    def get_block_children(
        self,
        block_id: str,
        start_cursor: str | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        """GET /v1/blocks/{block_id}/children — List child blocks."""
        params: dict[str, Any] = {}
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        if page_size is not None:
            params["page_size"] = page_size
        return self._get(f"/blocks/{block_id}/children", params=params or None)

    def append_block_children(
        self,
        block_id: str,
        children: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """PATCH /v1/blocks/{block_id}/children — Append child blocks."""
        return self._patch(
            f"/blocks/{block_id}/children", json={"children": children}
        )

    def update_block(self, block_id: str, **kwargs: Any) -> dict[str, Any]:
        """PATCH /v1/blocks/{block_id} — Update a block."""
        return self._patch(f"/blocks/{block_id}", json=kwargs)

    def delete_block(self, block_id: str) -> dict[str, Any]:
        """DELETE /v1/blocks/{block_id} — Delete (archive) a block."""
        return self._delete(f"/blocks/{block_id}")
