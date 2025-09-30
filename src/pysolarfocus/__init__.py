"""Python client lib for Solarfocus"""
import importlib.metadata
from enum import Enum

from packaging import version

__version__ = importlib.metadata.version("pysolarfocus")

# Default port for modbus
PORT = 502

# This needs to be defined before the imports because of circular dependencies
class Systems(str, Enum):
    """
    Supported systems by this library
    """

    VAMPAIR = "Vampair"
    THERMINATOR = "Therminator"
    ECOTOP = "Ecotop"
    PELLETELEGANCE = "Pellet Elegance"
    OCTOPLUS = "Octoplus"


class ApiVersions(str, Enum):
    """
    Supported Solarfocus API versions by this library
    """

    V_20_110 = "20.110"
    V_21_140 = "21.140"
    V_22_090 = "22.090"
    V_23_010 = "23.010"
    V_23_020 = "23.020"
    V_23_040 = "23.040"
    V_23_080 = "23.080"
    V_25_030 = "25.030"

    def greater_or_equal(self, api_version) -> bool:
        """Compare given version with own version."""
        return version.parse(self.value) >= version.parse(api_version)


# Async imports
from .async_api import AsyncSolarfocusAPI
from .async_component_manager import AsyncComponentManager
from .async_modbus_wrapper import AsyncModbusConnector
from .component_factory import ComponentFactory
from .component_manager import ComponentManager
from .config_validator import ConfigValidator
from .const import (
    SLAVE_ID,
    DomesticHotWaterMode,
    HeatingCircuitCooling,
    HeatingCircuitHeatingMode,
    HeatingCircuitMode,
    HeatPumpSgReadyMode,
)
from .exceptions import InvalidConfigurationError
from .modbus_wrapper import ModbusConnector


