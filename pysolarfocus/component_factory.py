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
            return TherminatorHeatingCircuit()
        return HeatingCircuit()
    
    @staticmethod
    def boiler(system:Systems)->Boiler:
        return Boiler()
    
    @staticmethod
    def heatpump(system:Systems)->HeatPump:
        return HeatPump()
    
    @staticmethod
    def photovoltaic(system:Systems)->Photovoltaic:
        return Photovoltaic()
    
    @staticmethod
    def pelletsboiler(system:Systems)->PelletsBoiler:
        return PelletsBoiler()
    
    @staticmethod
    def buffer(system:Systems)->Buffer:
        if system == Systems.Therminator:
            return TherminatorBuffer()
        else:
            return Buffer()