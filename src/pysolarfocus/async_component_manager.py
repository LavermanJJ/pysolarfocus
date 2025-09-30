"""Async component manager for centralized component lifecycle management"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union

from . import ApiVersions, Systems
from .async_component import AsyncComponent
from .async_modbus_wrapper import AsyncModbusConnector
from .component_factory import ComponentFactory
from .exceptions import ComponentInitializationError


class AsyncComponentManager:
    """Async version of ComponentManager for non-blocking component lifecycle management."""

    def __init__(self, async_modbus_connector: AsyncModbusConnector):
        """Initialize async component manager.

        Args:
            async_modbus_connector: Async Modbus connection instance
        """
        self.async_modbus_connector = async_modbus_connector
        self.factory = ComponentFactory(async_modbus_connector.sync_connector)
        self.components: Dict[str, Union[AsyncComponent, List[AsyncComponent]]] = {}
        self._failed_components: List[str] = []

    async def create_components(
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
            # Create sync components first using the factory
            sync_components = await asyncio.to_thread(
                self._create_sync_components,
                system,
                api_version,
                heating_circuit_count,
                buffer_count,
                boiler_count,
                fresh_water_module_count,
                circulation_count,
                differential_module_count,
                solar_count,
            )
            # Wrap sync components in async wrappers
            await self._wrap_components(sync_components)
            logging.info("All async components created successfully")
        except Exception as e:
            raise ComponentInitializationError(f"Failed to create async components: {e}")

    def _create_sync_components(
        self,
        system: Systems,
        api_version: ApiVersions,
        heating_circuit_count: int,
        buffer_count: int,
        boiler_count: int,
        fresh_water_module_count: int,
        circulation_count: int,
        differential_module_count: int,
        solar_count: int,
    ) -> Dict[str, Any]:
        """Create sync components using the factory (runs in thread pool)"""
        sync_components = {}

        # Create multi-instance components
        sync_components["heating_circuits"] = self.factory.heating_circuit(system, heating_circuit_count, api_version)
        sync_components["boilers"] = self.factory.boiler(system, boiler_count, api_version)
        sync_components["buffers"] = self.factory.buffer(system, buffer_count, api_version)
        sync_components["solar"] = self.factory.solar(system, solar_count, api_version)

        # Create version-specific components
        if api_version.greater_or_equal(ApiVersions.V_23_020.value):
            sync_components["fresh_water_modules"] = self.factory.fresh_water_modules(system, fresh_water_module_count, api_version)

        if api_version.greater_or_equal(ApiVersions.V_25_030.value):
            sync_components["circulations"] = self.factory.circulation(system, circulation_count, api_version)
            sync_components["differential_modules"] = self.factory.differential_modules(system, differential_module_count, api_version)

        # Create single-instance components
        sync_components["heatpump"] = self.factory.heatpump(system, api_version)
        sync_components["photovoltaic"] = self.factory.photovoltaic(system, api_version)
        sync_components["biomassboiler"] = self.factory.pelletsboiler(system, api_version)

        return sync_components

    async def _wrap_components(self, sync_components: Dict[str, Any]) -> None:
        """Wrap sync components in async wrappers"""
        for component_name, sync_component in sync_components.items():
            if isinstance(sync_component, list):
                # Handle lists of components
                async_components = []
                for sync_comp in sync_component:
                    async_comp = AsyncComponent(sync_comp)
                    await async_comp.initialize(self.async_modbus_connector)
                    async_components.append(async_comp)
                self.components[component_name] = async_components
            else:
                # Handle single components
                if sync_component is not None:
                    async_comp = AsyncComponent(sync_component)
                    await async_comp.initialize(self.async_modbus_connector)
                    self.components[component_name] = async_comp

    async def update_all(self, parallel: bool = True, optimized: bool = False) -> bool:
        """Update all components with optional parallel execution.

        Args:
            parallel: Whether to update components in parallel (default: True)
            optimized: Whether to use optimized update method (default: False)

        Returns:
            True if all components updated successfully, False otherwise
        """
        self._failed_components.clear()

        if parallel:
            return await self._update_all_parallel(optimized)
        else:
            return await self._update_all_sequential(optimized)

    async def _update_all_parallel(self, optimized: bool) -> bool:
        """Update all components in parallel"""
        tasks = []
        component_names = []

        for component_name in self.components:
            tasks.append(self.update(component_name, optimized=optimized))
            component_names.append(component_name)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        success = True
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logging.error(f"Exception updating {component_names[i]}: {result}")
                self._failed_components.append(component_names[i])
                success = False
            elif not result:
                success = False

        if not success:
            logging.warning(f"Failed to update components: {', '.join(self._failed_components)}")

        return success

    async def _update_all_sequential(self, optimized: bool) -> bool:
        """Update all components sequentially"""
        success = True

        for component_name in self.components:
            if not await self.update(component_name, optimized=optimized):
                success = False

        if not success:
            logging.warning(f"Failed to update components: {', '.join(self._failed_components)}")

        return success

    def get_component(self, name: str) -> Optional[Union[AsyncComponent, List[AsyncComponent]]]:
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

    async def update(self, component_name: str, optimized: bool = False) -> bool:
        """Update a single component or component list.

        Args:
            component_name: Name of the component to update
            optimized: Whether to use optimized update method

        Returns:
            True if update was successful, False otherwise
        """
        if component_name not in self.components:
            return False

        component = self.components[component_name]
        try:
            if isinstance(component, list):
                # Update list of components
                tasks = []
                for comp in component:
                    if optimized and hasattr(comp, "update_optimized"):
                        tasks.append(comp.update_optimized())
                    else:
                        tasks.append(comp.update())
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for i, result in enumerate(results):
                    if isinstance(result, Exception) or not result:
                        self._failed_components.append(f"{component_name}[{i}]")
                        return False
            else:
                # Update single component
                if optimized and hasattr(component, "update_optimized"):
                    result = await component.update_optimized()
                else:
                    result = await component.update()
                if not result:
                    self._failed_components.append(component_name)
                    return False
            return True
        except Exception as e:
            logging.error(f"Error updating {component_name}: {e}")
            self._failed_components.append(component_name)
            return False
