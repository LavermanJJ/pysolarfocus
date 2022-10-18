from .enums import RegisterTypes,DataTypes

class DataValue(object):
    """
    Abstraction of a certain relative address in the modbus register
    """
    type:DataTypes
    address:int
    count:int
    value:int
    multiplier:float
    _absolut_address:int
    register_type:RegisterTypes
    def __init__(self,address:int,count:int=1,default_value:int=0,multiplier:float=None,type:DataTypes=DataTypes.INT,register_type:RegisterTypes=RegisterTypes.Input) -> None:
        self.address = address
        self.count = count
        self.value = default_value
        self.multiplier = multiplier
        self.type = type
        self._absolut_address = None # This will be set by the parent component
        self.register_type = register_type
        
    def get_absolute_address(self)->int:
        """
        Returns the absolute address of the register
        """
        if not self._absolut_address:
            raise Exception("Absolute address not set!")
        return self._absolut_address + self.address  
    
    @property
    def has_scaler(self)->bool:
        return  self.multiplier is not None
    
    @property
    def scaled_value(self)->float:
        """
        Scaled value of this register
        """
        if self.has_scaler:
            return self.value * self.multiplier
        else:
            return self.value
        
    @property
    def reverse_scaled_value(self)->float:
        """
        Scaled value of this register
        """
        if self.has_scaler:
            return self.value / self.multiplier
        else:
            return self.value
       
    def reverse_scale(self,value:float)->float:
        """
        Applies the scaler in the reverse direction
        """
        if self.has_scaler:
            return value / self.multiplier
        else:
            return value
        
    def set_unscaled_value(self,value:float)->None:
        """
        Applies the scaler to the value and sets the value
        """
        self.value = self.reverse_scale(value)