"""Solarfocus heating circuit component"""
from .. import ApiVersions
from .base.component import Component
from .base.data_value import DataValue
from .base.enums import DataTypes, RegisterTypes


class HeatingCircuit(Component):
    def __init__(self, input_address=1100, holding_address=32600, api_version: ApiVersions = ApiVersions.V_23_010) -> None:
        super().__init__(input_address=input_address, holding_address=holding_address)
        self.supply_temperature = DataValue(address=0, multiplier=0.1)
        self.room_temperature = DataValue(address=1, multiplier=0.1)
        self.humidity = DataValue(address=2, multiplier=0.1)
        self.limit_thermostat = DataValue(address=3, data_type=DataTypes.UINT)
        self.circulator_pump = DataValue(address=4, data_type=DataTypes.UINT)
        self.mixer_valve = DataValue(address=5, data_type=DataTypes.UINT)
        self.state = DataValue(address=6, data_type=DataTypes.UINT)

        self.target_supply_temperature = DataValue(address=0, multiplier=10, register_type=RegisterTypes.HOLDING)
        self.cooling = DataValue(address=2, register_type=RegisterTypes.HOLDING)
        self.mode = DataValue(address=3, register_type=RegisterTypes.HOLDING)
        self.target_room_temperature = DataValue(address=5, multiplier=10, register_type=RegisterTypes.HOLDING)
        self.indoor_temperature_external = DataValue(address=6, multiplier=10, register_type=RegisterTypes.HOLDING)
        self.indoor_humidity_external = DataValue(address=7, multiplier=10, register_type=RegisterTypes.HOLDING)

        if api_version.greater_or_equal(ApiVersions.V_22_090.value):
            self.heating_mode = DataValue(address=8, register_type=RegisterTypes.HOLDING)


class TherminatorHeatingCircuit(HeatingCircuit):
    def __init__(self, input_address=1100, holding_address=32600, api_version: ApiVersions = ApiVersions.V_23_010) -> None:
        super().__init__(input_address, holding_address)
        # No idea, why this is offset by 1 ...
        self.circulator_pump = DataValue(address=5, data_type=DataTypes.UINT)
        self.mixer_valve = DataValue(address=6, data_type=DataTypes.UINT)
        self.state = DataValue(address=7, data_type=DataTypes.UINT)
