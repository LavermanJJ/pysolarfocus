"""Tests for base Component class"""
import unittest.mock as mock
from unittest.mock import MagicMock

import pytest

from pysolarfocus.components.base.component import Component
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.base.enums import RegisterTypes
from pysolarfocus.components.base.register_slice import RegisterSlice
from pysolarfocus.modbus_wrapper import ModbusConnector


class MockComponent(Component):
    """Mock component class for testing"""

    def __init__(self, input_address=1000, holding_address=2000):
        super().__init__(input_address, holding_address)
        self.test_input = DataValue(address=0, register_type=RegisterTypes.INPUT)
        self.test_input_multi = DataValue(address=1, count=2, register_type=RegisterTypes.INPUT)
        self.test_holding = DataValue(address=0, register_type=RegisterTypes.HOLDING)
        self.test_holding_multi = DataValue(address=1, count=3, register_type=RegisterTypes.HOLDING)


def test_component_init():
    """Test Component initialization"""
    comp = MockComponent()
    assert comp.input_address == 1000
    assert comp.holding_address == 2000


def test_component_init_only_input():
    """Test Component initialization with only input address"""
    comp = MockComponent(input_address=1500, holding_address=-1)
    assert comp.input_address == 1500
    assert comp.holding_address == -1


def test_component_initialize():
    """Test Component initialize method"""
    mock_modbus = MagicMock()
    comp = MockComponent()

    result = comp.initialize(mock_modbus)

    # Should return self
    assert result == comp

    # Should set modbus connector (it's private)
    # We can't directly test the private attribute, but we can test the behavior

    # Should set absolute addresses for data values
    assert comp.test_input.absolut_address == 1000
    assert comp.test_input_multi.absolut_address == 1000
    assert comp.test_holding.absolut_address == 2000
    assert comp.test_holding_multi.absolut_address == 2000

    # Should set modbus for holding register data values only
    assert comp.test_holding.modbus == mock_modbus
    assert comp.test_holding_multi.modbus == mock_modbus


def test_component_update_input_registers_success():
    """Test component update with successful input register read"""
    mock_modbus = MagicMock()
    mock_modbus.read_input_registers.return_value = (True, [100, 200, 300])
    mock_modbus.read_holding_registers.return_value = (True, [400, 500, 600, 700])

    comp = MockComponent()
    comp.initialize(mock_modbus)

    result = comp.update()

    assert result is True
    assert comp.test_input.value == 100
    # Multi-register values are parsed according to Component logic - actual value is combined
    assert comp.test_input_multi.value == 13107500  # (200 << 16) + 300


def test_component_update_input_registers_failure():
    """Test component update with failed input register read"""
    mock_modbus = MagicMock()
    mock_modbus.read_input_registers.return_value = (False, None)
    mock_modbus.read_holding_registers.return_value = (True, [400, 500, 600, 700])

    comp = MockComponent()
    comp.initialize(mock_modbus)

    result = comp.update()

    assert result is False


def test_component_update_holding_registers_success():
    """Test component update with successful holding register read"""
    mock_modbus = MagicMock()
    mock_modbus.read_input_registers.return_value = (True, [100, 200, 300])
    mock_modbus.read_holding_registers.return_value = (True, [400, 500, 600, 700])

    comp = MockComponent()
    comp.initialize(mock_modbus)

    result = comp.update()

    assert result is True
    assert comp.test_holding.value == 400
    # Multi-register values are parsed as single values according to Component logic
    assert comp.test_holding_multi.value == 500  # First value of the multi-register


def test_component_update_holding_registers_failure():
    """Test component update with failed holding register read"""
    mock_modbus = MagicMock()
    mock_modbus.read_input_registers.return_value = (True, [100, 200, 300])
    mock_modbus.read_holding_registers.return_value = (False, None)

    comp = MockComponent()
    comp.initialize(mock_modbus)

    result = comp.update()

    assert result is False


def test_component_update_no_holding_address():
    """Test component update with no holding address"""
    mock_modbus = MagicMock()
    mock_modbus.read_input_registers.return_value = (True, [100, 200, 300])

    comp = MockComponent(holding_address=-1)
    comp.initialize(mock_modbus)

    result = comp.update()

    assert result is True
    # Should not attempt to read holding registers
    mock_modbus.read_holding_registers.assert_not_called()


