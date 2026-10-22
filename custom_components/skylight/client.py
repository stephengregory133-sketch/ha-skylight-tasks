"""Skylight API client supporting both Bearer token and legacy session auth."""

from __future__ import annotations

import base64
from datetime import date
from typing import Any

import aiohttp

from .const import API_BASE_URL


class SkylightAuthError(Exception):
    """Exception to indicate authentication failure."""


class SkylightConnectionError(Exception):
    """Exception to indicate connection failure."""


class SkylightClient:
    """Skylight API client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        username: str,
        password: str,
        frame_id: str,
    ) -> None:
        """Initialize the Skylight client."""
        self._session = session
        self._username = username.strip()
        self._password = password.strip()
        if self._password.lower().startswith("bearer "):
            self._password = self._password[7:].strip()
        self._frame_id = frame_id.strip()
        self._auth_header: str | None = None

    async def async_login(self) -> None:
        """Authenticate with Skylight API using Bearer token or legacy session."""
        # First try password directly as a Bearer token against the frame endpoint
        try:
            async with self._session.get(
                f"{API_BASE_URL}/frames/{self._frame_id}",
                headers={
                    "Authorization": f"Bearer {self._password}",
                    "Accept": "application/json",
                },
                timeout=aiohttp.ClientTimeout(total=20),
            ) as resp:
                if resp.status == 200:
                    self._auth_header = f"Bearer {self._password}"
                    return
        except aiohttp.ClientError:
            pass

        # Fallback to legacy /api/sessions
        try:
            async with self._session.post(
                f"{API_BASE_URL}/sessions",
                json={
                    "email": self._username,
                    "name": "",
                    "phone": "",
                    "password": self._password,
                    "resettingPassword": "false",
                    "textMeTheApp": "true",
                    "agreedToMarketing": "true",
                },
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                if response.status == 401:
                    raise SkylightAuthError("Invalid username, password, or Bearer token")
                if response.status != 200:
                    raise SkylightConnectionError(
                        f"Login failed with status {response.status}"
                    )

                data = await response.json()
                user_id = data["data"]["id"]
                user_token = data["data"]["attributes"]["token"]
                b64 = base64.b64encode(f"{user_id}:{user_token}".encode()).decode()
                self._auth_header = f"Basic {b64}"

        except aiohttp.ClientError as err:
            raise SkylightConnectionError(f"Connection error: {err}") from err
        except KeyError as err:
            raise SkylightAuthError(f"Unexpected response format: {err}") from err

    async def async_create_chore(
        self,
        summary: str,
        emoji_icon: str | None = None,
        category_id: str | None = None,
    ) -> dict[str, Any]:
        """Create a chore in Skylight."""
        if not self._auth_header:
            await self.async_login()

        today = date.today().isoformat()
        payload: dict[str, Any] = {
            "summary": summary,
            "start": today,
            "start_time": None,
            "status": "pending",
            "recurring": False,
        }
        if emoji_icon:
            payload["emoji_icon"] = emoji_icon
        if category_id:
            payload["category_id"] = category_id

        try:
            async with self._session.post(
                f"{API_BASE_URL}/frames/{self._frame_id}/chores",
                headers={
                    "Authorization": self._auth_header or f"Bearer {self._password}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                if response.status not in (200, 201):
                    text = await response.text()
                    raise SkylightConnectionError(
                        f"Failed to create chore: {response.status} - {text}"
                    )
                return await response.json()
        except aiohttp.ClientError as err:
            raise SkylightConnectionError(f"Connection error: {err}") from err
