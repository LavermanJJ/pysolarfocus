import logging
try:
    #modbus version < 3.0
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient
    IS_LEGACY_VERSION = True
except:
    #modbus version >= 3.0
    from pymodbus.client import ModbusTcpClient as ModbusClient
    IS_LEGACY_VERSION = False
from .components.base.register_slice import RegisterSlice
  
class ModbusConnector():
    """
    Helper methodes to read/write data to a modbus server
    """
    def __init__(self,ip:str,port:int,slave_id:int) -> None:
        self.ip = ip
        self.port = port
        self.slave_id = slave_id
        self.client = ModbusClient(ip,port=port)
        self.__slave_args = {"unit":slave_id} if IS_LEGACY_VERSION else {"slave":slave_id}
        
    @property
    def is_connected(self)->bool:
        return self.client.is_socket_open()
    
    def connect(self)->bool:
        return self.client.connect()

  
    def read_input_registers(self,slices:list[RegisterSlice],count:int,check_connection:bool=True)->tuple[bool,list[int]]:
        """Internal methode to read input registers from modbus"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False, None
        try:
            combined_result = [None] * count
            for registerSlice in slices:
                result = self.client.read_input_registers(address=registerSlice.absolute_address,count=registerSlice.count, **self.__slave_args)
                if result.isError():
                    logging.error(f"Modbus read error at address={registerSlice.absolute_address}, count={registerSlice.count}: {result}")
                    return False, None
                slice_data = result.registers
                combined_result[registerSlice.relative_address:registerSlice.relative_address+registerSlice.count] = slice_data
            return True, combined_result
        except Exception:
            logging.exception(f"Exception while reading input registers for address: '{slices[0].absolute_address}'!")
            return False, None
     
    def read_holding_registers(self,slices:list[RegisterSlice],count:int, check_connection:bool = True)->tuple[bool,list[int]]:
        """Internal methode to read holding registers from modbus"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False, None
        try:
            combined_result = [None] * count
            for registerSlice in slices:
                result = self.client.read_holding_registers(address=registerSlice.absolute_address,count=registerSlice.count, **self.__slave_args)
                if result.isError():
                    logging.error(f"Modbus read error at address={registerSlice.absolute_address}: {result}")
                    return False, None
                slice_data = result.registers
                combined_result[registerSlice.relative_address:registerSlice.relative_address+registerSlice.count] = slice_data
            return True, combined_result
        except Exception:
            logging.exception(f"Exception while reading holding registers for address: '{slices[0].absolute_address}'!")
            return False, None
           
    def write_register(self,value:int, address:int, check_connection:bool = True) -> bool:
        """Write a value to the modbus server"""
        if check_connection and not self.is_connected:
            logging.error("Connection to modbus is not established!")
            return False
        try:
            response = self.client.write_registers(address, [value], **self.__slave_args)
            if response.isError():
                logging.error(f"Error writing value={value} to register: {address}: {response}")
                return False
        except Exception:
            logging.exception(f"Eception while writing value={value} to register: {address}!")
            return False
        return True
        
        
        