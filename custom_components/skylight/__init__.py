"""The Skylight integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

from .client import (
    SkylightAuthError,
    SkylightClient,
    SkylightConnectionError,
)
from .const import (
    ATTR_CATEGORY_ID,
    ATTR_EMOJI_ICON,
    ATTR_MEDIA_PLAYER,
    ATTR_PERSON,
    ATTR_SUMMARY,
    ATTR_TTS_ENTITY,
    ATTR_VOLUME_LEVEL,
    CONF_FRAME_ID,
    DOMAIN,
    SERVICE_ANNOUNCE_CHORES,
    SERVICE_CREATE_CHORE,
)

type SkylightConfigEntry = ConfigEntry[SkylightClient]


def _get_client(hass: HomeAssistant, config_entry_id: str | None) -> SkylightClient:
    if not config_entry_id:
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            raise ServiceValidationError(
                "No Skylight accounts configured. Please add a Skylight integration first"
            )
        entry = entries[0]
    else:
        entry = hass.config_entries.async_get_entry(config_entry_id)
        if not entry:
            raise ServiceValidationError(f"Config entry {config_entry_id} not found")
    return entry.runtime_data


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Skylight integration."""

    async def async_handle_create_chore(call: ServiceCall) -> None:
        client = _get_client(hass, call.data.get("config_entry_id"))
        summary = call.data[ATTR_SUMMARY]
        emoji_icon = call.data.get(ATTR_EMOJI_ICON)
        category_id = call.data.get(ATTR_CATEGORY_ID)
        try:
            await client.async_create_chore(
                summary=summary,
                emoji_icon=emoji_icon,
                category_id=category_id,
            )
        except (SkylightAuthError, SkylightConnectionError) as err:
            raise HomeAssistantError(f"Error creating chore: {err}") from err

    async def async_handle_announce_chores(call: ServiceCall) -> None:
        client = _get_client(hass, call.data.get("config_entry_id"))
        person = call.data[ATTR_PERSON].strip()
        media_player = call.data.get(ATTR_MEDIA_PLAYER, "media_player.living_room_display")
        tts_entity = call.data.get(ATTR_TTS_ENTITY, "tts.google_translate_en_com")
        volume = call.data.get(ATTR_VOLUME_LEVEL, 0.5)

        try:
            tasks = await client.async_get_pending_chores_for_person(person)
        except (SkylightAuthError, SkylightConnectionError) as err:
            raise HomeAssistantError(f"Error fetching chores: {err}") from err

        if not tasks:
            msg = f"Attention {person}. You have no pending chores on the Skylight calendar for today."
        elif len(tasks) == 1:
            msg = f"Attention {person}, this is your chore for the day: {tasks[0]}."
        else:
            joined = ", ".join(tasks[:-1]) + f", and {tasks[-1]}"
            msg = f"Attention {person}, this is your list of chores for the day: {joined}."

        if volume is not None:
            await hass.services.async_call(
                "media_player",
                "volume_set",
                {"entity_id": media_player, "volume_level": float(volume)},
                blocking=True,
            )

        await hass.services.async_call(
            "tts",
            "speak",
            {
                "entity_id": tts_entity,
                "media_player_entity_id": media_player,
                "cache": True,
                "message": msg,
            },
            blocking=True,
        )

    hass.services.async_register(
        DOMAIN,
        SERVICE_CREATE_CHORE,
        async_handle_create_chore,
        schema=vol.Schema(
            {
                vol.Optional("config_entry_id"): cv.string,
                vol.Required(ATTR_SUMMARY): cv.string,
                vol.Optional(ATTR_EMOJI_ICON): cv.string,
                vol.Optional(ATTR_CATEGORY_ID): cv.string,
            }
        ),
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_ANNOUNCE_CHORES,
        async_handle_announce_chores,
        schema=vol.Schema(
            {
                vol.Optional("config_entry_id"): cv.string,
                vol.Required(ATTR_PERSON): cv.string,
                vol.Optional(ATTR_MEDIA_PLAYER, default="media_player.living_room_display"): cv.string,
                vol.Optional(ATTR_TTS_ENTITY, default="tts.google_translate_en_com"): cv.string,
                vol.Optional(ATTR_VOLUME_LEVEL, default=0.5): vol.Coerce(float),
            }
        ),
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: SkylightConfigEntry) -> bool:
    """Set up Skylight from a config entry."""
    session = async_get_clientsession(hass)
    client = SkylightClient(
        session=session,
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        frame_id=entry.data[CONF_FRAME_ID],
    )
    entry.runtime_data = client
    return True


async def async_unload_entry(hass: HomeAssistant, entry: SkylightConfigEntry) -> bool:
    """Unload a config entry."""
    return True
