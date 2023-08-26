"""Solarfocus data value"""

import logging

from ...modbus_wrapper import ModbusConnector
from .enums import DataTypes, RegisterTypes
from .part import Part


class DataValue(Part):
    """
    Abstraction of a certain relative address in the modbus register
    """

    data_type: DataTypes
    address: int
    count: int
    value: int
    multiplier: float
    absolut_address: int
    modbus: ModbusConnector
    register_type: RegisterTypes

    def __init__(
        self,
        address: int,
        count: int = 1,
        default_value: int = 0,
        multiplier: float = None,
        data_type: DataTypes = DataTypes.INT,
        register_type: RegisterTypes = RegisterTypes.INPUT,
    ) -> None:
        self.address = address
        self.count = count
        self.value = default_value
        self.multiplier = multiplier
        self.data_type = data_type
        self.register_type = register_type
        # These are set by the parent component
        self.absolut_address = None
        self.modbus = None

    def get_absolute_address(self) -> int:
        """
        Returns the absolute address of the register
        """
        if not self.absolut_address:
            raise Exception("Absolute address not set!")
        return self.absolut_address + self.address

    @property
    def has_scaler(self) -> bool:
        return self.multiplier is not None

    @property
    def scaled_value(self) -> float:
        """
        Scaled value of this register
        """
        if self.has_scaler:
            # Input registers are scaled differently than holding registers
            if self.register_type == RegisterTypes.INPUT:
                return self.value * self.multiplier
            return self.value / self.multiplier
        return self.value

    def reverse_scale(self, value: float) -> float:
        """
        Applies the scaler in the reverse direction
        """
        if self.has_scaler:
            # Input registers are scaled differently than holding registers
            if self.register_type == RegisterTypes.INPUT:
                return value / self.multiplier
            return value * self.multiplier
        return value

    def set_unscaled_value(self, value: float) -> None:
        """
        Applies the reverse scaler to the value and sets the value
        """
        self.value = self.reverse_scale(value)

    def commit(self) -> bool:
        """
        Writes the current value to the heating system
        """
        if self.modbus is None:
            # Modbus is never set for input registers
            return False

        logging.debug(f"Writing to server: Scaled Value={self.scaled_value}, Raw Value={int(self.value)}, Address={self.get_absolute_address()}")
        return self.modbus.write_register(int(self.value), self.get_absolute_address())
