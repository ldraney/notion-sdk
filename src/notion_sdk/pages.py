"""Page operations."""

from __future__ import annotations

from typing import Any


class PagesMixin:
    """Mixin providing page API methods."""

    def create_page(
        self,
        parent: dict[str, Any],
        properties: dict[str, Any],
        children: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """POST /v1/pages — Create a new page."""
        body: dict[str, Any] = {"parent": parent, "properties": properties}
        if children is not None:
            body["children"] = children
        body.update(kwargs)
        return self._post("/pages", json=body)

    def get_page(self, page_id: str) -> dict[str, Any]:
        """GET /v1/pages/{page_id} — Retrieve a page."""
        return self._get(f"/pages/{page_id}")

    def update_page(self, page_id: str, **kwargs: Any) -> dict[str, Any]:
        """PATCH /v1/pages/{page_id} — Update page properties."""
        return self._patch(f"/pages/{page_id}", json=kwargs)

    def archive_page(self, page_id: str) -> dict[str, Any]:
        """PATCH /v1/pages/{page_id} — Archive (soft-delete) a page."""
        return self._patch(f"/pages/{page_id}", json={"archived": True})
