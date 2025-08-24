"""Custom exceptions for pysolarfocus"""


class PySolarfocusError(Exception):
    """Base exception for pysolarfocus"""

    pass


class ModbusConnectionError(PySolarfocusError):
    """Raised when modbus connection fails"""

    pass


class ComponentInitializationError(PySolarfocusError):
    """Raised when component initialization fails"""

    pass


class DataParsingError(PySolarfocusError):
    """Raised when data parsing fails"""

    pass


class RegisterReadError(PySolarfocusError):
    """Raised when register reading fails"""

    pass


class RegisterWriteError(PySolarfocusError):
    """Raised when register writing fails"""

    pass


class InvalidConfigurationError(PySolarfocusError):
    """Raised when invalid configuration is provided"""

    pass
