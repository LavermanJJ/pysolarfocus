"""Python client lib for Solarfocus"""
__version__ = "0.99.0"

from enum import Enum

#Default port for modbus
PORT = 502

#This needs to be defined before the imports because of circular dependencies
class Systems(str, Enum):
    """
    Supported systems by this library
    """
    Vampair = "Vampair"
    Therminator = "Therminator" 
    
from .modbus_wrapper import ModbusConnector
from .component_factory import ComponentFactory
from .const import SLAVE_ID

class SolarfocusAPI:
    """Solarfocus Heating System"""
    
    @property
    def system(self): 
        return self._system
    
    def __init__(self,
                 ip:str,
                 heating_circuit_count:int = 1,
                 buffer_count:int = 1,
                 boiler_count:int = 1,
                 system:Systems=Systems.Vampair,
                 port:int=PORT,
                 slave_id:int=SLAVE_ID):
        """Initialize Solarfocus communication."""
        assert heating_circuit_count >= 0 and heating_circuit_count < 9, "Heating circuit count must be between 0 and 8"
        assert buffer_count >= 0 and buffer_count < 5, "Buffer count must be between 0 and 4"
        assert boiler_count >= 0 and boiler_count < 5, "Boiler count must be between 0 and 4"
        
        self.__conn = ModbusConnector(ip,port,slave_id)
        self.__factory = ComponentFactory(self.__conn)
        #Lists of components
        self.heating_circuits = self.__factory.heating_circuit(system,heating_circuit_count) if heating_circuit_count > 0 else []
        self.boilers = self.__factory.boiler(system,boiler_count) if boiler_count > 0 else []
        self.buffers = self.__factory.buffer(system,buffer_count) if buffer_count > 0 else []
        #Single components
        self.heatpump = self.__factory.heatpump(system)
        self.photovoltaic = self.__factory.photovoltaic(system)
        self.pelletsboiler = self.__factory.pelletsboiler(system)
        self._slave_id = slave_id
        self._system = system
    
    def connect(self):
        """Connect to Solarfocus eco manager-touch"""
        return self.__conn.connect()

    @property
    def is_connected(self)->bool:
        """Check if connection is established"""
        return self.__conn.is_connected
    
    def update(self):
        """Read values from Heating System"""
        if (
            self.update_heating()
            and self.update_buffer()
            and self.update_boiler()
            and self.update_heatpump()
            and self.update_photovoltaic()
            and self.update_pelletsboiler()
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

    def update_heatpump(self) -> bool:
        """Read values from Heating System"""
        return self.heatpump.update()

    def update_photovoltaic(self) -> bool:
        """Read values from Heating System"""
        return self.photovoltaic.update()

    def update_pelletsboiler(self) -> bool:
        """Read values from Pellets boiler"""
        return self.pelletsboiler.update()