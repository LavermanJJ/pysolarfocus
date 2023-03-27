from .base.enums import RegisterTypes
from .base.component import Component
from .base.data_value import DataValue

class FreshWaterModule(Component):
    def __init__(self, input_address=700) -> None:
        super().__init__(input_address)
        self.state = DataValue(address=0)
        