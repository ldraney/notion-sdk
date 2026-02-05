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
        template: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """POST /v1/pages — Create a new page.

        Args:
            parent: Parent object, e.g. ``{"type": "page_id", "page_id": "..."}``.
            properties: Page properties mapping.
            children: Optional list of block children to append to the page.
                Cannot be used when *template* is specified — they are mutually
                exclusive.
            template: Optional data-source template dict to create the page
                from.  Cannot be used together with *children*.  Expected
                format is one of::

                    {"type": "none"}
                    {"type": "default"}
                    {"type": "template_id", "template_id": "<uuid>"}

        """
        body: dict[str, Any] = {"parent": parent, "properties": properties}
        if children is not None:
            body["children"] = children
        if template is not None:
            body["template"] = template
        body.update(kwargs)
        return self._post("/pages", json=body)

    def get_page(self, page_id: str) -> dict[str, Any]:
        """GET /v1/pages/{page_id} — Retrieve a page."""
        return self._get(f"/pages/{page_id}")

    def update_page(
        self,
        page_id: str,
        erase_content: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """PATCH /v1/pages/{page_id} — Update page properties.

        Args:
            erase_content: If True, clears all block content from the page.

                .. warning::
                    This is a **destructive, irreversible** operation.  All
                    block children of the page will be permanently deleted and
                    cannot be recovered.
        """
        body = dict(kwargs)
        if erase_content is not None:
            body["erase_content"] = erase_content
        return self._patch(f"/pages/{page_id}", json=body)

    def archive_page(self, page_id: str) -> dict[str, Any]:
        """PATCH /v1/pages/{page_id} — Archive (soft-delete) a page."""
        return self._patch(f"/pages/{page_id}", json={"archived": True})

    def move_page(
        self,
        page_id: str,
        parent: dict[str, Any],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """POST /v1/pages/{page_id}/move — Move a page to a new parent.

        Args:
            parent: New parent object, e.g. {"type": "page_id", "page_id": "..."}
        """
        body: dict[str, Any] = {"parent": parent}
        body.update(kwargs)
        return self._post(f"/pages/{page_id}/move", json=body)
