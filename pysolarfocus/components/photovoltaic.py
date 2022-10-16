from .base.component import Component
from .base.enums import RegisterTypes
from .base.data_value import DataValue

class Photovoltaic(Component):
    def __init__(self) -> None:
        super().__init__(input_address=2500, holding_address=33407)
        self.power = DataValue(address=0,count=2)
        self.house_consumption = DataValue(address=2,count=2)
        self.heatpump_consumption = DataValue(address=4,count=2)
        self.grid_import = DataValue(address=6,count=2)
        self.grid_export = DataValue(address=8,count=2)
        
        self.smart_meter = DataValue(address=0,register_type=RegisterTypes.Holding)
        self.photovoltaic = DataValue(address=1,register_type=RegisterTypes.Holding)
        self.grid_im_export = DataValue(address=2,register_type=RegisterTypes.Holding)