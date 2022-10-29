from .base.component import Component
from .base.enums import DataTypes
from .base.data_value import DataValue

class Buffer(Component):
    def __init__(self,address:int=1900) -> None:
        super().__init__(address)
        self.top_temperature = DataValue(address=0,multiplier=0.1)
        self.bottom_temperature = DataValue(address=1,multiplier=0.1)
        self.pump = DataValue(address=2)
        self.state = DataValue(address=3,type=DataTypes.UINT)
        self.mode = DataValue(address=4,type=DataTypes.UINT)
        
        
class TherminatorBuffer(Buffer):
    def __init__(self,address:int=1900) -> None:
        super().__init__(address=address)
        self.x35_temperature = DataValue(address=2,multiplier=0.1)
        self.pump = DataValue(address=3)
        self.state = DataValue(address=4,type=DataTypes.UINT)
        self.mode = DataValue(address=5,type=DataTypes.UINT)
        