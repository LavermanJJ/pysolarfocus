"""Solarfocus buffer component"""

from .. import ApiVersions
from .base.component import Component
from .base.data_value import DataValue
from .base.enums import DataTypes, RegisterTypes


class Buffer(Component):
    def __init__(self, input_address: int = 1900, holding_address=-1, api_version: ApiVersions = ApiVersions.V_21_140) -> None:

        super().__init__(input_address, holding_address)

        self.top_temperature = DataValue(address=0, multiplier=0.1)
        self.bottom_temperature = DataValue(address=1, multiplier=0.1)
        self.pump = DataValue(address=2)
        self.state = DataValue(address=3, data_type=DataTypes.UINT)
        self.mode = DataValue(address=4, data_type=DataTypes.UINT)

        if api_version.greater_or_equal(ApiVersions.V_22_090.value):
            self.external_top_temperature_x44 = DataValue(address=0, multiplier=10, register_type=RegisterTypes.HOLDING)
            self.external_middle_temperature_x36 = DataValue(address=1, multiplier=10, register_type=RegisterTypes.HOLDING)
            self.external_bottom_temperature_x35 = DataValue(address=2, multiplier=10, register_type=RegisterTypes.HOLDING)


class TherminatorBuffer(Buffer):
    def __init__(self, address: int = 1900) -> None:
        super().__init__(input_address=address)
        self.x35_temperature = DataValue(address=2, multiplier=0.1)
        self.pump = DataValue(address=3)
        self.state = DataValue(address=4, data_type=DataTypes.UINT)
        self.mode = DataValue(address=5, data_type=DataTypes.UINT)
