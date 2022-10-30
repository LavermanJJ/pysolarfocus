from .base.component import Component
from .base.enums import DataTypes,RegisterTypes
from .base.data_value import DataValue

class HeatPump(Component):
    def __init__(self) -> None:
        super().__init__(input_address=2300,holding_address=33404)
        self.supply_temperature = DataValue(address=0,multiplier=0.1)
        self.return_temperatur = DataValue(address=1,multiplier=0.1)
        self.flow_rate = DataValue(address=2)
        self.compressor_speed = DataValue(address=3)
        self.evu_lock_active = DataValue(address=4,type=DataTypes.UINT)
        self.defrost_active = DataValue(address=5,type=DataTypes.UINT)
        self.boiler_charge = DataValue(address=6, type=DataTypes.UINT)
        self.thermal_energy_total = DataValue(address=7,count=2,multiplier=0.001)
        self.thermal_energy_drinking_water = DataValue(address=9,count=2,multiplier=0.001)
        self.thermal_energy_heating = DataValue(address=11,count=2,multiplier=0.001)
        self.electrical_energy_total = DataValue(address=13,count=2,multiplier=0.001)
        self.electrical_energy_drinking_water = DataValue(address=15,count=2,multiplier=0.001)
        # spelling error kept for compatibility with HA-integraiton
        self.eletrical_energy_heating = DataValue(address=17,count=2,multiplier=0.001) 
        self.electrical_power = DataValue(address=19)
        self.thermal_power_cooling = DataValue(address=20)
        self.thermal_power_heating = DataValue(address=21)
        self.thermal_energy_cooling = DataValue(address=22,count=2,multiplier=0.001,type=DataTypes.UINT)
        self.electrical_energy_cooling = DataValue(address=24,count=2,multiplier=0.001,type=DataTypes.UINT)
        self.vampair_state = DataValue(address=26,type=DataTypes.UINT)
        
        self.evu_lock = DataValue(address=0,register_type=RegisterTypes.Holding)
        self.smart_grid = DataValue(address=1,register_type=RegisterTypes.Holding)
        self.outdoor_temperature_external = DataValue(address=2,multiplier=10,register_type=RegisterTypes.Holding)