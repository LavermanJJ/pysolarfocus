"""Async Solarfocus API"""

import asyncio
import logging
from typing import List, Optional

from . import PORT, SLAVE_ID, ApiVersions, Systems
from .async_component import AsyncComponent
from .async_component_manager import AsyncComponentManager
from .async_modbus_wrapper import AsyncModbusConnector
from .config_validator import ConfigValidator
from .const import (
    DomesticHotWaterMode,
    HeatingCircuitCooling,
    HeatingCircuitHeatingMode,
    HeatingCircuitMode,
    HeatPumpSgReadyMode,
)
from .exceptions import InvalidConfigurationError


class AsyncSolarfocusAPI:
    """Async version of SolarfocusAPI for non-blocking Heating System communication"""

    @property
    def system(self) -> Systems:
        """Get the system type"""
        return self._system

    @property
    def api_version(self) -> ApiVersions:
        """Get the API version"""
        return self._api_version

    @property
    def component_manager(self) -> AsyncComponentManager:
        """Get the component manager (for testing purposes)"""
        return self.__component_manager

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
        auto_reconnect: bool = True,
        connection_timeout: float = 10.0,
    ):
        """Initialize Async Solarfocus communication.

        Args:
            ip: IP address of the Solarfocus system
            heating_circuit_count: Number of heating circuits
            buffer_count: Number of buffers
            boiler_count: Number of boilers
            fresh_water_module_count: Number of fresh water modules
            circulation_count: Number of circulation modules
            differential_module_count: Number of differential modules
            solar_count: Number of solar modules
            system: Solarfocus system type
            port: Modbus TCP port
            slave_id: Modbus slave ID
            api_version: API version to use
            auto_reconnect: Enable automatic reconnection
            connection_timeout: Connection timeout in seconds
        """
        if not isinstance(system, Systems):
            raise InvalidConfigurationError("system not of type Systems")
        if not isinstance(api_version, ApiVersions):
            raise InvalidConfigurationError("api_version not of type ApiVersions")

        is_modern_api = api_version.greater_or_equal(ApiVersions.V_25_030.value)

        # Validate component counts
        ConfigValidator.validate_component_count("heating_circuit", heating_circuit_count)
        ConfigValidator.validate_component_count("buffer", buffer_count)
        ConfigValidator.validate_component_count("boiler", boiler_count)
        ConfigValidator.validate_component_count("fresh_water_module", fresh_water_module_count)
        ConfigValidator.validate_component_count("circulation", circulation_count)
        ConfigValidator.validate_component_count("differential_module", differential_module_count)
        ConfigValidator.validate_component_count("solar", solar_count, is_modern_api)

        self.__conn = AsyncModbusConnector(ip, port, slave_id)
        self._slave_id = slave_id
        self._system = system
        self._api_version = api_version

        # Store component counts for later initialization
        self._component_counts = {
            "heating_circuit_count": heating_circuit_count,
            "buffer_count": buffer_count,
            "boiler_count": boiler_count,
            "fresh_water_module_count": fresh_water_module_count,
            "circulation_count": circulation_count,
            "differential_module_count": differential_module_count,
            "solar_count": solar_count,
        }

        # Initialize component manager
        self.__component_manager = AsyncComponentManager(self.__conn)

        # Component references (will be set after create_components)
        self.heating_circuits: List[AsyncComponent] = []
        self.boilers: List[AsyncComponent] = []
        self.buffers: List[AsyncComponent] = []
        self.solar: List[AsyncComponent] = []
        self.fresh_water_modules: List[AsyncComponent] = []
        self.circulations: List[AsyncComponent] = []
        self.differential_modules: List[AsyncComponent] = []
        self.heatpump: Optional[AsyncComponent] = None
        self.photovoltaic: Optional[AsyncComponent] = None
        self.biomassboiler: Optional[AsyncComponent] = None
        self.fresh_water_module_cascade: Optional[AsyncComponent] = None
        self.circulation_module: Optional[AsyncComponent] = None

    async def initialize(self) -> None:
        """Initialize components asynchronously. Must be called after __init__."""
        await self.__component_manager.create_components(self._system, self._api_version, **self._component_counts)

        # Get component references
        self._update_component_references()

    def _update_component_references(self) -> None:
        """Update component references from component manager"""
        components = self.__component_manager.components

        # Handle list components with type checking
        heating_circuits = components.get("heating_circuits", [])
        self.heating_circuits = heating_circuits if isinstance(heating_circuits, list) else []

        boilers = components.get("boilers", [])
        self.boilers = boilers if isinstance(boilers, list) else []

        buffers = components.get("buffers", [])
        self.buffers = buffers if isinstance(buffers, list) else []

        solar = components.get("solar", [])
        self.solar = solar if isinstance(solar, list) else []

        if self._api_version.greater_or_equal(ApiVersions.V_23_020.value):
            fresh_water_modules = components.get("fresh_water_modules", [])
            self.fresh_water_modules = fresh_water_modules if isinstance(fresh_water_modules, list) else []

        if self._api_version.greater_or_equal(ApiVersions.V_23_040.value):
            fwm_cascade = components.get("fresh_water_module_cascade")
            self.fresh_water_module_cascade = fwm_cascade if not isinstance(fwm_cascade, list) else None

            circ_module = components.get("circulation_module")
            self.circulation_module = circ_module if not isinstance(circ_module, list) else None

        if self._api_version.greater_or_equal(ApiVersions.V_25_030.value):
            circulations = components.get("circulations", [])
            self.circulations = circulations if isinstance(circulations, list) else []

            diff_modules = components.get("differential_modules", [])
            self.differential_modules = diff_modules if isinstance(diff_modules, list) else []

        # Single components with type checking
        heatpump = components.get("heatpump")
        self.heatpump = heatpump if not isinstance(heatpump, list) else None

        photovoltaic = components.get("photovoltaic")
        self.photovoltaic = photovoltaic if not isinstance(photovoltaic, list) else None

        biomassboiler = components.get("biomassboiler")
        self.biomassboiler = biomassboiler if not isinstance(biomassboiler, list) else None

    async def connect(self) -> bool:
        """Connect to Solarfocus eco manager-touch"""
        try:
            connected = await self.__conn.connect()
            if connected:
                logging.info("Successfully connected to Solarfocus system")
            else:
                logging.warning("Failed to connect to Solarfocus system")
            return connected
        except Exception as e:
            logging.error(f"Error during connection: {e}")
            return False

    @property
    def is_connected(self) -> bool:
        """Check if connection is established"""
        return self.__conn.is_connected

    def get_connection_health(self) -> dict:
        """Get connection health information"""
        return self.__conn.get_connection_health()

    async def update(self, parallel: bool = True, optimized: bool = False) -> bool:
        """Read values from Heating System.

        Args:
            parallel: Whether to update components in parallel (default: True)
            optimized: Whether to use optimized update method (default: False)
        """
        try:
            if not self.is_connected:
                logging.warning("Attempting to update while not connected")
                return False
            return await self.__component_manager.update_all(parallel=parallel, optimized=optimized)
        except Exception as e:
            logging.error(f"Error during update: {e}")
            return False

    async def update_partial(self, component_names: List[str], parallel: bool = True, optimized: bool = False) -> bool:
        """Update only specific components.

        Args:
            component_names: List of component names to update
            parallel: Whether to update in parallel
            optimized: Whether to use optimized update method
        """
        if parallel:
            tasks = [self.__component_manager.update(name, optimized=optimized) for name in component_names]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return all(result is True for result in results if not isinstance(result, Exception))
        else:
            for name in component_names:
                if not await self.__component_manager.update(name, optimized=optimized):
                    return False
            return True

    async def update_heating(self) -> bool:
        """Read values from Heating System"""
        return await self.__component_manager.update("heating_circuits")

    async def update_buffer(self) -> bool:
        """Read values from Heating System"""
        return await self.__component_manager.update("buffers")

    async def update_boiler(self) -> bool:
        """Read values from Heating System"""
        return await self.__component_manager.update("boilers")

    async def update_fresh_water_modules(self) -> bool:
        """Read values from Heating System"""
        if self._api_version.greater_or_equal(ApiVersions.V_23_020.value):
            return await self.__component_manager.update("fresh_water_modules")
        return True

    async def update_fresh_water_module_cascade(self) -> bool:
        """Read values from Fresh Water Module Cascade"""
        if self._api_version.greater_or_equal(ApiVersions.V_23_040.value) and self.fresh_water_module_cascade:
            return await self.fresh_water_module_cascade.update()
        return True

    async def update_circulation_module(self) -> bool:
        """Read values from Circulation Module for DHW"""
        if self._api_version.greater_or_equal(ApiVersions.V_23_040.value) and self.circulation_module:
            return await self.circulation_module.update()
        return True

    async def update_circulation(self) -> bool:
        """Read values from Heating System"""
        if self._api_version.greater_or_equal(ApiVersions.V_25_030.value):
            return await self.__component_manager.update("circulations")
        return True

    async def update_differential_modules(self) -> bool:
        """Read values from Heating System"""
        if self._api_version.greater_or_equal(ApiVersions.V_25_030.value):
            return await self.__component_manager.update("differential_modules")
        return True

    async def update_heatpump(self) -> bool:
        """Read values from Heating System"""
        if self._system is Systems.VAMPAIR and self.heatpump:
            return await self.heatpump.update()
        return True

    async def update_photovoltaic(self) -> bool:
        """Read values from Heating System"""
        if self.photovoltaic:
            return await self.photovoltaic.update()
        return True

    async def update_biomassboiler(self) -> bool:
        """Read values from biomass boiler"""
        if self._system in [Systems.THERMINATOR, Systems.ECOTOP] and self.biomassboiler:
            return await self.biomassboiler.update()
        return True

    async def update_solar(self) -> bool:
        """Read values from Solar"""
        return await self.__component_manager.update("solar")

    async def set_heating_circuit_mode(self, index: int, mode: HeatingCircuitMode) -> bool:
        """Set mode of heating circuit"""
        if 0 <= index < len(self.heating_circuits):
            _mode = self.heating_circuits[index].mode
            _mode.set_unscaled_value(mode)
            return await asyncio.to_thread(_mode.commit)
        return False

    async def set_heating_circuit_cooling(self, index: int, cooling: HeatingCircuitCooling) -> bool:
        """Set cooling of heating circuit"""
        if 0 <= index < len(self.heating_circuits):
            _cooling = self.heating_circuits[index].cooling
            _cooling.set_unscaled_value(cooling)
            return await asyncio.to_thread(_cooling.commit)
        return False

    async def set_heating_circuit_heating_mode(self, index: int, heating_mode: HeatingCircuitHeatingMode) -> bool:
        """Set heating_mode of heating circuit"""
        if 0 <= index < len(self.heating_circuits):
            _heating_mode = self.heating_circuits[index].heating_mode
            _heating_mode.set_unscaled_value(heating_mode)
            return await asyncio.to_thread(_heating_mode.commit)
        return False

    async def set_domestic_hot_water_mode(self, index: int, mode: DomesticHotWaterMode) -> bool:
        """Set mode of domestic hot water"""
        if 0 <= index < len(self.fresh_water_modules):
            _mode = self.fresh_water_modules[index].mode
            _mode.set_unscaled_value(mode)
            return await asyncio.to_thread(_mode.commit)
        return False

    async def set_heatpump_sg_ready_mode(self, mode: HeatPumpSgReadyMode) -> bool:
        """Set SG Ready mode of heat pump"""
        if self.heatpump:
            _mode = self.heatpump.sg_ready_mode
            _mode.set_unscaled_value(mode)
            return await asyncio.to_thread(_mode.commit)
        return False

    def get_failed_components(self) -> List[str]:
        """Get list of components that failed during last update"""
        return self.__component_manager.get_failed_components()

    def is_healthy(self) -> bool:
        """Check if all components are healthy"""
        return self.__component_manager.is_healthy()

    async def disconnect(self) -> None:
        """Disconnect from the heating system"""
        try:
            await self.__conn.disconnect()
            logging.info("Disconnected from Solarfocus system")
        except Exception as e:
            logging.error(f"Error during disconnection: {e}")

    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()

    def __repr__(self) -> str:
        from . import __version__

        message = ["-" * 50]
        message.append(f"Async{self.__class__.__name__}, v{__version__}")
        message.append("-" * 50)
        message.append(f"+ System: {self.system.value}")
        message.append(f"+ Version: {self._api_version.value}")
        message.append(f"+ Connection: {'Connected' if self.is_connected else 'Disconnected'}")
        message.append(f"+ Health: {'Healthy' if self.is_healthy() else 'Issues detected'}")
        message.append("-" * 50)
        return "\n".join(message)
