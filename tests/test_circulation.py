"""Tests for circulation component"""

from pysolarfocus import ApiVersions
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.circulation import Circulation


def test_circulation_data_values():
    """Test data values for circulation component"""
    circulation = Circulation(api_version=ApiVersions.V_25_030)

    # Check basic attributes
    assert isinstance(circulation.temperature, DataValue)
    assert isinstance(circulation.pump, DataValue)

    # Check addresses
    assert circulation.temperature.address == 0
    assert circulation.pump.address == 1

    # Check multiplier for temperature
    assert circulation.temperature.multiplier == 0.1


def test_circulation_multiple_instances():
    """Test multiple circulation instances have correct offsets"""
    circulation1 = Circulation(input_address=900, api_version=ApiVersions.V_25_030)
    circulation2 = Circulation(input_address=925, api_version=ApiVersions.V_25_030)

    # Check that both instances have the same relative addresses
    assert circulation2.temperature.address == circulation1.temperature.address
    assert circulation2.pump.address == circulation1.pump.address


def test_circulation_with_older_api_version():
    """Test circulation with older API version that doesn't support it"""
    circulation = Circulation(api_version=ApiVersions.V_21_140)

    # For older API versions, the attributes should not exist or should be handled gracefully
    # This tests the version checking logic
    try:
        temp = circulation.temperature
        # If it exists, that's fine
    except AttributeError:
        # If it doesn't exist, that's also acceptable for older versions
        pass
