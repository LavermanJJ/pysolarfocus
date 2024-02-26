"""Solarfocus fresh water module component"""
from .. import ApiVersions
from .base.component import Component
from .base.data_value import DataValue


class FreshWaterModule(Component):
    def __init__(self, input_address=700, api_version: ApiVersions = ApiVersions.V_23_020) -> None:
        super().__init__(input_address)
        self.state = DataValue(address=0)

        if api_version.greater_or_equal(ApiVersions.V_23_040.value):
            self.supply_temperature = DataValue(address=1, count=1)
            self.flow_rate = DataValue(address=2, count=1)
            self.target_temperature = DataValue(address=3, count=1)
            self.valve = DataValue(address=4, count=1)
