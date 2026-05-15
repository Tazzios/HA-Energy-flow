import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_SOLAR,
    CONF_EXPORT,
    CONF_BATTERY_CHARGE,
    CONF_BATTERY_DISCHARGE,
)


class EnergyFlowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):

        if user_input is not None:
            return self.async_create_entry(title="Energy Flow", data=user_input)

        schema = vol.Schema({
            vol.Optional(CONF_SOLAR): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="energy", multiple=True)
            ),
            vol.Required(CONF_EXPORT): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="energy", multiple=False)
            ),
            vol.Optional(CONF_BATTERY_CHARGE): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="energy", multiple=True)
            ),
            vol.Optional(CONF_BATTERY_DISCHARGE): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", device_class="energy", multiple=True)
            ),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        from .options_flow import EnergyFlowOptionsFlow
        return EnergyFlowOptionsFlow(config_entry)