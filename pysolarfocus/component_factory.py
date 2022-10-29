from pysolarfocus.components.solar import Solar
from .components.heating_circuit import *
from .components.boiler import *
from .components.heat_pump import *
from .components.buffer import *
from .components.pellets_boiler import *
from .components.photovoltaic import *
from . import Systems


class ComponentFactory:
    @staticmethod
    def heating_circuit(system:Systems)->HeatingCircuit:
        if system == Systems.Therminator:
            return TherminatorHeatingCircuit()._initialize()
        return HeatingCircuit()._initialize()
    
    @staticmethod
    def boiler(system:Systems)->Boiler:
        return Boiler()._initialize()
    
    @staticmethod
    def heatpump(system:Systems)->HeatPump:
        return HeatPump()._initialize()
    
    @staticmethod
    def photovoltaic(system:Systems)->Photovoltaic:
        return Photovoltaic()._initialize()
    
    @staticmethod
    def pelletsboiler(system:Systems)->PelletsBoiler:
        return PelletsBoiler()._initialize()
    
    @staticmethod
    def solar(system:Systems)->Solar:
        return Solar()._initialize()
    
    @staticmethod
    def buffer(system:Systems)->Buffer:
        if system == Systems.Therminator:
            return TherminatorBuffer()._initialize()
        else:
            return Buffer()._initialize()