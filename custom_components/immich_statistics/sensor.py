"""Sensor platform for immich_statistics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import EntityCategory, UnitOfInformation
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from .entity import ImmichStatisticsEntity

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import StateType

    from .coordinator import ImmichStatisticsDataUpdateCoordinator
    from .data import ImmichStatisticsConfigEntry


@dataclass(frozen=True, kw_only=True)
class ImmichStatisticsSensorEntityDescription(SensorEntityDescription):
    """Describes GitHub issue sensor entity."""

    value_fn: Callable[[dict[str, Any]], StateType]

    attr_fn: Callable[[dict[str, Any]], Mapping[str, Any] | None] = lambda data: None  # noqa: ARG005
    avabl_fn: Callable[[dict[str, Any]], bool] = lambda data: True  # noqa: ARG005


ENTITY_DESCRIPTIONS = (
    ImmichStatisticsSensorEntityDescription(
        key="photos_count",
        name="Immich Photos",
        icon="mdi:image",
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("photos"),
        avabl_fn=lambda data: "photos" in data,
    ),
    ImmichStatisticsSensorEntityDescription(
        key="videos_count",
        name="Immich Videos",
        icon="mdi:video-image",
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("videos"),
        avabl_fn=lambda data: "videos" in data,
    ),
    ImmichStatisticsSensorEntityDescription(
        key="storage_usage",
        name="Immich Storage Usage",
        icon="mdi:database",
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
        suggested_display_precision=2,
        value_fn=lambda data: data.get("usage"),
        avabl_fn=lambda data: "usage" in data,
    ),
    ImmichStatisticsSensorEntityDescription(
        key="storage_usage_photos",
        name="Immich Photos Storage Usage",
        icon="mdi:database",
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
        suggested_display_precision=2,
        value_fn=lambda data: data.get("usagePhotos"),
        avabl_fn=lambda data: "usagePhotos" in data,
    ),
    ImmichStatisticsSensorEntityDescription(
        key="storage_usage_videos",
        name="Immich Videos Storage Usage",
        icon="mdi:database",
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
        suggested_display_precision=2,
        value_fn=lambda data: data.get("usageVideos"),
        avabl_fn=lambda data: "usageVideos" in data,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: ImmichStatisticsConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        ImmichStatisticsSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class ImmichStatisticsSensor(ImmichStatisticsEntity, SensorEntity):
    """immich_statistics Sensor class."""

    entity_description: ImmichStatisticsSensorEntityDescription

    def __init__(
        self,
        coordinator: ImmichStatisticsDataUpdateCoordinator,
        entity_description: ImmichStatisticsSensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"immich_statistics_{entity_description.key}"

        self._attr_device_info = DeviceInfo(
            name="Immich Statistics",
            manufacturer="Immich",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.coordinator.data is not None
            and self.entity_description.avabl_fn(self.coordinator.data)
        )

    @property
    def native_value(self) -> StateType:
        """Return the native value of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)
