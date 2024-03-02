"""Solarfocus base enums"""

from enum import Enum


class RegisterTypes(str, Enum):
    HOLDING = "Holding"
    INPUT = "Input"


class DataTypes(int, Enum):
    INT = 1
    UINT = 2
