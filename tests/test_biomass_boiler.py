"""Tests for biomass boiler component"""

from pysolarfocus import ApiVersions
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.biomass_boiler import BiomassBoiler


def test_biomass_boiler_data_values():
    """Test data values for biomass boiler component"""
    bb = BiomassBoiler(api_version=ApiVersions.V_25_030)

    # Check basic attributes
    assert isinstance(bb.temperature, DataValue)
    assert isinstance(bb.status, DataValue)
    assert isinstance(bb.time_of_operation_at_maintenance, DataValue)
    assert isinstance(bb.message_number, DataValue)
    assert isinstance(bb.door_contact, DataValue)
    assert isinstance(bb.cleaning, DataValue)
    assert isinstance(bb.ash_container, DataValue)
    assert isinstance(bb.outdoor_temperature, DataValue)
    assert isinstance(bb.boiler_operating_mode, DataValue)
    assert isinstance(bb.octoplus_buffer_temperature_bottom, DataValue)
    assert isinstance(bb.octoplus_buffer_temperature_top, DataValue)

    # Check addresses
    assert bb.temperature.address == 0
    assert bb.status.address == 1
    assert bb.time_of_operation_at_maintenance.address == 2
    assert bb.message_number.address == 4
    assert bb.door_contact.address == 5
    assert bb.cleaning.address == 6
    assert bb.ash_container.address == 7
    assert bb.outdoor_temperature.address == 8
    assert bb.boiler_operating_mode.address == 9
    assert bb.octoplus_buffer_temperature_bottom.address == 10
    assert bb.octoplus_buffer_temperature_top.address == 11
