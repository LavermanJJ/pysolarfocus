"""Async Solarfocus component base class"""
import asyncio
import logging
from typing import Any, Optional

from .async_modbus_wrapper import AsyncModbusConnector
from .components.base.component import Component
from .components.base.enums import RegisterTypes


class AsyncComponent:
    """
    Async wrapper for Component that provides non-blocking operations
    """

    def __init__(self, sync_component: Component):
        """Initialize with sync component.
        
        Args:
            sync_component: The synchronous component to wrap
        """
        self._sync_component = sync_component
        self._async_modbus: Optional[AsyncModbusConnector] = None

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to sync component"""
        return getattr(self._sync_component, name)

    async def initialize(self, async_modbus: AsyncModbusConnector) -> 'AsyncComponent':
        """Initialize the async component with async modbus connector.
        
        Args:
            async_modbus: Async modbus connector instance
            
        Returns:
            Self for method chaining
        """
        self._async_modbus = async_modbus
        
        # Initialize the underlying sync component with the sync connector
        await asyncio.to_thread(
            self._sync_component.initialize, 
            async_modbus.sync_connector
        )
        return self

    async def update(self) -> bool:
        """Async update method for retrieving current values from the heating system"""
        if not self._async_modbus:
            logging.error(f"AsyncComponent {self._sync_component.__class__.__name__} not properly initialized")
            return False

        try:
            # Run the sync update in a thread pool to avoid blocking
            return await asyncio.to_thread(self._sync_component.update)
        except Exception as e:
            logging.exception(f"Error during async update of {self._sync_component.__class__.__name__}: {e}")
            return False

    async def update_optimized(self) -> bool:
        """Optimized async update that directly handles modbus operations"""
        if not self._async_modbus:
            logging.error(f"AsyncComponent {self._sync_component.__class__.__name__} not properly initialized")
            return False

        failed = False

        # Handle input registers
        if self._sync_component.has_input_address:
            read_success, registers = await self._async_modbus.read_input_registers(
                self._sync_component.input_slices, 
                self._sync_component.input_count
            )
            if read_success and registers is not None:
                parsing_success = await asyncio.to_thread(
                    self._sync_component._parse, 
                    registers, 
                    RegisterTypes.INPUT
                )
                failed = not parsing_success or failed
            else:
                failed = True
                logging.error(f"Failed to read input registers of {self._sync_component.__class__.__name__}")

        # Handle holding registers  
        if self._sync_component.has_holding_address:
            read_success, registers = await self._async_modbus.read_holding_registers(
                self._sync_component.holding_slices, 
                self._sync_component.holding_count
            )
            if read_success and registers is not None:
                parsing_success = await asyncio.to_thread(
                    self._sync_component._parse, 
                    registers, 
                    RegisterTypes.HOLDING
                )
                failed = not parsing_success or failed
            else:
                failed = True
                logging.error(f"Failed to read holding registers of {self._sync_component.__class__.__name__}")

        return not failed

    def __repr__(self) -> str:
        return f"Async{self._sync_component.__repr__()}"
