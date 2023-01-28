"""Tests for Tradfri diagnostics."""
from __future__ import annotations

from unittest.mock import MagicMock, Mock

from aiohttp import ClientSession
from pytradfri.device.air_purifier import AirPurifier

from homeassistant.core import HomeAssistant

from .common import setup_integration

from tests.components.diagnostics import get_diagnostics_for_config_entry


async def test_diagnostics(
    hass: HomeAssistant,
    hass_client: ClientSession,
    mock_gateway: Mock,
    mock_api_factory: MagicMock,
    air_purifier: AirPurifier,
) -> None:
    """Test diagnostics for config entry."""
    device = air_purifier.device
    mock_gateway.mock_devices.append(device)
    config_entry = await setup_integration(hass)

    result = await get_diagnostics_for_config_entry(hass, hass_client, config_entry)

    assert isinstance(result, dict)
    assert result["gateway_version"] == "1.2.1234"
    assert len(result["device_data"]) == 1
    assert result["device_data"][0] == "STARKVIND Air purifier"
