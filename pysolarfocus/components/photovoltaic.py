"""Solarfocus photovoltaic component"""
from .. import ApiVersions
from .base.component import Component
from .base.data_value import DataValue
from .base.enums import RegisterTypes


class Photovoltaic(Component):
    def __init__(self, api_version: ApiVersions = ApiVersions.V_21_140) -> None:
        super().__init__(input_address=2500, holding_address=33407)
        self.power = DataValue(address=0, count=2)
        self.house_consumption = DataValue(address=2, count=2)
        self.heatpump_consumption = DataValue(address=4, count=2)
        self.grid_import = DataValue(address=6, count=2)
        self.grid_export = DataValue(address=8, count=2)

        if api_version.greater_or_equal(ApiVersions.V_21_140.value):
            self.overcharge_possible = DataValue(address=10, count=1)
            self.overcharge_active = DataValue(address=11, count=1)

        self.smart_meter = DataValue(address=0, register_type=RegisterTypes.HOLDING)
        self.photovoltaic = DataValue(address=1, register_type=RegisterTypes.HOLDING)
        self.grid_im_export = DataValue(address=2, register_type=RegisterTypes.HOLDING)
