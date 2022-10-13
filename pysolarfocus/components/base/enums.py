from enum import Enum

class RegisterTypes(str, Enum):
    Holding = "Holding"
    Input = "Input"
     
class DataTypes(int, Enum):
    INT = 1
    UINT = 2  