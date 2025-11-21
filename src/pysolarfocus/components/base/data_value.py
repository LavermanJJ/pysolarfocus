"""Solarfocus data value"""

import logging
from typing import Optional, Union

from ...modbus_wrapper import ModbusConnector
from .enums import DataTypes, RegisterTypes
from .part import Part


class DataValue(Part):
    """
    Abstraction of a certain relative address in the modbus register with validation and error handling.
    """

    def __init__(
        self,
        address: int,
        count: int = 1,
        default_value: int = 0,
        multiplier: Optional[float] = None,
        data_type: DataTypes = DataTypes.INT,
        register_type: RegisterTypes = RegisterTypes.INPUT,
    ) -> None:
        """Initialize DataValue with validation.

        Args:
            address: Relative address in the modbus register
            count: Number of registers to read (1 or 2)
            default_value: Default value if read fails
            multiplier: Scaling multiplier (None for no scaling)
            data_type: Data type (INT or UINT)
            register_type: Register type (INPUT or HOLDING)

        Raises:
            ValueError: If parameters are invalid
        """
        self._validate_parameters(address, count, multiplier, data_type, register_type)

        self.address = address
        self.count = count
        self.value: Union[int, float] = default_value
        self.multiplier = multiplier
        self.data_type = data_type
        self.register_type = register_type
        # These are set by the parent component
        self.absolut_address: Optional[int] = None
        self.modbus: Optional[ModbusConnector] = None

    def _validate_parameters(
        self,
        address: int,
        count: int,
        multiplier: Optional[float],
        data_type: DataTypes,
        register_type: RegisterTypes,
    ) -> None:
        """Validate initialization parameters."""
        if address < 0:
            raise ValueError("Address must be non-negative")
        if count < 1 or count > 10:  # Allow reasonable range for register count
            raise ValueError("Count must be between 1 and 10")
        if multiplier is not None and multiplier < 0:
            raise ValueError("Multiplier must be non-negative")
        if not isinstance(data_type, DataTypes):
            raise ValueError("Invalid data_type")
        if not isinstance(register_type, RegisterTypes):
            raise ValueError("Invalid register_type")

    def get_absolute_address(self) -> int:
        """
        Returns the absolute address of the register
        """
        if not self.absolut_address:
            raise ValueError("Absolute address not set!")
        return self.absolut_address + self.address

    @property
    def has_scaler(self) -> bool:
        return self.multiplier is not None

    @property
    def scaled_value(self) -> float:
        """
        Scaled value of this register
        """
        if self.has_scaler and self.multiplier is not None:
            # Input registers are scaled differently than holding registers
            if self.register_type == RegisterTypes.INPUT:
                return self.value * self.multiplier
            else:
                # Handle division by zero gracefully
                if self.multiplier == 0:
                    return 0.0
                return self.value / self.multiplier
        return self.value

    def reverse_scale(self, value: float) -> float:
        """
        Applies the scaler in the reverse direction
        """
        if self.has_scaler and self.multiplier is not None:
            # Input registers are scaled differently than holding registers
            if self.register_type == RegisterTypes.INPUT:
                if self.multiplier == 0:
                    return 0.0
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
