"""Tests for the configuration detector.

The fixtures are the register map of a real eco manager-touch on api version
26.020 - a vampair with one heating circuit, boiler, buffer, fresh water module,
circulation and differential module, and no solar - with the other systems built
by changing what that one says.
"""
import unittest.mock as mock
from unittest.mock import MagicMock

import pytest

from pysolarfocus import ApiVersions, Systems
from pysolarfocus.components.base.enums import RegisterTypes
from pysolarfocus.detector import SolarfocusDetector
from pysolarfocus.modbus_wrapper import ModbusConnector

INPUT = RegisterTypes.INPUT
HOLDING = RegisterTypes.HOLDING


class FakeController:
    """A controller that refuses the addresses it does not have.

    Single registers answer a read of one. A 32-bit register only answers a read
    of two, refusing a read of one exactly as a missing address does, which is
    the trap the detector has to get right.
    """

    def __init__(self, registers, dwords=None):
        self.registers = dict(registers)
        self.dwords = dict(dwords or {})
        self.reads = 0

    def probe_registers(self, address, register_type, count=1):
        self.reads += 1
        key = (register_type, address)
        if count == 1:
            return [self.registers[key]] if key in self.registers else None
        if key in self.dwords:
            value = self.dwords[key]
            return [value >> 16, value & 0xFFFF]
        following = (register_type, address + 1)
        if key in self.registers and following in self.registers:
            return [self.registers[key], self.registers[following]]
        return None

    def connect(self):
        return True

    @property
    def client(self):
        return MagicMock()


def vampair_26_020():
    """The register map read off the controller at 26.020."""
    registers = {}
    dwords = {}

    # Version markers, all present on a 26.020 controller.
    registers[(HOLDING, 33415)] = 0
    registers[(INPUT, 2420)] = 0
    registers[(INPUT, 802)] = 450
    registers[(HOLDING, 33412)] = 0
    registers[(HOLDING, 32958)] = 2
    registers[(INPUT, 2511)] = 0

    # Heating circuits: one enabled, seven reporting 7, "nicht freigeschaltet".
    for index in range(8):
        base = 1100 + 50 * index
        for offset in range(8):
            registers[(INPUT, base + offset)] = 0
        registers[(INPUT, base + 7)] = 0 if index == 0 else 7
    registers[(INPUT, 1100)] = 304

    # Boilers: one in Bereitschaft, three reporting 0, "nicht vorhanden".
    for index in range(4):
        base = 500 + 50 * index
        registers[(INPUT, base)] = 532 if index == 0 else 0
        registers[(INPUT, base + 1)] = 1 if index == 0 else 0
        registers[(INPUT, base + 2)] = 1 if index == 0 else 0

    # Buffers: one present, three reporting 0 with open sensors.
    for index in range(4):
        base = 1900 + 20 * index
        registers[(INPUT, base)] = 471 if index == 0 else 1300
        registers[(INPUT, base + 1)] = 350 if index == 0 else 1300
        registers[(INPUT, base + 3)] = 0
        registers[(INPUT, base + 4)] = 1 if index == 0 else 0
        registers[(INPUT, base + 5)] = 1
    registers[(INPUT, 1902)] = 2700  # only buffer 1 has an X35 sensor

    # Fresh water modules, circulations: one of each.
    for index in range(4):
        base = 700 + 25 * index
        registers[(INPUT, base)] = 1 if index == 0 else 0
        registers[(INPUT, base + 1)] = 419 if index == 0 else 0
        registers[(INPUT, 900 + 25 * index)] = 348 if index == 0 else 1300

    # Solar: mapped for all four circuits, lifeless on all four.
    for index in range(4):
        for offset in range(18):
            registers[(INPUT, 2100 + 20 * index + offset)] = 0

    # Differential modules: the first has live channels, the rest read zero.
    for index in range(4):
        for offset in range(10):
            registers[(INPUT, 2200 + 10 * index + offset)] = 0
    registers.update({(INPUT, 2201): 2700, (INPUT, 2202): 532, (INPUT, 2204): 382, (INPUT, 2205): 279})

    # Heat pump, running.
    registers.update({(INPUT, 2300): 382, (INPUT, 2301): 279, (INPUT, 2330): 5})

    # Biomass boiler: mapped, but nothing behind it.
    registers.update({(INPUT, 2400): 0, (INPUT, 2401): 6, (INPUT, 2409): 0, (INPUT, 2410): 1300, (INPUT, 2411): 1300, (INPUT, 2412): 0})
    dwords[(INPUT, 2402)] = 0
    dwords[(INPUT, 2416)] = 0

    dwords[(INPUT, 2500)] = 1734  # photovoltaic power

    return registers, dwords


def detect(registers, dwords):
    controller = FakeController(registers, dwords)
    return SolarfocusDetector("localhost", connector=controller).detect(), controller


