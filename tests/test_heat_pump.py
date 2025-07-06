"""Tests for heat pump component"""

from pysolarfocus import ApiVersions
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.heat_pump import HeatPump


def test_heat_pump_data_values_v21():
    """Test data values for API version 21.140"""
    hp = HeatPump(api_version=ApiVersions.V_21_140)

    # Common attributes for all versions
    assert isinstance(hp.supply_temperature, DataValue)
    assert isinstance(hp.return_temperature, DataValue)
    assert isinstance(hp.flow_rate, DataValue)
    assert isinstance(hp.compressor_speed, DataValue)
    assert isinstance(hp.evu_lock_active, DataValue)

    # Version specific addresses
    assert hp.defrost_active.address == 5
    assert hp.boiler_charge.address == 6
    assert hp.thermal_energy_total.address == 7
    assert hp.thermal_energy_drinking_water.address == 9
    assert hp.thermal_energy_heating.address == 11
    assert hp.electrical_energy_total.address == 13
    assert hp.electrical_power.address == 19
    assert hp.vampair_state.address == 26


def test_heat_pump_data_values_v25():
    """Test data values for API version 25.030"""
    hp = HeatPump(api_version=ApiVersions.V_25_030)

    # Version specific addresses
    assert hp.defrost_active.address == 6
    assert hp.boiler_charge.address == 7
    assert hp.thermal_energy_total.address == 10
    assert hp.thermal_energy_drinking_water.address == 12
    assert hp.thermal_energy_heating.address == 14
    assert hp.electrical_energy_total.address == 16
    assert hp.electrical_power.address == 22
    assert hp.vampair_state.address == 30

    # Performance calculators should be present
    assert hp.cop_heating is not None
    assert hp.cop_cooling is not None
    assert hp.performance_overall is not None
    assert hp.performance_overall_heating is not None
    assert hp.performance_overall_drinking_water is not None
