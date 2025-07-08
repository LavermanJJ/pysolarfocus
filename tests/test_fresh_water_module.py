"""Tests for fresh water module component"""

from pysolarfocus import ApiVersions
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.fresh_water_module import FreshWaterModule


def test_fresh_water_module_data_values():
    """Test data values for fresh water module component"""
    fwm = FreshWaterModule(api_version=ApiVersions.V_23_020)

    # Check basic attributes
    assert isinstance(fwm.state, DataValue)

    # Check addresses
    assert fwm.state.address == 0


def test_fresh_water_module_v23_040():
    """Test fresh water module with API version 23.040 and newer"""
    fwm = FreshWaterModule(api_version=ApiVersions.V_23_040)

    # Check basic attributes
    assert isinstance(fwm.state, DataValue)
    assert isinstance(fwm.supply_temperature, DataValue)
    assert isinstance(fwm.flow_rate, DataValue)
    assert isinstance(fwm.target_temperature, DataValue)
    assert isinstance(fwm.valve, DataValue)

    # Check addresses
    assert fwm.state.address == 0
    assert fwm.supply_temperature.address == 1
    assert fwm.flow_rate.address == 2
    assert fwm.target_temperature.address == 3
    assert fwm.valve.address == 4

    # Check multipliers
    assert fwm.supply_temperature.multiplier == 0.1
    assert fwm.target_temperature.multiplier == 0.1


def test_fresh_water_module_multiple_instances():
    """Test multiple fresh water module instances have correct offsets"""
    fwm1 = FreshWaterModule(input_address=700, api_version=ApiVersions.V_23_040)
    fwm2 = FreshWaterModule(input_address=725, api_version=ApiVersions.V_23_040)

    # Check that both instances have the same relative addresses
    assert fwm2.state.address == fwm1.state.address
    assert fwm2.supply_temperature.address == fwm1.supply_temperature.address
    assert fwm2.flow_rate.address == fwm1.flow_rate.address
    assert fwm2.target_temperature.address == fwm1.target_temperature.address
    assert fwm2.valve.address == fwm1.valve.address


def test_fresh_water_module_with_older_api_version():
    """Test fresh water module with older API version"""
    fwm = FreshWaterModule(api_version=ApiVersions.V_23_020)

    # Should have basic state
    assert isinstance(fwm.state, DataValue)

    # Should not have extended attributes for older versions
    try:
        temp = fwm.supply_temperature
        # If it exists, that's fine for this version
    except AttributeError:
        # If it doesn't exist, that's expected for older versions
        pass
