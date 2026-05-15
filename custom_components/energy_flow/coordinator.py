
import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)


class EnergyFlowCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config):
        super().__init__(
            hass,
            logger=_LOGGER,
            name="energy_flow",
            update_interval=timedelta(minutes=1),
        )

        self.hass = hass
        self.config = config
        self.store = Store(hass, version=1, key="energy_flow_storage")

        self._last_snapshot = {}

    async def _async_setup(self):
        data = await self.store.async_load()
        if data:
            self._last_snapshot = data.get("last_snapshot", {})

    def _normalize(self, value):
        if not value:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return value
        return []

    def _get_snapshot(self, entity_ids):
        snapshot = {}

        for entity_id in entity_ids:
            state = self.hass.states.get(entity_id)

            if state is None:
                _LOGGER.debug("Missing entity state: %s", entity_id)
                snapshot[entity_id] = 0.0
                continue

            try:
                snapshot[entity_id] = float(state.state)
            except (ValueError, TypeError):
                _LOGGER.warning("Invalid state for %s: %s", entity_id, state.state)
                snapshot[entity_id] = 0.0

        return snapshot

    def _delta(self, current, last):
        total = 0.0

        for key, value in current.items():
            prev = last.get(key)
            if prev is None:
                continue

            change = value - prev
            if change > 0:
                total += change

        return total

    async def _save(self):
        await self.store.async_save(
            {"last_snapshot": self._last_snapshot}
        )

    async def _async_update_data(self):

        solar_ids = self._normalize(self.config.get("solar_production", []))
        export_ids = self._normalize(self.config.get("grid_export", []))
        charge_ids = self._normalize(self.config.get("battery_charge", []))
        discharge_ids = self._normalize(self.config.get("battery_discharge", []))

        all_ids = solar_ids + export_ids + charge_ids + discharge_ids

        current = self._get_snapshot(all_ids)

        if not self._last_snapshot:
            self._last_snapshot = current.copy()
            return self._empty()

        solar = self._delta(
            {k: current.get(k, 0) for k in solar_ids},
            {k: self._last_snapshot.get(k, 0) for k in solar_ids},
        )

        export = self._delta(
            {k: current.get(k, 0) for k in export_ids},
            {k: self._last_snapshot.get(k, 0) for k in export_ids},
        )

        charge = self._delta(
            {k: current.get(k, 0) for k in charge_ids},
            {k: self._last_snapshot.get(k, 0) for k in charge_ids},
        )

        discharge = self._delta(
            {k: current.get(k, 0) for k in discharge_ids},
            {k: self._last_snapshot.get(k, 0) for k in discharge_ids},
        )

        self._last_snapshot = current.copy()

        result = self._calculate_flows(
            solar, export, charge, discharge
        )

        await self._save()

        _LOGGER.warning("RESULT=%s", result)

        return result

    def _empty(self):
        return {
            "solar_to_home": 0,
            "solar_to_grid": 0,
            "solar_to_battery": 0,
            "grid_to_battery": 0,
            "battery_to_home": 0,
            "battery_to_grid": 0,
        }

    def _calculate_flows(self, solar, export, charge, discharge):

        # batterij -> net eerst afboeken op export
        battery_to_grid = min(discharge, export)

        solar_to_grid = max(export - battery_to_grid, 0)

        solar_available = max(solar - solar_to_grid, 0)

        solar_to_battery = min(charge, solar_available)

        solar_to_home = max(
            solar - solar_to_grid - solar_to_battery,
            0
        )

        battery_to_home = max(
            discharge - battery_to_grid,
            0
        )

        grid_to_battery = max(
            charge - solar_to_battery,
            0
        )

        return {
            "solar_to_home": solar_to_home,
            "solar_to_grid": solar_to_grid,
            "solar_to_battery": solar_to_battery,
            "grid_to_battery": grid_to_battery,
            "battery_to_home": battery_to_home,
            "battery_to_grid": battery_to_grid,
        }