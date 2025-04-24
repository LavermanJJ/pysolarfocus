"""Solarfocus solar component"""
from .. import ApiVersions
from .base.component import Component
from .base.data_value import DataValue
from .base.enums import DataTypes


class Solar(Component):
    def __init__(self, input_address=2100, api_version: ApiVersions = ApiVersions.V_20_110) -> None:
        super().__init__(input_address)
        self.collector_temperature_1 = DataValue(address=0, multiplier=0.1)
        self.collector_temperature_2 = DataValue(address=1, multiplier=0.1)
        self.collector_supply_temperature = DataValue(address=2, multiplier=0.1)
        self.collector_return_temperature = DataValue(address=3, multiplier=0.1)
        self.flow_heat_meter = DataValue(address=4, multiplier=0.1)
        self.current_power = DataValue(address=5, multiplier=0.1)
        self.current_yield_heat_meter = DataValue(address=6, count=2)
        self.today_yield = DataValue(address=8, count=2)
        self.buffer_sensor_1 = DataValue(address=10, multiplier=0.1)
        self.buffer_sensor_2 = DataValue(address=11, multiplier=0.1)
        self.buffer_sensor_3 = DataValue(address=12, multiplier=0.1)
        self.state = DataValue(address=13, data_type=DataTypes.UINT)

        if api_version.greater_or_equal(ApiVersions.V_25_030.value):
            self.relay_o1 = DataValue(address=14, data_type=DataTypes.UINT)
            self.control_out_1 = DataValue(address=15, data_type=DataTypes.UINT)
            self.relay_o2 = DataValue(address=16, data_type=DataTypes.UINT)
            self.control_out_2 = DataValue(address=17, data_type=DataTypes.UINT)