class SolarfocusAPI:
    """Solarfocus Heating System"""

    @property
    def system(self) -> Systems:
        return self._system

    @property
    def api_version(self) -> ApiVersions:
        return self._api_version

    def __init__(
        self,
        ip: str,
        heating_circuit_count: int = 1,
        buffer_count: int = 1,
        boiler_count: int = 1,
        fresh_water_module_count: int = 1,
        circulation_count: int = 1,
        differential_module_count: int = 1,
        solar_count: int = 1,
        system: Systems = Systems.VAMPAIR,
        port: int = PORT,
        slave_id: int = SLAVE_ID,
        api_version: ApiVersions = ApiVersions.V_21_140,
    ):
        """Initialize Solarfocus communication."""
        if not isinstance(system, Systems):
            raise InvalidConfigurationError("system not of type Systems")
        if not isinstance(api_version, ApiVersions):
            raise InvalidConfigurationError("api_version not of type ApiVersions")

        is_modern_api = api_version.greater_or_equal(ApiVersions.V_25_030.value)
        ConfigValidator.validate_component_count("heating_circuit", heating_circuit_count)
        ConfigValidator.validate_component_count("buffer", buffer_count)
        ConfigValidator.validate_component_count("boiler", boiler_count)
        ConfigValidator.validate_component_count("fresh_water_module", fresh_water_module_count)
        ConfigValidator.validate_component_count("circulation", circulation_count)
        ConfigValidator.validate_component_count("differential_module", differential_module_count)
        ConfigValidator.validate_component_count("solar", solar_count, is_modern_api)

        self.__conn = ModbusConnector(ip, port, slave_id)
        self._slave_id = slave_id
        self._system = system
        self._api_version = api_version

        # Initialize component manager
        self.__component_manager = ComponentManager(self.__conn)
        self.__component_manager.create_components(
            system, api_version, heating_circuit_count, buffer_count, boiler_count, fresh_water_module_count, circulation_count, differential_module_count, solar_count
        )

        # Get component references
        components = self.__component_manager.components
        self.heating_circuits = components["heating_circuits"]
        self.boilers = components["boilers"]
        self.buffers = components["buffers"]
        self.solar = components["solar"]

        if self._api_version.greater_or_equal(ApiVersions.V_23_020.value):
            self.fresh_water_modules = components.get("fresh_water_modules", [])

        if self._api_version.greater_or_equal(ApiVersions.V_23_040.value):
            self.fresh_water_module_cascade = components.get("fresh_water_module_cascade")
            self.circulation_module = components.get("circulation_module")

        if self._api_version.greater_or_equal(ApiVersions.V_25_030.value):
            self.circulations = components.get("circulations", [])
            self.differential_modules = components.get("differential_modules", [])

        # Single components
        self.heatpump = components.get("heatpump")
        self.photovoltaic = components.get("photovoltaic")
        self.biomassboiler = components.get("biomassboiler")

    def connect(self):
        """Connect to Solarfocus eco manager-touch"""
        return self.__conn.connect()

    @property
    def is_connected(self) -> bool:
        """Check if connection is established"""
        return self.__conn.is_connected

    def update(self) -> bool:
        """Read values from Heating System"""
        return self.__component_manager.update_all()

    def update_heating(self) -> bool:
        """Read values from Heating System"""
        return self.__component_manager.update("heating_circuits")

    def update_buffer(self) -> bool:
        """Read values from Heating System"""
        return self.__component_manager.update("buffers")

    def update_boiler(self) -> bool:
        """Read values from Heating System"""
        return self.__component_manager.update("boilers")

    def update_fresh_water_modules(self) -> bool:
        """Read values from Heating System"""
        if self._api_version.greater_or_equal(ApiVersions.V_23_020.value):
            return self.__component_manager.update("fresh_water_modules")
        return True

    def update_fresh_water_module_cascade(self) -> bool:
        """Read values from Fresh Water Module Cascade"""
        if self._api_version.greater_or_equal(ApiVersions.V_23_040.value):
            return self.fresh_water_module_cascade.update()
        return True

    def update_circulation_module(self) -> bool:
        """Read values from Circulation Module for DHW"""
        if self._api_version.greater_or_equal(ApiVersions.V_23_040.value):
            return self.__component_manager.update("circulation_module")
        return True

    def update_circulation(self) -> bool:
        """Read values from Heating System"""
        if self._api_version.greater_or_equal(ApiVersions.V_25_030.value):
            return self.__component_manager.update("circulations")
        return True

    def update_differential_modules(self) -> bool:
        """Read values from Heating System"""
        if self._api_version.greater_or_equal(ApiVersions.V_25_030.value):
            return self.__component_manager.update("differential_modules")
        return True

    def update_heatpump(self) -> bool:
        """Read values from Heating System"""
        if self._system is Systems.VAMPAIR:
            return self.__component_manager.update("heatpump")
        return True

    def update_photovoltaic(self) -> bool:
        """Read values from Heating System"""
        return self.__component_manager.update("photovoltaic")

    def update_biomassboiler(self) -> bool:
        """Read values from biomass boiler"""
        if self._system in [Systems.THERMINATOR, Systems.ECOTOP]:
            return self.__component_manager.update("biomassboiler")
        return True

    def update_solar(self) -> bool:
        """Read values from Solar"""
        return self.__component_manager.update("solar")

    def set_heating_circuit_mode(self, index, mode: HeatingCircuitMode) -> bool:
        """Set mode of heating circuit"""
        if 0 <= index < len(self.heating_circuits):
            _mode = self.heating_circuits[index].mode
            _mode.set_unscaled_value(mode)
            return _mode.commit()
        return False

    def set_heating_circuit_cooling(self, index, cooling: HeatingCircuitCooling) -> bool:
        """Set cooling of heating circuit"""
        if 0 <= index < len(self.heating_circuits):
            _cooling = self.heating_circuits[index].cooling
            _cooling.set_unscaled_value(cooling)
            return _cooling.commit()
        return False

    def set_heating_circuit_heating_mode(self, index, heating_mode: HeatingCircuitHeatingMode) -> bool:
        """Set heating_mode of heating circuit"""
        if 0 <= index < len(self.heating_circuits):
            _heating_mode = self.heating_circuits[index].heating_mode
            _heating_mode.set_unscaled_value(heating_mode)
            return _heating_mode.commit()
        return False

    def set_domestic_hot_water_mode(self, index, mode: DomesticHotWaterMode) -> bool:
        """Set domestic hot water / boiler mode"""
        if 0 <= index < len(self.boilers):
            _mode = self.boilers[index].mode
            _mode.set_unscaled_value(mode)
            return _mode.commit()
        return False

    def set_domestic_hot_water_single_charge(self, index, charge: bool) -> bool:
        """Set domestic hot water / boiler mode"""
        if 0 <= index < len(self.boilers):
            _single_charge = self.boilers[index].single_charge
            _single_charge.set_unscaled_value(int(charge))
            return _single_charge.commit()
        return False

    def set_heat_pump_sg_ready_mode(self, mode: HeatPumpSgReadyMode) -> bool:
        """Set SG-Ready mode of heat pump"""
        if self._system is Systems.VAMPAIR:
            _smart_grid = self.heatpump.smart_grid
            _smart_grid.set_unscaled_value(mode)
            return _smart_grid.commit()
        return False

    def set_heat_pump_evu_lock(self, lock: bool) -> bool:
        """Set heat pump EVU Lock"""
        if self._system is Systems.VAMPAIR:
            _evu_lock = self.heatpump.evu_lock
            _evu_lock.set_unscaled_value(int(lock))
            return _evu_lock.commit()
        return False

    def __repr__(self) -> str:
        message = ["-" * 50]
        message.append(f"{self.__class__.__name__}, v{__version__}")
        message.append("-" * 50)
        message.append(f"+ System: {self.system.value}")
        message.append(f"+ Version: {self._api_version.value}")
        message.append("-" * 50)
        return "\n".join(message)
