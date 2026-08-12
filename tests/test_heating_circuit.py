"""Tests for heating circuit component"""

from unittest.mock import MagicMock

from pysolarfocus import ApiVersions
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.heating_circuit import HeatingCircuit
from pysolarfocus.const import HeatingCircuitCooling, HeatingCircuitMode


def test_heating_circuit_data_values_v21():
    """Test data values for heating circuit with API version 21.140"""
    hc = HeatingCircuit(api_version=ApiVersions.V_21_140)

    # Basic attributes
    assert isinstance(hc.supply_temperature, DataValue)
    assert isinstance(hc.room_temperature, DataValue)
    assert isinstance(hc.humidity, DataValue)
    assert isinstance(hc.limit_thermostat, DataValue)
    assert isinstance(hc.circulator_pump, DataValue)
    assert isinstance(hc.mixer_valve, DataValue)
    assert isinstance(hc.state, DataValue)
    assert isinstance(hc.target_supply_temperature, DataValue)
    assert isinstance(hc.target_room_temperature, DataValue)

    # v21 specific addresses
    assert hc.supply_temperature.address == 0
    assert hc.room_temperature.address == 1
    assert hc.humidity.address == 2
    assert hc.limit_thermostat.address == 3
    assert hc.circulator_pump.address == 4
    assert hc.mixer_valve.address == 5
    assert hc.state.address == 6


def test_heating_circuit_data_values_v25():
    """Test data values for heating circuit with API version 25.030"""
    hc = HeatingCircuit(api_version=ApiVersions.V_25_030)

    # Additional v25 attributes
    assert isinstance(hc.mode, DataValue)
    assert isinstance(hc.cooling, DataValue)
    assert isinstance(hc.heating_mode, DataValue)
    assert hc.mode.address == 3
    assert hc.cooling.address == 2
    assert hc.heating_mode.address == 8


def test_heating_circuit_multiple_instances():
    """Test multiple heating circuit instances have correct offsets"""
    hc1 = HeatingCircuit(input_address=1100, api_version=ApiVersions.V_25_030)
    hc2 = HeatingCircuit(input_address=1120, api_version=ApiVersions.V_25_030)

    # Check offset between instances
    base_offset = 20
    assert hc2.supply_temperature.address == hc1.supply_temperature.address
    assert hc2.target_supply_temperature.address == hc1.target_supply_temperature.address


def test_heating_circuit_enums():
    """Test heating circuit enums"""
    assert HeatingCircuitMode.ALWAYS_ON.value == 0
    assert HeatingCircuitMode.REDUCED_OPERATION.value == 1
    assert HeatingCircuitMode.AUTOMATIC.value == 2
    assert HeatingCircuitMode.OFF.value == 3

    assert HeatingCircuitCooling.HEATING.value == 0
    assert HeatingCircuitCooling.COOLING.value == 1


def test_external_room_humidity_is_written_as_whole_percent():
    """Register 32607 has no scale factor, see registers.csv.

    The temperature registers around it are written as tenths (32606: 230 = 23.0
    degrees), and the humidity register was given the same multiplier by analogy.
    The controller then rejected every value above 10 percent, because 55 percent
    was sent as 550. See home-assistant-solarfocus issue #150.
    """
    modbus = MagicMock()
    modbus.write_register.return_value = True
    hc = HeatingCircuit(api_version=ApiVersions.V_26_020).initialize(modbus)

    hc.indoor_humidity_external.set_unscaled_value(55)
    hc.indoor_humidity_external.commit()

    modbus.write_register.assert_called_once_with(55, 32607)
    assert hc.indoor_humidity_external.scaled_value == 55


def test_external_room_temperature_stays_in_tenths():
    """The neighbouring register does have a scale factor (32606: 230 = 23.0)."""
    modbus = MagicMock()
    modbus.write_register.return_value = True
    hc = HeatingCircuit(api_version=ApiVersions.V_26_020).initialize(modbus)

    hc.indoor_temperature_external.set_unscaled_value(23)
    hc.indoor_temperature_external.commit()

    modbus.write_register.assert_called_once_with(230, 32606)
    assert hc.indoor_temperature_external.scaled_value == 23
