"""Solarfocus heat pump component"""

from .. import ApiVersions
from .base.component import Component
from .base.data_value import DataValue
from .base.enums import DataTypes, RegisterTypes
from .base.performance_calculator import PerformanceCalculator


class HeatPump(Component):
    def __init__(self, api_version: ApiVersions = ApiVersions.V_21_140) -> None:
        super().__init__(input_address=2300, holding_address=33404)
        self.supply_temperature = DataValue(address=0, multiplier=0.1)
        self.return_temperature = DataValue(address=1, multiplier=0.1)
        self.flow_rate = DataValue(address=2)
        self.compressor_speed = DataValue(address=3)
        self.evu_lock_active = DataValue(address=4, data_type=DataTypes.UINT)

        if api_version.greater_or_equal(ApiVersions.V_25_030.value):
            self.defrost_active = DataValue(address=6, data_type=DataTypes.UINT)
            self.boiler_charge = DataValue(address=7, data_type=DataTypes.UINT)
            self.thermal_energy_total = DataValue(address=10, count=2, multiplier=0.001)
            self.thermal_energy_drinking_water = DataValue(address=12, count=2, multiplier=0.001)
            self.thermal_energy_heating = DataValue(address=14, count=2, multiplier=0.001)
            self.electrical_energy_total = DataValue(address=16, count=2, multiplier=0.001)
            self.electrical_energy_drinking_water = DataValue(address=18, count=2, multiplier=0.001)
            self.electrical_energy_heating = DataValue(address=20, count=2, multiplier=0.001)
            self.electrical_power = DataValue(address=22)
            self.thermal_power_cooling = DataValue(address=23)
            self.thermal_power_heating = DataValue(address=24)
            self.thermal_energy_cooling = DataValue(address=26, count=2, multiplier=0.001, data_type=DataTypes.UINT)
            self.electrical_energy_cooling = DataValue(address=28, count=2, multiplier=0.001, data_type=DataTypes.UINT)

            self.vampair_state = DataValue(address=30, data_type=DataTypes.UINT)
        else:
            self.defrost_active = DataValue(address=5, data_type=DataTypes.UINT)
            self.boiler_charge = DataValue(address=6, data_type=DataTypes.UINT)
            self.thermal_energy_total = DataValue(address=7, count=2, multiplier=0.001)
            self.thermal_energy_drinking_water = DataValue(address=9, count=2, multiplier=0.001)
            self.thermal_energy_heating = DataValue(address=11, count=2, multiplier=0.001)
            self.electrical_energy_total = DataValue(address=13, count=2, multiplier=0.001)
            self.electrical_energy_drinking_water = DataValue(address=15, count=2, multiplier=0.001)
            self.electrical_energy_heating = DataValue(address=17, count=2, multiplier=0.001)
            self.electrical_power = DataValue(address=19)
            self.thermal_power_cooling = DataValue(address=20)
            self.thermal_power_heating = DataValue(address=21)
            self.thermal_energy_cooling = DataValue(address=22, count=2, multiplier=0.001, data_type=DataTypes.UINT)
            self.electrical_energy_cooling = DataValue(address=24, count=2, multiplier=0.001, data_type=DataTypes.UINT)

            self.vampair_state = DataValue(address=26, data_type=DataTypes.UINT)

        # This register is shared with the biomass boiler
        self.outdoor_temperature = DataValue(address=108, multiplier=0.1)

        self.evu_lock = DataValue(address=0, register_type=RegisterTypes.HOLDING)
        self.smart_grid = DataValue(address=1, register_type=RegisterTypes.HOLDING)
        self.outdoor_temperature_external = DataValue(address=2, multiplier=10, register_type=RegisterTypes.HOLDING)

        self.cop_heating = PerformanceCalculator(self.thermal_power_heating, self.electrical_power)
        self.cop_cooling = PerformanceCalculator(self.thermal_power_cooling, self.electrical_power)
        self.performance_overall = PerformanceCalculator(self.thermal_energy_total, self.electrical_energy_total)
        self.performance_overall_heating = PerformanceCalculator(self.thermal_energy_heating, self.electrical_energy_heating)
        self.performance_overall_drinking_water = PerformanceCalculator(self.thermal_energy_drinking_water, self.electrical_energy_drinking_water)
