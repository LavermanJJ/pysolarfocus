from .base.component import Component
from .base.enums import DataTypes
from .base.data_value import DataValue

class PelletsBoiler(Component):
    def __init__(self) -> None:
        super().__init__(2400)
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