def test_detects_a_vampair_installation():
    """The whole configuration, off the wire."""
    result, _ = detect(*vampair_26_020())

    assert result.api_version is ApiVersions.V_26_020
    assert result.system is Systems.VAMPAIR
    assert result.system_confident
    assert result.has_heatpump
    assert not result.has_biomassboiler
    assert result.has_photovoltaic
    assert result.heating_circuit_count == 1
    assert result.boiler_count == 1
    assert result.buffer_count == 1
    assert result.fresh_water_module_count == 1
    assert result.circulation_count == 1
    assert result.solar_count == 0
    # Never claimed - see test_a_differential_module_is_never_counted
    assert result.differential_module_count == 0


def test_result_builds_the_api_arguments():
    result, _ = detect(*vampair_26_020())
    assert result.as_api_kwargs() == {
        "system": Systems.VAMPAIR,
        "api_version": ApiVersions.V_26_020,
        "heating_circuit_count": 1,
        "buffer_count": 1,
        "boiler_count": 1,
        "fresh_water_module_count": 1,
        "circulation_count": 1,
        "differential_module_count": 0,
        "solar_count": 0,
    }


def test_evidence_carries_what_the_counts_were_read_from():
    """A user has to be able to see why a component was left out."""
    result, _ = detect(*vampair_26_020())

    assert result.evidence["heating_circuit_states"] == [0, 7, 7, 7, 7, 7, 7, 7]
    assert result.evidence["boiler_states"] == [1, 0, 0, 0]
    assert result.evidence["buffer_states"] == [1, 0, 0, 0]
    assert result.evidence["circulation_temperatures"] == [348, 1300, 1300, 1300]
    assert result.evidence["layout"]["heating_circuit_state_offset"] == 7
    assert result.evidence["layout"]["buffer_state_offset"] == 4
    assert result.evidence["layout"]["heat_pump"] == "25.030"


def test_detection_is_a_few_dozen_reads():
    """Cheap enough for a config flow, which is the whole point of doing it."""
    _, controller = detect(*vampair_26_020())
    assert controller.reads < 150


def test_a_32_bit_register_is_not_mistaken_for_a_missing_one():
    """The pellet counters refuse count=1; that must not read as no boiler."""
    registers, dwords = vampair_26_020()
    registers[(INPUT, 2400)] = 0
    dwords[(INPUT, 2416)] = 4200  # pellets burned

    result, _ = detect(registers, dwords)
    assert result.has_biomassboiler
    assert result.evidence["biomass_boiler"]["pellet_usage_total"] == 4200


def test_reads_the_older_register_layout():
    """Before 25.030 the heating circuit, buffer and heat pump blocks were shorter."""
    registers, dwords = vampair_26_020()
    for index in range(8):
        del registers[(INPUT, 1100 + 50 * index + 7)]
        registers[(INPUT, 1100 + 50 * index + 6)] = 0 if index == 0 else 7
    for index in range(4):
        del registers[(INPUT, 1900 + 20 * index + 5)]
        registers[(INPUT, 1900 + 20 * index + 3)] = 1 if index == 0 else 0
    del registers[(INPUT, 2330)]
    registers[(INPUT, 2326)] = 5

    result, _ = detect(registers, dwords)

    assert result.evidence["layout"] == {
        "heating_circuit_state_offset": 6,
        "buffer_state_offset": 3,
        "heat_pump": "legacy",
    }
    assert result.heating_circuit_count == 1
    assert result.buffer_count == 1
    assert result.has_heatpump


def test_therminator_status_marks_a_component_as_absent_too():
    """The therminator systems enumerate the same states from 200."""
    registers, dwords = vampair_26_020()
    registers[(INPUT, 501)] = 201  # boiler 1 in Bereitschaft
    for index in range(1, 4):
        registers[(INPUT, 500 + 50 * index + 1)] = 200  # "nicht freigeschaltet"
        registers[(INPUT, 1900 + 20 * index + 4)] = 200

    result, _ = detect(registers, dwords)
    assert result.boiler_count == 1
    assert result.buffer_count == 1


def biomass_only(registers):
    """Take the heat pump out, so that the boiler is the heat generator."""
    for address in (2300, 2301, 2330):
        registers[(INPUT, address)] = 0
    registers[(INPUT, 2400)] = 653  # boiler at 65.3 °C
    return registers


def test_therminator_identified_by_its_log_wood():
    registers, dwords = vampair_26_020()
    registers = biomass_only(registers)
    registers[(INPUT, 2409)] = 4  # a mode that does not itself imply logs
    registers[(INPUT, 2412)] = 1

    result, _ = detect(registers, dwords)
    assert result.has_biomassboiler
    assert not result.has_heatpump
    assert result.system is Systems.THERMINATOR


def test_octoplus_identified_by_its_buffer():
    registers, dwords = vampair_26_020()
    registers = biomass_only(registers)
    registers[(INPUT, 2410)] = 402
    registers[(INPUT, 2411)] = 551

    result, _ = detect(registers, dwords)
    assert result.system is Systems.OCTOPLUS


