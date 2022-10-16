from dataclasses import dataclass

@dataclass()
class RegisterSlice:
    absolute_address:int
    relative_address:int
    count:int
