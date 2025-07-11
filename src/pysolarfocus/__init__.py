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


from .component_factory import ComponentFactory
from .const import (
    SLAVE_ID,
    DomesticHotWaterMode,
    HeatingCircuitCooling,
    HeatingCircuitHeatingMode,
    HeatingCircuitMode,
    HeatPumpSgReadyMode,
)
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
        assert heating_circuit_count >= 0 and heating_circuit_count < 9, "Heating circuit count must be between 0 and 8"
        assert buffer_count >= 0 and buffer_count < 5, "Buffer count must be between 0 and 4"
        assert boiler_count >= 0 and boiler_count < 5, "Boiler count must be between 0 and 4"
        assert fresh_water_module_count >= 0 and fresh_water_module_count < 5, "Fresh water module count must be between 0 and 4"
        assert circulation_count >= 0 and circulation_count < 5, "Circulation count must be between 0 and 4"
        assert differential_module_count >= 0 and differential_module_count < 5, "Differential module count must be between 0 and 4"

        assert isinstance(system, Systems), "system not of type Systems"
        assert isinstance(api_version, ApiVersions), "api_version not of type ApiVersions"

        self.__conn = ModbusConnector(ip, port, slave_id)
        self.__factory = ComponentFactory(self.__conn)
        self._slave_id = slave_id
        self._system = system
        self._api_version = api_version

        if self._api_version.greater_or_equal(ApiVersions.V_25_030.value):
            assert solar_count >= 0 and solar_count < 5, "Solar count must be between 0 and 4"
        else:
            assert solar_count >= 0 and solar_count < 2, "Solar count must be max 1"

        # Lists of components
        self.heating_circuits = self.__factory.heating_circuit(system, heating_circuit_count, api_version)
        self.boilers = self.__factory.boiler(system, boiler_count, api_version)
        self.buffers = self.__factory.buffer(system, buffer_count, api_version)
        self.solar = self.__factory.solar(system, solar_count, api_version)

        if self._api_version.greater_or_equal(ApiVersions.V_23_020.value):
            self.fresh_water_modules = self.__factory.fresh_water_modules(system, fresh_water_module_count, api_version)

        if self._api_version.greater_or_equal(ApiVersions.V_25_030.value):
            self.circulations = self.__factory.circulation(system, circulation_count, api_version)
            self.differential_modules = self.__factory.differential_modules(system, differential_module_count, api_version)

        # Single components
        self.heatpump = self.__factory.heatpump(system, api_version)
        self.photovoltaic = self.__factory.photovoltaic(system, api_version)
        self.biomassboiler = self.__factory.pelletsboiler(system, api_version)

    def connect(self):
        """Connect to Solarfocus eco manager-touch"""
        return self.__conn.connect()

    @property
    def is_connected(self) -> bool:
        """Check if connection is established"""
        return self.__conn.is_connected

    def update(self) -> bool:
        """Read values from Heating System"""
        if (
            self.update_heating()
            and self.update_buffer()
            and self.update_boiler()
            and self.update_heatpump()
            and self.update_photovoltaic()
            and self.update_biomassboiler()
            and self.update_solar()
            and self.update_fresh_water_modules()
            and self.update_circulation()
            and self.update_differential_modules()
        ):
            return True
        return False

    def update_heating(self) -> bool:
        """Read values from Heating System"""
        for heating_circuit in self.heating_circuits:
            if not heating_circuit.update():
                return False
        return True

    def update_buffer(self) -> bool:
        """Read values from Heating System"""
        for buffer in self.buffers:
            if not buffer.update():
                return False
        return True

    def update_boiler(self) -> bool:
        """Read values from Heating System"""
        for boiler in self.boilers:
            if not boiler.update():
                return False
        return True

    def update_fresh_water_modules(self) -> bool:
        """Read values from Heating System"""
        if self._api_version.greater_or_equal(ApiVersions.V_23_020.value):
            for fresh_water_module in self.fresh_water_modules:
                if not fresh_water_module.update():
                    return False
        return True

    def update_circulation(self) -> bool:
        """Read values from Heating System"""
        if self._api_version.greater_or_equal(ApiVersions.V_25_030.value):
            for circulation in self.circulations:
                if not circulation.update():
                    return False
        return True

    def update_differential_modules(self) -> bool:
        """Read values from Heating System"""
        if self._api_version.greater_or_equal(ApiVersions.V_25_030.value):
            for differential_module in self.differential_modules:
                if not differential_module.update():
                    return False
        return True

    def update_heatpump(self) -> bool:
        """Read values from Heating System"""
        if self._system is Systems.VAMPAIR:
            return self.heatpump.update()
        return True

    def update_photovoltaic(self) -> bool:
        """Read values from Heating System"""
        if self.photovoltaic:
            return self.photovoltaic.update()
        return True

    def update_biomassboiler(self) -> bool:
        """Read values from biomass boiler"""
        if self._system in [Systems.THERMINATOR, Systems.ECOTOP]:
            return self.biomassboiler.update()
        return True

    def update_solar(self) -> bool:
        """Read values from Solar"""
        for solar in self.solar:
            if not solar.update():
                return False
        return True

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
