"""Tests for biomass boiler component"""
from contextlib import contextmanager
import unittest.mock as mock
from unittest.mock import MagicMock

from pysolarfocus import ApiVersions, Systems
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.biomass_boiler import BiomassBoiler
from pysolarfocus.modbus_wrapper import ModbusConnector


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


@contextmanager
def modbus_answering_with_zeros():
    """A connector whose server answers every read with the registers asked for."""

    def answer(address, count, **kwargs):
        response = MagicMock()
        response.isError.return_value = False
        response.registers = [0] * count
        return response

    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as client:
        client.return_value.is_socket_open.return_value = True
        client.return_value.read_input_registers.side_effect = answer
        client.return_value.read_holding_registers.side_effect = answer
        yield ModbusConnector("localhost", 502, 1)


def test_ecotop_reads_its_single_holding_register():
    """The Ecotop has one holding register, and it is not the first of the range.

    Reading from the start of the component instead of the start of the slice
    asked the controller for seven registers rather than one, and the answer was
    too long to be parsed - the whole boiler was reported as unreadable.
    """
    boiler = BiomassBoiler(api_version=ApiVersions.V_25_030, system=Systems.ECOTOP)

    with modbus_answering_with_zeros() as modbus:
        boiler.initialize(modbus)

        assert [(s.absolute_address, s.count) for s in boiler.holding_slices] == [(33406, 1)]
        assert boiler.update() is True


def test_the_sweep_registers_are_read_on_their_own():
    """Before 23.010 the holding registers start at the sweep function."""
    boiler = BiomassBoiler(api_version=ApiVersions.V_22_090, system=Systems.PELLETELEGANCE)

    with modbus_answering_with_zeros() as modbus:
        boiler.initialize(modbus)

        assert [(s.absolute_address, s.count) for s in boiler.holding_slices] == [(33410, 2)]
        assert boiler.update() is True
