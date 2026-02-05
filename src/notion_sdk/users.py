"""User operations."""

from __future__ import annotations

from typing import Any


class UsersMixin:
    """Mixin providing user API methods."""

    def get_users(
        self,
        start_cursor: str | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        """GET /v1/users — List all users."""
        params: dict[str, Any] = {}
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        if page_size is not None:
            params["page_size"] = page_size
        return self._get("/users", params=params or None)

    def get_self(self) -> dict[str, Any]:
        """GET /v1/users/me — Retrieve the bot user."""
        return self._get("/users/me")
