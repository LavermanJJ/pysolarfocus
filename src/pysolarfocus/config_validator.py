"""Configuration validation utilities for pysolarfocus"""

from .exceptions import InvalidConfigurationError


class ConfigValidator:
    """Validates configuration parameters for pysolarfocus components."""

    # Component count limits
    COMPONENT_LIMITS = {
        "heating_circuit": (0, 8),
        "buffer": (0, 4),
        "boiler": (0, 4),
        "fresh_water_module": (0, 4),
        "circulation": (0, 4),
        "differential_module": (0, 4),
        "solar_legacy": (0, 1),  # For API versions < V_25_030
        "solar_modern": (0, 4),  # For API versions >= V_25_030
    }

    @classmethod
    def validate_component_count(cls, component_type: str, count: int, is_modern_api: bool = False) -> None:
        """Validate component count against limits.

        Args:
            component_type: Type of component to validate
            count: Number of components
            is_modern_api: Whether using modern API version for solar validation

        Raises:
            InvalidConfigurationError: If count is outside valid range
        """
        # Handle special case for solar components
        if component_type == "solar":
            component_type = "solar_modern" if is_modern_api else "solar_legacy"

        if component_type not in cls.COMPONENT_LIMITS:
            raise InvalidConfigurationError(f"Unknown component type: {component_type}")

        min_count, max_count = cls.COMPONENT_LIMITS[component_type]
        if not (min_count <= count <= max_count):
            raise InvalidConfigurationError(f"{component_type.replace('_', ' ').title()} count must be between {min_count} and {max_count}")

    @classmethod
    def validate_address_range(cls, address: int, min_addr: int, max_addr: int) -> None:
        """Validate modbus address is within valid range.

        Args:
            address: Address to validate
            min_addr: Minimum valid address
            max_addr: Maximum valid address

        Raises:
            InvalidConfigurationError: If address is outside valid range
        """
        if not (min_addr <= address <= max_addr):
            raise InvalidConfigurationError(f"Address {address} is outside valid range [{min_addr}, {max_addr}]")

    @classmethod
    def validate_multiplier(cls, multiplier: float) -> None:
        """Validate scaling multiplier.

        Args:
            multiplier: Multiplier value to validate

        Raises:
            InvalidConfigurationError: If multiplier is invalid
        """
        if multiplier <= 0:
            raise InvalidConfigurationError("Multiplier must be positive")
        if multiplier > 1000:
            raise InvalidConfigurationError("Multiplier seems unreasonably large")
