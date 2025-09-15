"""Custom types for immich_statistics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import ImmichStatisticsApiClient
    from .coordinator import ImmichStatisticsDataUpdateCoordinator


type ImmichStatisticsConfigEntry = ConfigEntry[ImmichStatisticsData]


@dataclass
class ImmichStatisticsData:
    """Data for the Immich Statistics integration."""

    client: ImmichStatisticsApiClient
    coordinator: ImmichStatisticsDataUpdateCoordinator
    integration: Integration
