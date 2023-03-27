from .base.component import Component
from .base.enums import DataTypes, RegisterTypes
from .base.data_value import DataValue
from .. import ApiVersions

class PelletsBoiler(Component):
    def __init__(self,input_address=2400,holding_address=-1,api_version:ApiVersions=ApiVersions.V_21_140) -> None:
        
        if api_version.value >= ApiVersions.V_22_090.value:
            holding_address=33400
        
        super().__init__(input_address, holding_address)
        self.temperature = DataValue(address=0,multiplier=0.1)
        self.status  = DataValue(address=1,type=DataTypes.UINT)
        self.message_number = DataValue(address=4)
        self.door_contact = DataValue(address=5)
        self.cleaning = DataValue(address=6)
        self.ash_container = DataValue(address=7)
        self.outdoor_temperature = DataValue(address=8,multiplier=0.1)
        self.boiler_operating_mode = DataValue(address=9)
        self.octoplus_buffer_temperature_bottom = DataValue(address=10,multiplier=0.1)
        self.octoplus_buffer_temperature_top = DataValue(address=11,multiplier=0.1)
        self.log_wood = DataValue(address=12,type=DataTypes.UINT)
        
        if api_version.value >= ApiVersions.V_22_090.value:
            self.sweep_function_start_stop = DataValue(address=10,register_type=RegisterTypes.Holding)
            self.sweep_function_extend = DataValue(address=11,register_type=RegisterTypes.Holding)

        if api_version.value >= ApiVersions.V_23_010.value:
            self.pellet_usage_last_fill = DataValue(address=14,count=2,multiplier=0.1)
            self.pellet_usage_total = DataValue(address=16,count=2,multiplier=0.1)
            self.heat_energy_total = DataValue(address=18,count=2,multiplier=0.1)            

            self.pellet_usage_reset = DataValue(address=12,register_type=RegisterTypes.Holding)