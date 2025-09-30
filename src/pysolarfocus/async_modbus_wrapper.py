"""Async Solarfocus modbus wrapper"""

import asyncio
import logging
import time
from typing import List, Optional, Tuple

from pymodbus.client import AsyncModbusTcpClient

from .components.base.register_slice import RegisterSlice
from .modbus_wrapper import ModbusConnector

# Export both connectors for external use
__all__ = ["AsyncModbusConnector", "ModbusConnector"]

ASYNC_CLIENT_NOT_INITIALIZED = "AsyncModbusTcpClient is not initialized!"


class AsyncModbusConnector:
    """
    True async Modbus connector using pymodbus 4.x AsyncModbusTcpClient
    Also maintains a sync connector for compatibility with existing components.
    """

    def __init__(self, ip: str, port: int, slave_id: int, retry_count: int = 3, retry_delay: float = 1.0) -> None:
        self._ip = ip
        self._port = port
        self._slave_id = slave_id
        self._retry_count = retry_count
        self._retry_delay = retry_delay
        self._client: Optional[AsyncModbusTcpClient] = None
        self._connection_lock = asyncio.Lock()
        self._last_connection_attempt = 0.0
        self._connection_backoff = 1.0
        self._max_backoff = 60.0
        self._is_connected = False

        # Create sync connector for compatibility
        self._sync_connector = ModbusConnector(ip, port, slave_id, retry_count, retry_delay)

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def port(self) -> int:
        return self._port

    @property
    def slave_id(self) -> int:
        return self._slave_id

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def sync_connector(self) -> ModbusConnector:
        """Get the sync connector for compatibility with existing components"""
        return self._sync_connector

    async def connect(self) -> bool:
        """Connect to modbus server with async retry logic using AsyncModbusTcpClient."""
        async with self._connection_lock:
            for attempt in range(self._retry_count):
                now = time.time()
                if now - self._last_connection_attempt < self._connection_backoff:
                    await asyncio.sleep(self._connection_backoff - (now - self._last_connection_attempt))
                self._last_connection_attempt = time.time()

                try:
                    self._client = AsyncModbusTcpClient(host=self._ip, port=self._port)
                    await self._client.connect()
                    if self._client.connected:
                        self._is_connected = True
                        self._connection_backoff = 1.0
                        # Also connect the sync connector
                        sync_connected = await asyncio.to_thread(self._sync_connector.connect)
                        if not sync_connected:
                            logging.warning("Sync connector failed to connect, but async is connected")
                        logging.info(f"Successfully connected to async modbus server at {self.ip}:{self.port}")
                        return True
                    else:
                        if attempt < self._retry_count - 1:
                            self._connection_backoff = min(self._connection_backoff * 2, self._max_backoff)
                            logging.warning(f"Async connection attempt {attempt + 1} failed, retrying in {self._connection_backoff}s")
                            await asyncio.sleep(self._retry_delay)
                        else:
                            self._is_connected = False
                            logging.error(f"Failed to connect to async modbus server after {self._retry_count} attempts")
                            return False
                except Exception as e:
                    if attempt < self._retry_count - 1:
                        self._connection_backoff = min(self._connection_backoff * 2, self._max_backoff)
                        logging.error(f"Async connection attempt {attempt + 1} failed with exception: {e}, retrying...")
                        await asyncio.sleep(self._retry_delay)
                    else:
                        self._is_connected = False
                        logging.error(f"Failed to connect to async modbus server after {self._retry_count} attempts, last error: {e}")
                        return False
            return False

    async def read_input_registers(self, slices: List[RegisterSlice], count: int, check_connection: bool = True) -> Tuple[bool, Optional[List[int]]]:
        """Async method to read input registers from modbus using async client."""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False, None
        try:
            if not self._client:
                logging.error(ASYNC_CLIENT_NOT_INITIALIZED)
                return False, None

            # Use slave parameter for async client (this is the correct parameter name for async client)
            slave_param = self._slave_id

            # Read registers using the same logic as sync connector
            combined_result: List[Optional[int]] = [None] * count
            for register_slice in slices:
                result = await self._client.read_input_registers(address=register_slice.absolute_address, count=register_slice.count, slave=slave_param)
                if result.isError():
                    logging.error(f"Async modbus read error at address={register_slice.absolute_address}, count={register_slice.count}: {result}")
                    return False, None
                slice_data = result.registers
                combined_result[register_slice.relative_address : register_slice.relative_address + register_slice.count] = slice_data

            # Convert to List[int], replacing any remaining None values with 0
            final_result = [x if x is not None else 0 for x in combined_result]
            return True, final_result
        except Exception as e:
            logging.exception(f"Exception while reading input registers async: {e}")
            return False, None

    async def read_holding_registers(self, slices: List[RegisterSlice], count: int, check_connection: bool = True) -> Tuple[bool, Optional[List[int]]]:
        """Async method to read holding registers from modbus using async client."""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False, None
        try:
            if not self._client:
                logging.error(ASYNC_CLIENT_NOT_INITIALIZED)
                return False, None

            # Use slave parameter for async client
            slave_param = self._slave_id

            # Read registers using the same logic as sync connector
            combined_result: List[Optional[int]] = [None] * count
            for register_slice in slices:
                result = await self._client.read_holding_registers(address=register_slice.absolute_address, count=register_slice.count, slave=slave_param)
                if result.isError():
                    logging.error(f"Async modbus read error at address={register_slice.absolute_address}: {result}")
                    return False, None
                slice_data = result.registers
                combined_result[register_slice.relative_address : register_slice.relative_address + register_slice.count] = slice_data

            # Convert to List[int], replacing any remaining None values with 0
            final_result = [x if x is not None else 0 for x in combined_result]
            return True, final_result
        except Exception as e:
            logging.exception(f"Exception while reading holding registers async: {e}")
            return False, None

    async def write_register(self, value: int, address: int, check_connection: bool = True) -> bool:
        """Async method to write a value to the modbus server using async client."""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False
        try:
            if not self._client:
                logging.error(ASYNC_CLIENT_NOT_INITIALIZED)
                return False

            # Use slave parameter for async client
            slave_param = self._slave_id

            response = await self._client.write_registers(address=address, values=[value], slave=slave_param)
            if response.isError():
                logging.error(f"Error writing value={value} to register: {address}: {response}")
                return False
            return True
        except Exception as e:
            logging.exception(f"Exception while writing register async: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from modbus server using async client."""
        if self._client:
            self._client.close()
            self._is_connected = False

        # Also disconnect sync connector
        if hasattr(self._sync_connector, "client") and self._sync_connector.client:
            self._sync_connector.client.close()

    def get_connection_health(self) -> dict:
        """Return connection health metrics"""
        return {
            "is_connected": self.is_connected,
            "last_connection_attempt": self._last_connection_attempt,
            "connection_backoff": self._connection_backoff,
            "ip": self.ip,
            "port": self.port,
            "slave_id": self.slave_id,
        }
