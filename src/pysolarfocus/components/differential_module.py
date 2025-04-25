"""Solarfocus differential module component"""
from .. import ApiVersions
from .base.component import Component
from .base.data_value import DataValue
from .base.enums import DataTypes


class DifferentialModule(Component):
    def __init__(self, input_address=2200, api_version: ApiVersions = ApiVersions.V_25_030) -> None:
        super().__init__(input_address)

        if api_version.greater_or_equal(ApiVersions.V_25_030.value):
            self.relay_control_loop_o1 = DataValue(address=0, data_type=DataTypes.UINT)
            self.temperature_1_control_loop_1 = DataValue(address=1, multiplier=0.1)
            self.temperature_2_control_loop_1 = DataValue(address=2, multiplier=0.1)
            self.relay_control_loop_o2 = DataValue(address=3, data_type=DataTypes.UINT)
            self.temperature_1_control_loop_2 = DataValue(address=4, multiplier=0.1)
            self.temperature_2_control_loop_2 = DataValue(address=5, multiplier=0.1)