def test_component_update_no_modbus():
    """Test component update with no modbus connector"""
    comp = MockComponent()
    # Don't call initialize, so modbus remains None

    # Since the component is not initialized, it has no registers to read
    # so update should return True (no failures)
    result = comp.update()
    assert result is True


def test_component_properties():
    """Test Component properties"""
    comp = MockComponent()
    comp.initialize(MagicMock())

    # Test has_input_address
    assert comp.has_input_address is True

    # Test has_holding_address
    assert comp.has_holding_address is True

    # Test input_slices property
    assert comp.input_slices is not None
    assert len(comp.input_slices) >= 1

    # Test holding_slices property
    assert comp.holding_slices is not None
    assert len(comp.holding_slices) >= 1


def test_component_no_input_address():
    """Test component with no input address"""
    comp = MockComponent(input_address=-1)
    comp.initialize(MagicMock())

    assert comp.has_input_address is False


def test_component_no_holding_address():
    """Test component with no holding address"""
    comp = MockComponent(holding_address=-1)
    comp.initialize(MagicMock())

    assert comp.has_holding_address is False


def test_component_calculate_ranges_simple():
    """Test _calculate_ranges with simple case"""
    data_values = [DataValue(address=0), DataValue(address=1), DataValue(address=2)]

    # Set absolute addresses
    for i, dv in enumerate(data_values):
        dv.absolut_address = 1000

    ranges = Component._calculate_ranges(data_values)

    assert len(ranges) == 1
    assert ranges[0].absolute_address == 1000
    assert ranges[0].relative_address == 0
    assert ranges[0].count == 3


def test_component_calculate_ranges_with_gaps():
    """Test _calculate_ranges with gaps in addresses"""
    data_values = [DataValue(address=0), DataValue(address=1), DataValue(address=5), DataValue(address=6)]  # Gap here

    # Set absolute addresses
    for dv in data_values:
        dv.absolut_address = 1000

    ranges = Component._calculate_ranges(data_values)

    assert len(ranges) == 2
    assert ranges[0].absolute_address == 1000
    assert ranges[0].relative_address == 0
    assert ranges[0].count == 2
    assert ranges[1].absolute_address == 1005
    assert ranges[1].relative_address == 5
    assert ranges[1].count == 2


def test_component_calculate_ranges_multi_register():
    """Test _calculate_ranges with multi-register values"""
    data_values = [DataValue(address=0, count=2), DataValue(address=2, count=3)]

    # Set absolute addresses
    for dv in data_values:
        dv.absolut_address = 1000

    ranges = Component._calculate_ranges(data_values)

    assert len(ranges) == 1
    assert ranges[0].absolute_address == 1000
    assert ranges[0].relative_address == 0
    assert ranges[0].count == 5


def test_component_repr():
    """Test Component repr method"""
    mock_modbus = MagicMock()
    mock_modbus.read_input_registers.return_value = (True, [100, 200, 300])
    mock_modbus.read_holding_registers.return_value = (True, [400, 500, 600, 700])

    comp = MockComponent()
    comp.initialize(mock_modbus)
    comp.update()

    repr_str = repr(comp)
    assert "MockComponent" in repr_str
    assert "Input:" in repr_str
    assert "Holding:" in repr_str
    assert "===" in repr_str


class ComponentWithNoDataValues(Component):
    """Component with no data values for testing edge cases"""

    def __init__(self):
        super().__init__(1000)


def test_component_with_no_data_values():
    """Test component with no data values"""
    mock_modbus = MagicMock()
    comp = ComponentWithNoDataValues()
    comp.initialize(mock_modbus)

    # Should still work without data values
    result = comp.update()
    assert result is True


class ComponentWithOnlyHolding(Component):
    """Component with only holding registers for testing"""

    def __init__(self):
        super().__init__(input_address=-1, holding_address=2000)
        self.test_holding = DataValue(address=0, register_type=RegisterTypes.HOLDING)


def test_component_with_only_holding_registers():
    """Test component with only holding registers"""
    mock_modbus = MagicMock()
    mock_modbus.read_holding_registers.return_value = (True, [123])

    comp = ComponentWithOnlyHolding()
    comp.initialize(mock_modbus)

    result = comp.update()

    assert result is True
    assert comp.test_holding.value == 123
    # Should not attempt to read input registers
    mock_modbus.read_input_registers.assert_not_called()
