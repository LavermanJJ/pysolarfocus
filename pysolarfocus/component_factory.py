from .components.heating_circuit import *
from .components.boiler import *
from .components.heat_pump import *
from .components.buffer import *
from .components.pellets_boiler import *
from .components.photovoltaic import *
from .modbus_wrapper import ModbusConnector
from . import Systems


class ComponentFactory:
    def __init__(self,modbus_connector:ModbusConnector) -> None:
        self.__modbus_connector = modbus_connector
        
    def heating_circuit(self, system:Systems)->HeatingCircuit:
        if system == Systems.Therminator:
            return TherminatorHeatingCircuit()._initialize(self.__modbus_connector)
        return HeatingCircuit()._initialize(self.__modbus_connector)
    
    def boiler(self, system:Systems)->Boiler:
        return Boiler()._initialize(self.__modbus_connector)
    
    def heatpump(self, system:Systems)->HeatPump:
        return HeatPump()._initialize(self.__modbus_connector)
    
    def photovoltaic(self, system:Systems)->Photovoltaic:
        return Photovoltaic()._initialize(self.__modbus_connector)
    
    def pelletsboiler(self, system:Systems)->PelletsBoiler:
        return PelletsBoiler()._initialize(self.__modbus_connector)
    
    def buffer(self, system:Systems)->Buffer:
        if system == Systems.Therminator:
            return TherminatorBuffer()._initialize(self.__modbus_connector)
        else:
            return Buffer()._initialize(self.__modbus_connector)