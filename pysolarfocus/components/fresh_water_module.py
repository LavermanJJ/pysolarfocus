from .base.enums import RegisterTypes
from .base.component import Component
from .base.data_value import DataValue

class FreshWaterModule(Component):
    def __init__(self, input_address=700, holding_address=32003) -> None:
        super().__init__(input_address, holding_address)
        self.state = DataValue(address=0)
        
        self.circulation = DataValue(address=0,register_type=RegisterTypes.Holding)