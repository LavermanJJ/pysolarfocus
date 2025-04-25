"""Solarfocus circulation component"""
from .. import ApiVersions
from .base.component import Component
from .base.data_value import DataValue


class Circulation(Component):
    def __init__(self, input_address=900, api_version: ApiVersions = ApiVersions.V_25_030) -> None:
        super().__init__(input_address)

        if api_version.greater_or_equal(ApiVersions.V_25_030.value):
            self.temperature = DataValue(address=0, multiplier=0.1)
            self.pump = DataValue(address=1)
