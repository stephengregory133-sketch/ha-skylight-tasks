"""The Skylight integration."""

from __future__ import annotations

from typing import Any

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
    ATTR_SUMMARY,
    CONF_FRAME_ID,
    DOMAIN,
    LOGGER,
    SERVICE_CREATE_CHORE,
)

type SkylightConfigEntry = ConfigEntry[SkylightClient]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Skylight integration."""

    async def async_handle_create_chore(call: ServiceCall) -> None:
        """Handle the create_chore service call."""
        # Get the config entry ID from the service call
        config_entry_id = call.data.get("config_entry_id")

        # If no config_entry_id provided, use the first configured account
        if not config_entry_id:
            entries = hass.config_entries.async_entries(DOMAIN)
            if not entries:
                raise ServiceValidationError(
                    "No Skylight accounts configured. Please add a Skylight integration first"
                )
            entry = entries[0]
            LOGGER.debug(
                "No config_entry_id provided, using first configured account: %s",
                entry.title,
            )
        else:
            # Get the config entry
            entry: SkylightConfigEntry | None = hass.config_entries.async_get_entry(
                config_entry_id
            )

            if not entry:
                raise ServiceValidationError(
                    f"Config entry {config_entry_id} not found"
                )

        # Get the client from runtime data
        client: SkylightClient = entry.runtime_data

        # Extract service call parameters
        summary = call.data[ATTR_SUMMARY]
        emoji_icon = call.data.get(ATTR_EMOJI_ICON)
        category_id = call.data.get(ATTR_CATEGORY_ID)

        # Validate required parameters
        if not summary:
            raise ServiceValidationError("Summary is required")

        try:
            # Create the chore
            result = await client.async_create_chore(
                summary=summary,
                emoji_icon=emoji_icon,
                category_id=category_id,
            )
            LOGGER.info("Successfully created chore: %s", summary)
            LOGGER.debug("Chore creation result: %s", result)

        except SkylightAuthError as err:
            raise HomeAssistantError(
                f"Authentication failed when creating chore: {err}"
            ) from err
        except SkylightConnectionError as err:
            raise HomeAssistantError(
                f"Connection error when creating chore: {err}"
            ) from err

    # Register the service
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

    return True


async def async_setup_entry(hass: HomeAssistant, entry: SkylightConfigEntry) -> bool:
    """Set up Skylight from a config entry."""
    session = async_get_clientsession(hass)

    # Create the client
    client = SkylightClient(
        session=session,
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        frame_id=entry.data[CONF_FRAME_ID],
    )

    # Store the client in runtime_data
    entry.runtime_data = client

    return True


async def async_unload_entry(hass: HomeAssistant, entry: SkylightConfigEntry) -> bool:
    """Unload a config entry."""
    return True

