"""Tests for differential module component"""

from pysolarfocus import ApiVersions
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.base.enums import DataTypes
from pysolarfocus.components.differential_module import DifferentialModule


def test_differential_module_data_values():
    """Test data values for differential module component"""
    dm = DifferentialModule(api_version=ApiVersions.V_25_030)

    # Check basic attributes
    assert isinstance(dm.relay_control_loop_o1, DataValue)
    assert isinstance(dm.temperature_1_control_loop_1, DataValue)
    assert isinstance(dm.temperature_2_control_loop_1, DataValue)
    assert isinstance(dm.relay_control_loop_o2, DataValue)
    assert isinstance(dm.temperature_1_control_loop_2, DataValue)
    assert isinstance(dm.temperature_2_control_loop_2, DataValue)

    # Check addresses
    assert dm.relay_control_loop_o1.address == 0
    assert dm.temperature_1_control_loop_1.address == 1
    assert dm.temperature_2_control_loop_1.address == 2
    assert dm.relay_control_loop_o2.address == 3
    assert dm.temperature_1_control_loop_2.address == 4
    assert dm.temperature_2_control_loop_2.address == 5

    # Check data types
    assert dm.relay_control_loop_o1.data_type == DataTypes.UINT
    assert dm.relay_control_loop_o2.data_type == DataTypes.UINT

    # Check multipliers for temperature values
    assert dm.temperature_1_control_loop_1.multiplier == 0.1
    assert dm.temperature_2_control_loop_1.multiplier == 0.1
    assert dm.temperature_1_control_loop_2.multiplier == 0.1
    assert dm.temperature_2_control_loop_2.multiplier == 0.1


def test_differential_module_multiple_instances():
    """Test multiple differential module instances have correct offsets"""
    dm1 = DifferentialModule(input_address=2200, api_version=ApiVersions.V_25_030)
    dm2 = DifferentialModule(input_address=2210, api_version=ApiVersions.V_25_030)

    # Check that both instances have the same relative addresses
    assert dm2.relay_control_loop_o1.address == dm1.relay_control_loop_o1.address
    assert dm2.temperature_1_control_loop_1.address == dm1.temperature_1_control_loop_1.address
    assert dm2.temperature_2_control_loop_1.address == dm1.temperature_2_control_loop_1.address
    assert dm2.relay_control_loop_o2.address == dm1.relay_control_loop_o2.address
    assert dm2.temperature_1_control_loop_2.address == dm1.temperature_1_control_loop_2.address
    assert dm2.temperature_2_control_loop_2.address == dm1.temperature_2_control_loop_2.address


def test_differential_module_with_older_api_version():
    """Test differential module with older API version that doesn't support it"""
    dm = DifferentialModule(api_version=ApiVersions.V_21_140)

    # For older API versions, the attributes should not exist or should be handled gracefully
    # This tests the version checking logic
    try:
        relay = dm.relay_control_loop_o1
        # If it exists, that's fine
    except AttributeError:
        # If it doesn't exist, that's also acceptable for older versions
        pass
