"""Config flow for Skylight integration."""

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .client import SkylightAuthError, SkylightClient, SkylightConnectionError
from .const import CONF_FRAME_ID, DOMAIN, LOGGER

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_FRAME_ID): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> None:
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    session = async_get_clientsession(hass)
    client = SkylightClient(
        session,
        data[CONF_USERNAME],
        data[CONF_PASSWORD],
        data[CONF_FRAME_ID],
    )

    try:
        await client.async_login()
    except SkylightAuthError as err:
        LOGGER.error("Authentication failed: %s", err)
        raise InvalidAuth from err
    except SkylightConnectionError as err:
        LOGGER.error("Connection failed: %s", err)
        raise CannotConnect from err


class SkylightConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Skylight."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_USERNAME]}_{user_input[CONF_FRAME_ID]}"
            )
            self._abort_if_unique_id_configured()

            try:
                await validate_input(self.hass, user_input)
                return self.async_create_entry(
                    title=f"Skylight ({user_input[CONF_FRAME_ID]})",
                    data=user_input,
                )
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

