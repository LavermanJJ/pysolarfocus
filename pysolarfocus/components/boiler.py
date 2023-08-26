"""Solarfocus boiler component"""

from .base.component import Component
from .base.data_value import DataValue
from .base.enums import DataTypes, RegisterTypes


class Boiler(Component):
    def __init__(self, input_address: int = 500, holding_address: int = 32000) -> None:
        super().__init__(input_address=input_address, holding_address=holding_address)
        self.temperature = DataValue(address=0, multiplier=0.1)
        self.state = DataValue(address=1, data_type=DataTypes.UINT)
        self.mode = DataValue(address=2, data_type=DataTypes.UINT)

        self.target_temperature = DataValue(address=0, multiplier=10, register_type=RegisterTypes.HOLDING)
        self.single_charge = DataValue(address=1, register_type=RegisterTypes.HOLDING)
        self.holding_mode = DataValue(address=2, register_type=RegisterTypes.HOLDING)
        self.circulation = DataValue(address=3, register_type=RegisterTypes.HOLDING)
