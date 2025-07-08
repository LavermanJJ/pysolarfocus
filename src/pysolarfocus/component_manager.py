"""Component manager for centralized component lifecycle management"""

import logging
from typing import Any, Dict, List, Optional

from . import ApiVersions, Systems
from .component_factory import ComponentFactory
from .exceptions import ComponentInitializationError
from .modbus_wrapper import ModbusConnector


class ComponentManager:
    """Manages the lifecycle of all Solarfocus components with centralized error handling."""

    def __init__(self, modbus_connector: ModbusConnector):
        """Initialize component manager.

        Args:
            modbus_connector: Modbus connection instance
        """
        self.modbus_connector = modbus_connector
        self.factory = ComponentFactory(modbus_connector)
        self.components: Dict[str, Any] = {}
        self._failed_components: List[str] = []

    def create_components(
        self,
        system: Systems,
        api_version: ApiVersions,
        heating_circuit_count: int = 1,
        buffer_count: int = 1,
        boiler_count: int = 1,
        fresh_water_module_count: int = 1,
        circulation_count: int = 1,
        differential_module_count: int = 1,
        solar_count: int = 1,
    ) -> None:
        """Create all required components based on configuration.

        Args:
            system: Solarfocus system type
            api_version: API version
            *_count: Number of each component type to create
        """
        try:
            # Create multi-instance components
            self.components["heating_circuits"] = self.factory.heating_circuit(system, heating_circuit_count, api_version)
            self.components["boilers"] = self.factory.boiler(system, boiler_count, api_version)
            self.components["buffers"] = self.factory.buffer(system, buffer_count, api_version)
            self.components["solar"] = self.factory.solar(system, solar_count, api_version)

            # Create version-specific components
            if api_version.greater_or_equal(ApiVersions.V_23_020.value):
                self.components["fresh_water_modules"] = self.factory.fresh_water_modules(system, fresh_water_module_count, api_version)

            if api_version.greater_or_equal(ApiVersions.V_25_030.value):
                self.components["circulations"] = self.factory.circulation(system, circulation_count, api_version)
                self.components["differential_modules"] = self.factory.differential_modules(system, differential_module_count, api_version)

            # Create single-instance components
            self.components["heatpump"] = self.factory.heatpump(system, api_version)
            self.components["photovoltaic"] = self.factory.photovoltaic(system, api_version)
            self.components["biomassboiler"] = self.factory.pelletsboiler(system, api_version)

            logging.info("All components created successfully")

        except Exception as e:
            raise ComponentInitializationError(f"Failed to create components: {e}")

    def update_all(self) -> bool:
        """Update all components and track failures.

        Returns:
            True if all components updated successfully, False otherwise
        """
        success = True
        self._failed_components.clear()

        for component_name, component in self.components.items():
            try:
                if isinstance(component, list):
                    for i, comp in enumerate(component):
                        if not comp.update():
                            success = False
                            self._failed_components.append(f"{component_name}[{i}]")
                else:
                    if not component.update():
                        success = False
                        self._failed_components.append(component_name)
            except Exception as e:
                logging.error(f"Error updating {component_name}: {e}")
                success = False
                self._failed_components.append(component_name)

        if not success:
            logging.warning(f"Failed to update components: {', '.join(self._failed_components)}")

        return success

    def get_component(self, name: str) -> Optional[Any]:
        """Get component by name.

        Args:
            name: Component name

        Returns:
            Component instance or list of components, None if not found
        """
        return self.components.get(name)

    def get_failed_components(self) -> List[str]:
        """Get list of components that failed during last update.

        Returns:
            List of failed component names
        """
        return self._failed_components.copy()

    def is_healthy(self) -> bool:
        """Check if all components are healthy (no recent failures).

        Returns:
            True if no components failed in last update
        """
        return len(self._failed_components) == 0
