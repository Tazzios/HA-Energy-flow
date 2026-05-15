from homeassistant.helpers import entity_registry as er
import logging

_LOGGER = logging.getLogger(__name__)

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
    SensorEntityDescription,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


SENSORS = {
    "solar_to_home": SensorEntityDescription(
        key="solar_to_home",
        translation_key="solar_to_home",
    ),
    "solar_to_grid": SensorEntityDescription(
        key="solar_to_grid",
        translation_key="solar_to_grid",
    ),
    "solar_to_battery": SensorEntityDescription(
        key="solar_to_battery",
        translation_key="solar_to_battery",
    ),
    "grid_to_battery": SensorEntityDescription(
        key="grid_to_battery",
        translation_key="grid_to_battery",
    ),
    "battery_to_home": SensorEntityDescription(
        key="battery_to_home",
        translation_key="battery_to_home",
    ),
    "battery_to_grid": SensorEntityDescription(
        key="battery_to_grid",
        translation_key="battery_to_grid",
    ),
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors for Energy Flow."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    keys = [
        "solar_to_home",
        "solar_to_grid",
        "solar_to_battery",
        "grid_to_battery",
        "battery_to_home",
        "battery_to_grid",
    ]

    entities = [
        EnergyFlowSensor(coordinator, SENSORS[key])
        for key in keys
    ]

    async_add_entities(entities)


class EnergyFlowSensor(CoordinatorEntity, SensorEntity):
    entity_description: SensorEntityDescription

    def __init__(self, coordinator, description):
        super().__init__(coordinator)

        self.entity_description = description
        self.key = description.key

        self._attr_unique_id = f"_{self.key}"

        self._attr_translation_key = self.key
        self._attr_has_entity_name = False
        self._attr_name = None

        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "kWh"

    @property
    def native_value(self):
        value = 0.0

        if self.coordinator.data:
            value = self.coordinator.data.get(self.key, 0)

        return value
