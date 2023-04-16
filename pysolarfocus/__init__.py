"""Python client lib for Solarfocus"""
__version__ = "3.6.4"

from enum import Enum
from packaging import version

#Default port for modbus
PORT = 502

#This needs to be defined before the imports because of circular dependencies
class Systems(str, Enum):
    """
    Supported systems by this library
    """
    Vampair = "Vampair"
    Therminator = "Therminator" 
    
class ApiVersions(str, Enum):
    """
    Supported Solarfocus API versions by this library
    """
    V_21_140 = "21.140"
    V_22_090 = "22.090"
    V_23_010 = "23.010"
    V_23_020 = "23.020"
    
    def greater_or_equal(self, api_version)->bool:
        return version.parse(self.value) >= version.parse(api_version)
    
    
from .modbus_wrapper import ModbusConnector
from .component_factory import ComponentFactory
from .const import SLAVE_ID

class SolarfocusAPI:
    """Solarfocus Heating System"""
    
    @property
    def system(self) -> Systems: 
        return self._system
    
    @property
    def api_version(self) -> ApiVersions: 
        return self._api_version
    
    def __init__(self,
                 ip:str,
                 heating_circuit_count:int = 1,
                 buffer_count:int = 1,
                 boiler_count:int = 1,
                 fresh_water_module_count:int = 1,
                 system:Systems=Systems.Vampair,
                 port:int=PORT,
                 slave_id:int=SLAVE_ID,
                 api_version:ApiVersions=ApiVersions.V_21_140):
        """Initialize Solarfocus communication."""
        assert heating_circuit_count >= 0 and heating_circuit_count < 9, "Heating circuit count must be between 0 and 8"
        assert buffer_count >= 0 and buffer_count < 5, "Buffer count must be between 0 and 4"
        assert boiler_count >= 0 and boiler_count < 5, "Boiler count must be between 0 and 4"
        assert fresh_water_module_count >= 0 and fresh_water_module_count < 5, "Fresh water module count must be between 0 and 4"
        
        self.__conn = ModbusConnector(ip,port,slave_id)
        self.__factory = ComponentFactory(self.__conn)
        self._slave_id = slave_id
        self._system = system
        self._api_version = api_version
        
        #Lists of components
        self.heating_circuits = self.__factory.heating_circuit(system,heating_circuit_count)
        self.boilers = self.__factory.boiler(system,boiler_count)
        self.buffers = self.__factory.buffer(system,buffer_count,api_version)
        if self._api_version.greater_or_equal(ApiVersions.V_23_020.value):
            self.fresh_water_modules = self.__factory.fresh_water_modules(system,fresh_water_module_count)
        
        #Single components
        self.heatpump = self.__factory.heatpump(system)
        self.photovoltaic = self.__factory.photovoltaic(system)
        self.pelletsboiler = self.__factory.pelletsboiler(system,api_version)
        self.solar = self.__factory.solar(system)

       
    
    def connect(self):
        """Connect to Solarfocus eco manager-touch"""
        return self.__conn.connect()

    @property
    def is_connected(self)->bool:
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
            and self.update_pelletsboiler()
            and self.update_solar()
            and self.update_fresh_water_modules()
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

    def update_heatpump(self) -> bool:
        """Read values from Heating System"""
        return self.heatpump.update()

    def update_photovoltaic(self) -> bool:
        """Read values from Heating System"""
        return self.photovoltaic.update()

    def update_pelletsboiler(self) -> bool:
        """Read values from Pellets boiler"""
        return self.pelletsboiler.update()
    
    def update_solar(self) -> bool:
        """Read values from Solar"""
        return self.solar.update()
    
    
    def __repr__(self) -> str:
        s = ["-"*50]
        s.append(f"{self.__class__.__name__}, v{__version__}")
        s.append("-"*50)
        s.append(f"+ System: {self.system.name}")
        s.append(f"+ Version: {self._api_version}")
        s.append("-"*50)
        return "\n".join(s)
