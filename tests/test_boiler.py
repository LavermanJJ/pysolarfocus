"""Tests for boiler component"""

from pysolarfocus import ApiVersions
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.boiler import Boiler
from pysolarfocus.const import DomesticHotWaterMode


def test_boiler_data_values():
    """Test data values for boiler component"""
    boiler = Boiler(api_version=ApiVersions.V_25_030)

    # Check basic attributes
    assert isinstance(boiler.temperature, DataValue)
    assert isinstance(boiler.state, DataValue)
    assert isinstance(boiler.mode, DataValue)
    assert isinstance(boiler.target_temperature, DataValue)
    assert isinstance(boiler.single_charge, DataValue)
    assert isinstance(boiler.holding_mode, DataValue)

    # Check addresses
    assert boiler.temperature.address == 0
    assert boiler.state.address == 1
    assert boiler.mode.address == 2
    assert boiler.target_temperature.address == 0
    assert boiler.single_charge.address == 1
    assert boiler.holding_mode.address == 2


def test_boiler_multiple_instances():
    """Test multiple boiler instances have correct offsets"""
    boiler1 = Boiler(input_address=500, api_version=ApiVersions.V_25_030)
    boiler2 = Boiler(input_address=520, api_version=ApiVersions.V_25_030)

    # Check offset between instances
    assert boiler2.temperature.address == boiler1.temperature.address
    assert boiler2.target_temperature.address == boiler1.target_temperature.address
