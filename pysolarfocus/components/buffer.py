from .base.component import Component
from .base.enums import DataTypes,RegisterTypes
from .base.data_value import DataValue

class Buffer(Component):
    def __init__(self) -> None:
        super().__init__(1900, 5)
        self.top_temperature = DataValue(address=0,multiplier=0.1)
        self.bottom_temperature = DataValue(address=1,multiplier=0.1)
        self.pump = DataValue(address=2)
        self.state = DataValue(address=3,type=DataTypes.UINT)
        self.mode = DataValue(address=4,type=DataTypes.UINT)
        
        self._initialize_addresses()