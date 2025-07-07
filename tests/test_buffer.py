"""Tests for buffer component"""

from pysolarfocus import ApiVersions
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.buffer import Buffer


def test_buffer_data_values():
    """Test data values for buffer component"""
    buffer = Buffer(api_version=ApiVersions.V_25_030)

    # Check basic attributes
    assert isinstance(buffer.top_temperature, DataValue)
    assert isinstance(buffer.bottom_temperature, DataValue)
    assert isinstance(buffer.external_top_temperature_x44, DataValue)
    assert isinstance(buffer.external_middle_temperature_x36, DataValue)
    assert isinstance(buffer.external_bottom_temperature_x35, DataValue)

    # Check addresses
    assert buffer.top_temperature.address == 0
    assert buffer.bottom_temperature.address == 1
    assert buffer.external_top_temperature_x44.address == 0
    assert buffer.external_middle_temperature_x36.address == 1
    assert buffer.external_bottom_temperature_x35.address == 2


def test_buffer_multiple_instances():
    """Test multiple buffer instances have correct offsets"""
    buffer1 = Buffer(input_address=400, api_version=ApiVersions.V_25_030)
    buffer2 = Buffer(input_address=420, api_version=ApiVersions.V_25_030)

    # Check offset between instances
    assert buffer2.top_temperature.address == buffer1.top_temperature.address
    assert buffer2.bottom_temperature.address == buffer1.bottom_temperature.address
