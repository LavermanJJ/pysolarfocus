from .base.component import Component
from .base.enums import DataTypes,RegisterTypes
from .base.data_value import DataValue

class HeatingCircuit(Component):
    def __init__(self,input_address=1100,holding_address=32600) -> None:
        super().__init__(input_address=input_address,holding_address=holding_address)
        self.supply_temperature = DataValue(address=0,multiplier=0.1)
        self.room_temperature = DataValue(address=1,multiplier=0.1)
        self.humidity = DataValue(address=2,multiplier=0.1)
        self.limit_thermostat = DataValue(address=3,type=DataTypes.UINT)
        self.circulator_pump = DataValue(address=4,type=DataTypes.UINT)
        self.mixer_valve = DataValue(address=5,type=DataTypes.UINT)
        self.state = DataValue(address=6,type=DataTypes.UINT)
        
        self.target_supply_temperature = DataValue(address=0,multiplier=10,register_type=RegisterTypes.Holding)
        self.cooling = DataValue(address=2,register_type=RegisterTypes.Holding)
        self.mode = DataValue(address=3,register_type=RegisterTypes.Holding)
        self.target_room_temperatur = DataValue(address=5,multiplier=10,register_type=RegisterTypes.Holding)
        self.indoor_temperatur_external = DataValue(address=6,multiplier=10,register_type=RegisterTypes.Holding)
        self.indoor_humidity_external = DataValue(address=7,register_type=RegisterTypes.Holding)
        
class TherminatorHeatingCircuit(HeatingCircuit):
    def __init__(self, input_address=1100, holding_address=32600) -> None:
        super().__init__(input_address, holding_address)
        # No idea, why this is offset by 1 ... 
        self.circulator_pump = DataValue(address=5,type=DataTypes.UINT)
        self.mixer_valve = DataValue(address=6,type=DataTypes.UINT)
        self.state = DataValue(address=7,type=DataTypes.UINT)