"""Solarfocus modbus wrapper"""
import logging
import time
from typing import List, Optional, Tuple

try:
    # modbus version < 3.0
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient

    IS_LEGACY_VERSION = True
    IS_VERSION_3_10 = False
    
except ImportError:
    from pymodbus.client import ModbusTcpClient as ModbusClient

    IS_LEGACY_VERSION = False

    # modbus version >= 3.0 <= 3.10
    try:
        from pymodbus.datastore.context import ModbusDeviceContext

        IS_VERSION_3_10 = True
    except ImportError:
        IS_VERSION_3_10 = False


from .components.base.register_slice import RegisterSlice
from .exceptions import ModbusConnectionError, RegisterReadError, RegisterWriteError


class ModbusConnector:
    """
    Helper methods to read/write data to a modbus server with retry logic and better error handling
    """

    def __init__(self, ip: str, port: int, slave_id: int, retry_count: int = 3, retry_delay: float = 1.0) -> None:
        """Initialize ModbusConnector.

        Args:
            ip: IP address of the modbus server
            port: Port number for modbus communication
            slave_id: Slave ID for modbus communication
            retry_count: Number of retries for failed operations
            retry_delay: Delay between retries in seconds
        """
        self.ip = ip
        self.port = port
        self.slave_id = slave_id
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.client = ModbusClient(ip, port=port)
        self.__slave_args = {"unit": slave_id} if IS_LEGACY_VERSION else {"device_id": slave_id} if IS_VERSION_3_10 else {"slave": slave_id}

    @property
    def is_connected(self) -> bool:
        """Check if connection is established."""
        return self.client.is_socket_open()

    def connect(self) -> bool:
        """Connect to modbus server with retry logic."""
        for attempt in range(self.retry_count):
            try:
                if self.client.connect():
                    logging.info(f"Successfully connected to modbus server at {self.ip}:{self.port}")
                    return True
                else:
                    logging.warning(f"Connection attempt {attempt + 1} failed")
                    if attempt < self.retry_count - 1:
                        time.sleep(self.retry_delay)
            except Exception as e:
                logging.error(f"Connection attempt {attempt + 1} failed with exception: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)

        logging.error(f"Failed to connect to modbus server at {self.ip}:{self.port} after {self.retry_count} attempts")
        return False

    def read_input_registers(self, slices: List[RegisterSlice], count: int, check_connection: bool = True) -> Tuple[bool, Optional[List[int]]]:
        """Internal method to read input registers from modbus"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False, None
        try:
            combined_result: List[Optional[int]] = [None] * count
            for register_slice in slices:
                result = self.client.read_input_registers(address=register_slice.absolute_address, count=register_slice.count, **self.__slave_args)
                if result.isError():
                    logging.error(f"Modbus read error at address={register_slice.absolute_address}, count={register_slice.count}: {result}")
                    return False, None
                slice_data = result.registers
                combined_result[register_slice.relative_address : register_slice.relative_address + register_slice.count] = slice_data
            # Convert to List[int], replacing any remaining None values with 0
            final_result = [x if x is not None else 0 for x in combined_result]
            return True, final_result
        except Exception as e:
            logging.exception(f"Exception while reading input registers for address: '{slices[0].absolute_address}': {e}")
            return False, None

    def read_holding_registers(self, slices: List[RegisterSlice], count: int, check_connection: bool = True) -> Tuple[bool, Optional[List[int]]]:
        """Internal method to read holding registers from modbus"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False, None
        try:
            combined_result: List[Optional[int]] = [None] * count
            for register_slice in slices:
                result = self.client.read_holding_registers(address=register_slice.absolute_address, count=register_slice.count, **self.__slave_args)
                if result.isError():
                    logging.error(f"Modbus read error at address={register_slice.absolute_address}: {result}")
                    return False, None
                slice_data = result.registers
                combined_result[register_slice.relative_address : register_slice.relative_address + register_slice.count] = slice_data
            # Convert to List[int], replacing any remaining None values with 0
            final_result = [x if x is not None else 0 for x in combined_result]
            return True, final_result
        except Exception as e:
            logging.exception(f"Exception while reading holding registers for address: '{slices[0].absolute_address}': {e}")
            return False, None

    def write_register(self, value: int, address: int, check_connection: bool = True) -> bool:
        """Write a value to the modbus server"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False
        try:
            response = self.client.write_registers(address, [value], **self.__slave_args)
            if response.isError():
                logging.error(f"Error writing value={value} to register: {address}: {response}")
                return False
        except Exception as e:
            logging.exception(f"Exception while writing value={value} to register: {address}: {e}")
            return False
        return True
