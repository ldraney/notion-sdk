"""Database and data source operations — uses initial_data_source.properties for creation.

In Notion API v2025-09-03, database properties live on *data sources*, not on
the database object itself.  When you create a database the properties go inside
``initial_data_source.properties``.  After creation you retrieve properties via
``GET /v1/data_sources/{data_source_id}``.  Querying rows also happens on the
data source: ``POST /v1/data_sources/{data_source_id}/query``.
"""

from __future__ import annotations

from typing import Any


class DatabasesMixin:
    """Mixin providing database and data-source API methods."""

    # ---- databases --------------------------------------------------------

    def create_database(
        self,
        parent: dict[str, Any],
        title: list[dict[str, Any]],
        initial_data_source: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """POST /v1/databases — Create a database.

        Properties MUST be passed inside ``initial_data_source.properties``
        (Notion API v2025-09-03 requirement).
        """
        body: dict[str, Any] = {"parent": parent, "title": title}
        if initial_data_source is not None:
            body["initial_data_source"] = initial_data_source
        body.update(kwargs)
        return self._post("/databases", json=body)

    def get_database(self, database_id: str) -> dict[str, Any]:
        """GET /v1/databases/{database_id} — Retrieve a database.

        Note: In v2025-09-03 the response contains ``data_sources`` but NOT
        ``properties``.  Use :meth:`get_data_source` to inspect properties.
        """
        return self._get(f"/databases/{database_id}")

    def update_database(self, database_id: str, **kwargs: Any) -> dict[str, Any]:
        """PATCH /v1/databases/{database_id} — Update a database."""
        return self._patch(f"/databases/{database_id}", json=kwargs)

    def archive_database(self, database_id: str) -> dict[str, Any]:
        """PATCH /v1/databases/{database_id} — Archive a database."""
        return self._patch(f"/databases/{database_id}", json={"archived": True})

    def query_database(
        self,
        database_id: str,
        filter: dict[str, Any] | None = None,
        sorts: list[dict[str, Any]] | None = None,
        start_cursor: str | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        """Query a database.

        In v2025-09-03 this resolves the first data source automatically and
        queries via ``POST /v1/data_sources/{ds_id}/query``.  If you already
        know the data-source ID, use :meth:`query_data_source` directly.
        """
        db = self.get_database(database_id)
        ds_id = db["data_sources"][0]["id"]
        return self.query_data_source(
            ds_id,
            filter=filter,
            sorts=sorts,
            start_cursor=start_cursor,
            page_size=page_size,
        )

    # ---- data sources -----------------------------------------------------

    def get_data_source(self, data_source_id: str) -> dict[str, Any]:
        """GET /v1/data_sources/{data_source_id} — Retrieve a data source (includes properties)."""
        return self._get(f"/data_sources/{data_source_id}")

    def update_data_source(self, data_source_id: str, **kwargs: Any) -> dict[str, Any]:
        """PATCH /v1/data_sources/{data_source_id} — Update a data source."""
        return self._patch(f"/data_sources/{data_source_id}", json=kwargs)

    def query_data_source(
        self,
        data_source_id: str,
        filter: dict[str, Any] | None = None,
        sorts: list[dict[str, Any]] | None = None,
        start_cursor: str | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        """POST /v1/data_sources/{data_source_id}/query — Query rows in a data source."""
        body: dict[str, Any] = {}
        if filter is not None:
            body["filter"] = filter
        if sorts is not None:
            body["sorts"] = sorts
        if start_cursor is not None:
            body["start_cursor"] = start_cursor
        if page_size is not None:
            body["page_size"] = page_size
        return self._post(f"/data_sources/{data_source_id}/query", json=body)

    def list_data_source_templates(
        self,
        data_source_id: str,
        name: str | None = None,
        start_cursor: str | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        """GET /v1/data_sources/{data_source_id}/templates — List templates for a data source."""
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        if page_size is not None:
            params["page_size"] = page_size
        return self._get(f"/data_sources/{data_source_id}/templates", params=params or None)
