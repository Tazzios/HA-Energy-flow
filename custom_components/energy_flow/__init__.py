from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import EnergyFlowCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Energy Flow integration."""

    config = {
        **entry.data,
        **entry.options,
    }

    coordinator = EnergyFlowCoordinator(hass, config)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # ➜ BELANGRIJK: setup hook voor restore/state (als je die gebruikt)
    await coordinator._async_setup()

    # 1. eerst data laden
    await coordinator.async_config_entry_first_refresh()

    # 2. daarna pas entities maken
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload integration."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, ["sensor"]
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload integration."""

    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)