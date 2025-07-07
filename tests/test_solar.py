"""Tests for solar component"""

from pysolarfocus import ApiVersions
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.solar import Solar


def test_solar_data_values():
    """Test data values for solar component"""
    solar = Solar(api_version=ApiVersions.V_25_030)

    # Check basic attributes
    assert isinstance(solar.collector_temperature_1, DataValue)
    assert isinstance(solar.collector_temperature_2, DataValue)
    assert isinstance(solar.collector_supply_temperature, DataValue)
    assert isinstance(solar.collector_return_temperature, DataValue)
    assert isinstance(solar.flow_heat_meter, DataValue)
    assert isinstance(solar.current_power, DataValue)
    assert isinstance(solar.current_yield_heat_meter, DataValue)
    assert isinstance(solar.today_yield, DataValue)
    assert isinstance(solar.buffer_sensor_1, DataValue)
    assert isinstance(solar.buffer_sensor_2, DataValue)
    assert isinstance(solar.buffer_sensor_3, DataValue)
    assert isinstance(solar.buffer_sensor_3, DataValue)

    assert isinstance(solar.relay_o1, DataValue)
    assert isinstance(solar.control_out_1, DataValue)
    assert isinstance(solar.relay_o2, DataValue)
    assert isinstance(solar.control_out_2, DataValue)

    # Check addresses
    assert solar.collector_temperature_1.address == 0
    assert solar.collector_temperature_2.address == 1
    assert solar.collector_supply_temperature.address == 2
    assert solar.collector_return_temperature.address == 3
    assert solar.flow_heat_meter.address == 4
    assert solar.current_power.address == 5
    assert solar.current_yield_heat_meter.address == 6
    assert solar.today_yield.address == 8
    assert solar.buffer_sensor_1.address == 10
    assert solar.buffer_sensor_2.address == 11
    assert solar.buffer_sensor_3.address == 12
    assert solar.state.address == 13
    assert solar.relay_o1.address == 14
    assert solar.control_out_1.address == 15
    assert solar.relay_o2.address == 16
    assert solar.control_out_2.address == 17


def test_solar_multiple_instances():
    """Test multiple solar instances have correct offsets"""
    solar1 = Solar(input_address=600, api_version=ApiVersions.V_25_030)
    solar2 = Solar(input_address=620, api_version=ApiVersions.V_25_030)

    # Check offset between instances
    assert solar2.collector_temperature_1.address == solar1.collector_temperature_1.address
    assert solar2.current_power.address == solar1.current_power.address
