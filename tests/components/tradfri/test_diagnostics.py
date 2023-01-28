"""Tests for Tradfri diagnostics."""
from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock, Mock

from aiohttp import ClientSession
import pytest
from pytradfri.device import Device
from pytradfri.device.air_purifier import AirPurifier

from homeassistant.components.tradfri.const import DOMAIN
from homeassistant.core import HomeAssistant

from .common import setup_integration

from tests.common import load_fixture
from tests.components.diagnostics import get_diagnostics_for_config_entry


@pytest.fixture(scope="module")
def air_purifier_response() -> dict[str, Any]:
    """Return an air purifier response."""
    return json.loads(load_fixture("air_purifier.json", DOMAIN))


@pytest.fixture
def air_purifier(air_purifier_response) -> AirPurifier:
    """Return air purifier."""
    device = Device(air_purifier_response)
    air_purifier_control = device.air_purifier_control
    assert air_purifier_control
    return air_purifier_control.air_purifiers[0]


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
