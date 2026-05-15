import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    CONF_SOLAR,
    CONF_EXPORT,
    CONF_BATTERY_CHARGE,
    CONF_BATTERY_DISCHARGE,
)


class EnergyFlowOptionsFlow(config_entries.OptionsFlowWithConfigEntry):

    async def async_step_init(self, user_input=None):

        entry = self.config_entry

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        def _get(key):
            return entry.options.get(key) or entry.data.get(key)

        schema = vol.Schema({
            vol.Required(CONF_SOLAR, default=_get(CONF_SOLAR)):
                selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", device_class="energy", multiple=True)
                ),

            vol.Required(CONF_EXPORT, default=_get(CONF_EXPORT)):
                selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", device_class="energy", multiple=False)
                ),

            vol.Required(CONF_BATTERY_CHARGE, default=_get(CONF_BATTERY_CHARGE)):
                selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", device_class="energy", multiple=True)
                ),

            vol.Required(CONF_BATTERY_DISCHARGE, default=_get(CONF_BATTERY_DISCHARGE)):
                selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", device_class="energy", multiple=True)
                ),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )