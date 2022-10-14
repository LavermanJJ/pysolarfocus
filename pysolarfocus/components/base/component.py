from .enums import RegisterTypes,DataTypes
from .data_value import DataValue
import logging

class Component(object):
    def __init__(self,input_address:int,holding_address:int=-1)->None:
        self.input_address = input_address
        self.input_count = 0
        self.holding_address = holding_address
        self.holding_count = 0
        self.__data_values = None
        
    def _initialize(self)->None:
        """
        Initializes the absolute addresses of the DataValues and the count of the Component
        """
        for _,value in self.__get_data_values():
            if value.register_type == RegisterTypes.Input:
                value._absolut_address = self.input_address
            else:
                value._absolut_address = self.holding_address
          
        #Dynamically calcuate how many registers have to be read  
        if len(self.__get_input_values()) > 0:    
            last_input_value = max([v for _,v in self.__get_input_values()],key=lambda item: item.address)
            self.input_count = last_input_value.address+last_input_value.count
        
        if len(self.__get_holding_values()) > 0:
            last_holding_value = max([v for _,v in self.__get_holding_values()],key=lambda item: item.address)
            self.holding_count = last_holding_value.address+last_holding_value.count
                
    @property
    def has_input_address(self)->bool:
        return self.input_address >= 0 and self.input_count > 0
    
    @property
    def has_holding_address(self)->bool:
        return self.holding_address >= 0 and self.holding_count > 0
       
    def _reset(self):
        """
        Resets the DataValues of this Component
        """
        self.__data_values = None
            
    def __get_data_values(self)->list[tuple[str,DataValue]]:
        """
        Returns all DataValues of this Component
        """
        if self.__data_values is None:
            self.__data_values = [(k,v) for k,v in self.__dict__.items() if isinstance(v,DataValue)]
        return self.__data_values
    
    def __get_input_values(self)->list[tuple[str,DataValue]]:
        return [(k,v) for k,v in self.__get_data_values() if v.register_type == RegisterTypes.Input]
    
    def __get_holding_values(self)->list[tuple[str,DataValue]]:
        return [(k,v) for k,v in self.__get_data_values() if v.register_type == RegisterTypes.Holding]
    
    @staticmethod
    def __unsigned_to_signed(n:int, byte_count:int)->int:
        return int.from_bytes(
            n.to_bytes(byte_count, "little", signed=False), "little", signed=True
        )
        
    def parse(self,data:list[int],type:RegisterTypes)->bool:
        """
        Dynamically assignes the values to the DataValues of this Component
        """
        if len(data) != (self.input_count if type == RegisterTypes.Input else self.holding_count):
            logging.error(f"Data length does not match the expected length of {self.count} for {self.__class__.__name__}")
            return False
        
        encountered_error = False
        for name,value in self.__get_input_values() if type == RegisterTypes.Input else self.__get_holding_values():
            try:
                # Multi-register values (UINT32, INT32)
                if value.count == 2:
                    _value = (data[value.address] << 16) + data[value.address+ 1]
                else:
                    _value = data[value.address]
                 
                # Datatype
                if value.type == DataTypes.INT:
                    _value = Component.__unsigned_to_signed(_value, value.count * 2)
                    
                #Store
                value.value = _value   
            except:
                logging.exception(f"Error while parsing {name} of {self.__class__.__name__}")
                encountered_error = True
        return not encountered_error
    
    def __repr__(self) -> str:
        s = [f"{self.__class__.__name__}"]
        s.append("---Input:")
        for name,value in self.__get_input_values():
            s.append(f"{name}| raw:{value.value} scaled:{value.scaled_value}")
        s.append("---Holding:")
        for name,value in self.__get_holding_values():
            s.append(f"{name} | raw:{value.value}")
            
        return "\n".join(s)