@pytest.mark.parametrize("operating_mode", [0, 4, 5])
def test_a_boiler_with_neither_is_an_ecotop(operating_mode):
    """Mode 0 means logs but is also what an unset register reads, so it is not evidence."""
    registers, dwords = vampair_26_020()
    registers = biomass_only(registers)
    registers[(INPUT, 2409)] = operating_mode

    result, _ = detect(registers, dwords)
    assert result.system is Systems.ECOTOP


@pytest.mark.parametrize("operating_mode", [1, 2, 3])
def test_a_log_burning_mode_is_a_therminator(operating_mode):
    registers, dwords = vampair_26_020()
    registers = biomass_only(registers)
    registers[(INPUT, 2409)] = operating_mode

    result, _ = detect(registers, dwords)
    assert result.system is Systems.THERMINATOR


def test_a_silent_controller_is_not_claimed_as_a_finding():
    """Nothing alive means the system is a default, and says so."""
    registers, dwords = vampair_26_020()
    for address in (2300, 2301, 2330, 2400):
        registers[(INPUT, address)] = 0

    result, _ = detect(registers, dwords)
    assert not result.has_heatpump
    assert not result.has_biomassboiler
    assert not result.system_confident


@pytest.mark.parametrize(
    "drop, expected",
    [
        ([(HOLDING, 33415)], ApiVersions.V_25_030),
        ([(HOLDING, 33415), (INPUT, 2230)], ApiVersions.V_23_080),
        ([(HOLDING, 33415), (INPUT, 2230), (INPUT, 2420), (INPUT, 802)], ApiVersions.V_23_020),
        (
            [(HOLDING, 33415), (INPUT, 2230), (INPUT, 2420), (INPUT, 802), (INPUT, 775), (HOLDING, 33412), (HOLDING, 32958), (INPUT, 2511)],
            ApiVersions.V_20_110,
        ),
    ],
)
def test_version_is_the_newest_marker_the_controller_has(drop, expected):
    registers, dwords = vampair_26_020()
    registers[(INPUT, 2230)] = 0  # differential module 4, the 25.030 marker
    for key in drop:
        registers.pop(key, None)

    result, _ = detect(registers, dwords)
    assert result.api_version is expected


def test_counts_are_dropped_when_the_version_cannot_address_them():
    """A register is mapped whether or not the library can read it over this version."""
    registers, dwords = vampair_26_020()
    for key in ((HOLDING, 33415), (INPUT, 2230), (INPUT, 2420), (INPUT, 802)):
        registers.pop(key, None)
    # A live circulation and two live solar circuits, over a version with neither.
    for index in range(4):
        registers[(INPUT, 900 + 25 * index)] = 348
    for index in range(2):
        registers[(INPUT, 2100 + 20 * index)] = 610

    result, _ = detect(registers, dwords)

    assert result.api_version is ApiVersions.V_23_020
    assert result.circulation_count == 0
    assert result.solar_count == 1


def test_probe_returns_none_when_the_controller_refuses():
    """The connector treats a refusal as an answer, not a failure."""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as client:
        instance = MagicMock()
        client.return_value = instance
        conn = ModbusConnector("localhost", 502, 1)

        refused = MagicMock()
        refused.isError.return_value = True
        instance.read_input_registers.return_value = refused
        assert conn.probe_registers(503, INPUT) is None

        answered = MagicMock()
        answered.isError.return_value = False
        answered.registers = [532]
        instance.read_input_registers.return_value = answered
        assert conn.probe_registers(500, INPUT) == [532]

        instance.read_holding_registers.return_value = answered
        assert conn.probe_registers(32000, HOLDING) == [532]


def test_probe_survives_a_broken_connection():
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as client:
        instance = MagicMock()
        client.return_value = instance
        instance.read_input_registers.side_effect = ConnectionError("gone")

        conn = ModbusConnector("localhost", 502, 1)
        assert conn.probe_registers(500, INPUT) is None


def test_a_differential_module_is_never_counted():
    """A live block is reported as evidence but not claimed as a module.

    Nothing in the registers separates a module wired to the same points as
    another component from the controller filling an unused block, and the one
    installation this could be checked against had no module configured while
    its block read as though it did.
    """
    registers, dwords = vampair_26_020()
    for offset in (1, 2, 4, 5):
        registers[(INPUT, 2210 + offset)] = 2700

    result, _ = detect(registers, dwords)
    assert result.differential_module_count == 0
    assert result.evidence["differential_modules"][0] == [2700, 532, 382, 279]
    assert result.evidence["differential_modules"][1] == [2700, 2700, 2700, 2700]


def test_a_solar_circuit_with_no_sensor_still_counts():
    registers, dwords = vampair_26_020()
    registers[(INPUT, 2120)] = 1300  # circuit 2, collector sensor open

    result, _ = detect(registers, dwords)
    assert result.solar_count == 1
