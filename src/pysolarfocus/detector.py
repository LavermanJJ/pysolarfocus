"""Work out what an eco manager-touch installation looks like, by asking it.

There is no register listing the installed components, so this reads two
different things off the controller:

* **Which registers exist.** An address the firmware does not map is refused
  with illegal data address, so probing establishes the register set - the api
  version, and the layout of the components whose registers moved between
  versions. It says next to nothing about installed components: on a 26.020
  controller every documented register was mapped bar the X35 buffer sensors of
  the buffers that are not there.
* **What the registers say.** The specification defines "nicht vorhanden" and
  "nicht freigeschaltet" values for the components that repeat, and an
  unconfigured sensor channel reports a temperature far outside its range. That
  is what the counts are taken from.

The result carries the evidence it was reached from, because a heating system
this is wrong about is one whose owner has to be able to see why.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import PORT, ApiVersions, Systems
from .components.base.enums import RegisterTypes
from .const import SLAVE_ID
from .modbus_wrapper import ModbusConnector

# What an unconfigured or open sensor channel reports instead of a temperature:
# 130.0 °C, 270.0 °C, and -1 read as unsigned.
NO_SENSOR = frozenset({1300, 2700, 65535})

# Heating circuit status 7 is "Heizkreis nicht freigeschaltet".
HEATING_CIRCUIT_DISABLED = 7

# Boiler status 0 is "Boilerstatus nicht vorhanden" and buffer status 0 is
# "Status nicht vorhanden". The therminator systems enumerate the same states
# from 200, where the first is again the one meaning the component is not there.
NOT_PRESENT = frozenset({0, 200})

# Registers a version introduced, each picked to be there whatever the
# installation looks like - the fourth instance of a component, or a setting -
# so that the version they date the controller to does not depend on what is
# plugged into it. Highest first: the first one the controller has wins.
#
# 25.020 and 25.030 added their registers together, so a controller on 25.020
# is reported as 25.030. The layout that distinction is wanted for is probed
# directly rather than derived from the version, so this costs nothing here.
VERSION_MARKERS: List[tuple] = [
    (ApiVersions.V_26_020, RegisterTypes.HOLDING, 33415),  # HEMS target electrical power
    (ApiVersions.V_25_030, RegisterTypes.INPUT, 2230),  # differential module 4
    (ApiVersions.V_23_080, RegisterTypes.INPUT, 2420),  # sweep almost done
    (ApiVersions.V_23_040, RegisterTypes.INPUT, 802),  # fresh water cascade target temperature
    (ApiVersions.V_23_020, RegisterTypes.INPUT, 775),  # fresh water module 4 status
    (ApiVersions.V_23_010, RegisterTypes.HOLDING, 33412),  # pellet store refilled
    (ApiVersions.V_22_090, RegisterTypes.HOLDING, 32958),  # heating circuit 8 heating mode
    (ApiVersions.V_21_140, RegisterTypes.INPUT, 2511),  # pv overcharge active
]

# Base addresses and strides of the components that repeat.
HEATING_CIRCUIT_BASE, HEATING_CIRCUIT_STRIDE, HEATING_CIRCUIT_MAX = 1100, 50, 8
BOILER_BASE, BOILER_STRIDE, BOILER_MAX = 500, 50, 4
BUFFER_BASE, BUFFER_STRIDE, BUFFER_MAX = 1900, 20, 4
FRESH_WATER_BASE, FRESH_WATER_STRIDE, FRESH_WATER_MAX = 700, 25, 4
CIRCULATION_BASE, CIRCULATION_STRIDE, CIRCULATION_MAX = 900, 25, 4
SOLAR_BASE, SOLAR_STRIDE, SOLAR_MAX = 2100, 20, 4
DIFFERENTIAL_BASE, DIFFERENTIAL_STRIDE, DIFFERENTIAL_MAX = 2200, 10, 4


@dataclass
class DetectionResult:
    """What one controller says it is, and what it was read off."""

    api_version: ApiVersions
    system: Systems
    heating_circuit_count: int
    buffer_count: int
    boiler_count: int
    fresh_water_module_count: int
    circulation_count: int
    differential_module_count: int
    solar_count: int
    has_heatpump: bool
    has_biomassboiler: bool
    has_photovoltaic: bool
    evidence: Dict[str, Any] = field(default_factory=dict)

    @property
    def system_confident(self) -> bool:
        """Whether the heat generator identified itself.

        False when neither the heat pump nor a biomass boiler reported anything
        alive, in which case `system` is the default rather than a finding.
        """
        return self.has_heatpump or self.has_biomassboiler

    def as_api_kwargs(self) -> Dict[str, Any]:
        """The arguments to build a `SolarfocusAPI` for this installation."""
        return {
            "system": self.system,
            "api_version": self.api_version,
            "heating_circuit_count": self.heating_circuit_count,
            "buffer_count": self.buffer_count,
            "boiler_count": self.boiler_count,
            "fresh_water_module_count": self.fresh_water_module_count,
            "circulation_count": self.circulation_count,
            "differential_module_count": self.differential_module_count,
            "solar_count": self.solar_count,
        }


class SolarfocusDetector:
    """Reads an installation's shape off the controller.

    Costs somewhere around ninety single-register reads, which is a few seconds
    on the controllers this was written against - fine once, when a user is
    setting the integration up, and not something to do on every update.
    """

    def __init__(self, ip: str, port: int = PORT, slave_id: int = SLAVE_ID, connector: Optional[ModbusConnector] = None) -> None:
        """Initialize the detector.

        Args:
            ip: IP address of the controller
            port: Port number for modbus communication
            slave_id: Slave ID for modbus communication
            connector: An existing connector to probe through, for a caller that
                is already connected
        """
        self.__conn = connector if connector is not None else ModbusConnector(ip, port, slave_id)

    def connect(self) -> bool:
        """Connect to the controller."""
        return self.__conn.connect()

    def close(self) -> None:
        """Drop the connection, for a caller that only wanted to detect."""
        self.__conn.client.close()

    def __exists(self, register_type: RegisterTypes, address: int) -> bool:
        """Whether the firmware maps this address.

        A 32-bit register refuses a single-register read the same way a missing
        address does, so an address counts as absent only once it has refused
        both of its registers as well.
        """
        if self.__conn.probe_registers(address, register_type) is not None:
            return True
        return self.__conn.probe_registers(address, register_type, count=2) is not None

    def __value(self, address: int, register_type: RegisterTypes = RegisterTypes.INPUT) -> Optional[int]:
        """The value of a single register, or None if the controller refused it."""
        registers = self.__conn.probe_registers(address, register_type)
        return None if registers is None else registers[0]

    def __dword(self, address: int, register_type: RegisterTypes = RegisterTypes.INPUT) -> Optional[int]:
        """The value of a 32-bit register, or None if the controller refused it."""
        registers = self.__conn.probe_registers(address, register_type, count=2)
        return None if registers is None else (registers[0] << 16) + registers[1]

    @staticmethod
    def __live(value: Optional[int]) -> bool:
        """Whether a register is reporting a measurement rather than an empty channel."""
        return value is not None and value != 0 and value not in NO_SENSOR

    @staticmethod
    def __configured(value: Optional[int]) -> bool:
        """Whether a channel exists at all, sensor on it or not.

        Weaker than `__live`, for the components with no state register to ask.
        A configured channel whose sensor is missing reports one of the
        out-of-range temperatures rather than zero, so the sentinel is evidence
        that the component is there - only a flat zero says it is not.
        """
        return value is not None and value != 0

    def detect(self) -> DetectionResult:
        """Probe the controller and work out what is on it."""
        evidence: Dict[str, Any] = {}

        api_version = next(
            (version for version, register_type, address in VERSION_MARKERS if self.__exists(register_type, address)),
            ApiVersions.V_20_110,
        )
        evidence["api_version_marker"] = api_version.value

        # Where the state registers of the repeated components sit. The library
        # derives these from the system and the version together - a therminator
        # heating circuit is laid out like a 25.030 one - but the controller can
        # simply be asked how far its blocks reach, which is both shorter and
        # right for a combination nobody has tried yet.
        heating_circuit_state_offset = 7 if self.__exists(RegisterTypes.INPUT, HEATING_CIRCUIT_BASE + 7) else 6
        buffer_state_offset = 4 if self.__exists(RegisterTypes.INPUT, BUFFER_BASE + 5) else 3
        heat_pump_is_modern = self.__exists(RegisterTypes.INPUT, 2330)
        evidence["layout"] = {
            "heating_circuit_state_offset": heating_circuit_state_offset,
            "buffer_state_offset": buffer_state_offset,
            "heat_pump": "25.030" if heat_pump_is_modern else "legacy",
        }

        has_heatpump, has_biomassboiler, system = self.__detect_system(heat_pump_is_modern, evidence)
        has_photovoltaic = bool(self.__dword(2500))
        evidence["photovoltaic_power"] = self.__dword(2500)

        counts = self.__detect_counts(heating_circuit_state_offset, buffer_state_offset, evidence)
        self.__clamp_to_version(counts, api_version)

        result = DetectionResult(
            api_version=api_version,
            system=system,
            has_heatpump=has_heatpump,
            has_biomassboiler=has_biomassboiler,
            has_photovoltaic=has_photovoltaic,
            evidence=evidence,
            **counts,
        )
        logging.info(f"Detected {system.value} on api version {api_version.value}: {counts}")
        return result

    def __detect_system(self, heat_pump_is_modern: bool, evidence: Dict[str, Any]) -> tuple:
        """Which heat generator is installed, and so which system this is."""
        supply = self.__value(2300)
        return_temperature = self.__value(2301)
        heat_pump_state = self.__value(2330 if heat_pump_is_modern else 2326)
        has_heatpump = self.__live(supply) or self.__live(return_temperature) or self.__live(heat_pump_state)
        evidence["heat_pump"] = {"supply": supply, "return": return_temperature, "state": heat_pump_state}

        temperature = self.__value(2400)
        operating_mode = self.__value(2409)
        log_wood = self.__value(2412)
        octoplus_bottom = self.__value(2410)
        octoplus_top = self.__value(2411)
        pellets = self.__dword(2416)
        operating_minutes = self.__dword(2402)
        has_biomassboiler = self.__live(temperature) or bool(pellets) or bool(operating_minutes)
        evidence["biomass_boiler"] = {
            "temperature": temperature,
            "status": self.__value(2401),
            "operating_mode": operating_mode,
            "log_wood": log_wood,
            "octoplus_buffer": [octoplus_bottom, octoplus_top],
            "pellet_usage_total": pellets,
            "operating_minutes": operating_minutes,
        }

        # A heat pump is a vampair whatever else is on the controller, because
        # that is the component the library builds for it. Which biomass boiler
        # it is has only been reasoned from the specification - no therminator,
        # ecotop or octoplus was available to check it against - so the values
        # it rests on are in the evidence for a user to argue with.
        if has_heatpump:
            system = Systems.VAMPAIR
        elif not has_biomassboiler:
            system = Systems.VAMPAIR
        elif self.__live(octoplus_bottom) or self.__live(octoplus_top):
            # 2410 and 2411 are the buffer of an octoplus; on the other Sigmatek
            # boilers 2410 is a return temperature and the therminator leaves
            # both unused.
            system = Systems.OCTOPLUS
        elif self.__live(log_wood) or (operating_mode is not None and 1 <= operating_mode <= 3):
            # Kesselbetriebsart 1-3 all burn logs, which only a therminator does.
            # Mode 0 is logs as well, but it is also what an unset register reads,
            # so it is not taken as evidence of anything.
            system = Systems.THERMINATOR
        else:
            # The boiler that needs the least of the library: no log wood, no
            # sweep function, no pellet store reset. Wrong here costs a handful
            # of entities rather than a misread register.
            system = Systems.ECOTOP

        return has_heatpump, has_biomassboiler, system

    def __detect_counts(self, heating_circuit_state_offset: int, buffer_state_offset: int, evidence: Dict[str, Any]) -> Dict[str, int]:
        """How many of each repeated component the controller is driving."""

        def instances(base: int, stride: int, maximum: int, offset: int = 0) -> List[Optional[int]]:
            return [self.__value(base + stride * i + offset) for i in range(maximum)]

        heating_circuits = instances(HEATING_CIRCUIT_BASE, HEATING_CIRCUIT_STRIDE, HEATING_CIRCUIT_MAX, heating_circuit_state_offset)
        boilers = instances(BOILER_BASE, BOILER_STRIDE, BOILER_MAX, 1)
        buffers = instances(BUFFER_BASE, BUFFER_STRIDE, BUFFER_MAX, buffer_state_offset)
        circulations = instances(CIRCULATION_BASE, CIRCULATION_STRIDE, CIRCULATION_MAX)

        # The fresh water module status has no documented enumeration, so it is
        # taken together with the temperature of the water it is delivering.
        fresh_water = [(self.__value(FRESH_WATER_BASE + FRESH_WATER_STRIDE * i), self.__value(FRESH_WATER_BASE + FRESH_WATER_STRIDE * i + 1)) for i in range(FRESH_WATER_MAX)]

        # The solar circuit has no state saying whether it is there, so it goes
        # by the whole block reading plain zero. A channel that is configured
        # but has no sensor on it reports 130.0 or 270.0 °C, which counts as
        # there rather than not: an unconfigured one reads 0, the same way the
        # buffers that are not there have no X35 register at all while the one
        # that is has it reading 270.0.
        solar = [[self.__value(SOLAR_BASE + SOLAR_STRIDE * i + offset) for offset in (0, 1, 2, 3, 10, 13)] for i in range(SOLAR_MAX)]

        # The differential module is read for the evidence but never counted.
        # The same rule as solar would have claimed one on the system this was
        # written against, whose owner could find none configured, and whose
        # three live channels each repeated a temperature belonging to another
        # component - the boiler, and the heat pump flow and return. Whether
        # that is a module wired to those same points or the controller filling
        # an unused block is not something the registers settle, and a detector
        # filling in a form should not invent a component it cannot see. Until
        # an installation with a known differential module can say what one
        # looks like, this stays at zero for the user to raise.
        differential = [[self.__value(DIFFERENTIAL_BASE + DIFFERENTIAL_STRIDE * i + offset) for offset in (1, 2, 4, 5)] for i in range(DIFFERENTIAL_MAX)]

        evidence["heating_circuit_states"] = heating_circuits
        evidence["boiler_states"] = boilers
        evidence["buffer_states"] = buffers
        evidence["fresh_water_modules"] = fresh_water
        evidence["circulation_temperatures"] = circulations
        evidence["solar"] = solar
        evidence["differential_modules"] = differential

        return {
            "heating_circuit_count": sum(1 for state in heating_circuits if state is not None and state != HEATING_CIRCUIT_DISABLED),
            "boiler_count": sum(1 for state in boilers if state is not None and state not in NOT_PRESENT),
            "buffer_count": sum(1 for state in buffers if state is not None and state not in NOT_PRESENT),
            "fresh_water_module_count": sum(1 for state, temperature in fresh_water if self.__live(state) or self.__live(temperature)),
            "circulation_count": sum(1 for temperature in circulations if self.__live(temperature)),
            "solar_count": sum(1 for values in solar if any(self.__configured(value) for value in values)),
            "differential_module_count": 0,
        }

    @staticmethod
    def __clamp_to_version(counts: Dict[str, int], api_version: ApiVersions) -> None:
        """Drop components the detected version cannot address.

        The registers of a component are mapped whether or not the library can
        read them, so a controller can report a fresh water module over a
        version that has no fresh water module in it. Handing that count on
        would only make `SolarfocusAPI` refuse to build.
        """
        if not api_version.greater_or_equal(ApiVersions.V_23_020.value):
            counts["fresh_water_module_count"] = 0
        if not api_version.greater_or_equal(ApiVersions.V_25_030.value):
            counts["circulation_count"] = 0
            counts["differential_module_count"] = 0
            counts["solar_count"] = min(counts["solar_count"], 1)
