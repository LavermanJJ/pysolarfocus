from .base.component import Component
from .base.enums import DataTypes
from .base.data_value import DataValue

class Solar(Component):
    def __init__(self) -> None:
        super().__init__(input_address=2100)
        self.collector_temperature_1 = DataValue(address=0,multiplier=0.1)
        self.collector_temperature_2 = DataValue(address=1,multiplier=0.1)
        self.collector_supply_temperature = DataValue(address=2,multiplier=0.1)
        self.collector_return_temperature = DataValue(address=3,multiplier=0.1)
        self.flow_heat_meter = DataValue(address=4,multiplier=0.1)
        self.curent_power = DataValue(address=5,multiplier=0.1)
        self.curent_yield_heat_meter = DataValue(address=6,count=2)
        self.today_yield = DataValue(address=8,count=2)
        self.buffer_sensor_1 = DataValue(address=10,multiplier=0.1)
        self.buffer_sensor_2 = DataValue(address=11,multiplier=0.1)
        self.buffer_sensor_3 = DataValue(address=12,multiplier=0.1)
        self.state = DataValue(address=13,type=DataTypes.UINT)
         