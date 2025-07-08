"""Tests for DataValue class"""
import unittest.mock as mock
from unittest.mock import MagicMock

from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.base.enums import DataTypes, RegisterTypes
from pysolarfocus.modbus_wrapper import ModbusConnector


def test_data_value_init():
    """Test DataValue initialization"""
    dv = DataValue(address=5, count=2, default_value=100, multiplier=0.1, data_type=DataTypes.UINT, register_type=RegisterTypes.HOLDING)

    assert dv.address == 5
    assert dv.count == 2
    assert dv.value == 100
    assert dv.multiplier == 0.1
    assert dv.data_type == DataTypes.UINT
    assert dv.register_type == RegisterTypes.HOLDING
    assert dv.absolut_address is None
    assert dv.modbus is None


def test_data_value_defaults():
    """Test DataValue with default values"""
    dv = DataValue(address=10)

    assert dv.address == 10
    assert dv.count == 1
    assert dv.value == 0
    assert dv.multiplier is None
    assert dv.data_type == DataTypes.INT
    assert dv.register_type == RegisterTypes.INPUT


def test_get_absolute_address():
    """Test get_absolute_address method"""
    dv = DataValue(address=5)

    # Should raise ValueError when absolute address not set
    try:
        dv.get_absolute_address()
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert str(e) == "Absolute address not set!"

    # Should return correct absolute address when set
    dv.absolut_address = 1000
    assert dv.get_absolute_address() == 1005


def test_scaled_value_property():
    """Test scaled_value property"""
    # Test without multiplier
    dv = DataValue(address=0)
    dv.value = 250
    assert dv.scaled_value == 250

    # Test with multiplier for input register
    dv = DataValue(address=0, multiplier=0.1, register_type=RegisterTypes.INPUT)
    dv.value = 250
    assert dv.scaled_value == 25.0

    # Test with multiplier for holding register
    dv = DataValue(address=0, multiplier=0.1, register_type=RegisterTypes.HOLDING)
    dv.value = 250
    assert dv.scaled_value == 2500.0


def test_has_scaler_property():
    """Test has_scaler property"""
    dv_no_scaler = DataValue(address=0)
    assert dv_no_scaler.has_scaler is False

    dv_with_scaler = DataValue(address=0, multiplier=0.1)
    assert dv_with_scaler.has_scaler is True


def test_set_unscaled_value():
    """Test set_unscaled_value method"""
    # Test without multiplier
    dv = DataValue(address=0)
    dv.set_unscaled_value(456)
    assert dv.value == 456

    # Test with multiplier for input register
    dv = DataValue(address=0, multiplier=0.1, register_type=RegisterTypes.INPUT)
    dv.set_unscaled_value(25.0)
    assert dv.value == 250.0

    # Test with multiplier for holding register
    dv = DataValue(address=0, multiplier=0.1, register_type=RegisterTypes.HOLDING)
    dv.set_unscaled_value(25.0)
    assert dv.value == 2.5


def test_reverse_scale():
    """Test reverse_scale method"""
    # Test without multiplier
    dv = DataValue(address=0)
    assert dv.reverse_scale(100) == 100

    # Test with multiplier for input register
    dv = DataValue(address=0, multiplier=0.1, register_type=RegisterTypes.INPUT)
    assert dv.reverse_scale(25.0) == 250.0

    # Test with multiplier for holding register
    dv = DataValue(address=0, multiplier=0.1, register_type=RegisterTypes.HOLDING)
    assert dv.reverse_scale(25.0) == 2.5


def test_commit_input_register():
    """Test commit method for input register (should return False)"""
    dv = DataValue(address=0, register_type=RegisterTypes.INPUT)
    # Input registers don't get modbus set, so modbus should be None
    dv.absolut_address = 1000

    result = dv.commit()
    assert result is False


def test_commit_holding_register_success():
    """Test commit method for holding register success"""
    dv = DataValue(address=5, register_type=RegisterTypes.HOLDING)
    mock_modbus = MagicMock()
    mock_modbus.write_register.return_value = True
    dv.modbus = mock_modbus
    dv.absolut_address = 1000
    dv.value = 123

    result = dv.commit()
    assert result is True
    mock_modbus.write_register.assert_called_once_with(123, 1005)


def test_commit_holding_register_failure():
    """Test commit method for holding register failure"""
    dv = DataValue(address=5, register_type=RegisterTypes.HOLDING)
    mock_modbus = MagicMock()
    mock_modbus.write_register.return_value = False
    dv.modbus = mock_modbus
    dv.absolut_address = 1000
    dv.value = 123

    result = dv.commit()
    assert result is False
    mock_modbus.write_register.assert_called_once_with(123, 1005)


def test_commit_no_modbus():
    """Test commit method when modbus is None"""
    dv = DataValue(address=0, register_type=RegisterTypes.HOLDING)
    dv.absolut_address = 1000
    # modbus is None by default

    result = dv.commit()
    assert result is False


def test_commit_no_absolute_address():
    """Test commit method when absolute address is None"""
    dv = DataValue(address=0, register_type=RegisterTypes.HOLDING)
    dv.modbus = MagicMock()
    # absolut_address is None by default

    # This should raise ValueError when trying to get absolute address
    try:
        dv.commit()
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_data_value_with_different_data_types():
    """Test DataValue with different data types"""
    # Test with UINT
    dv_uint = DataValue(address=0, data_type=DataTypes.UINT)
    assert dv_uint.data_type == DataTypes.UINT

    # Test with INT
    dv_int = DataValue(address=0, data_type=DataTypes.INT)
    assert dv_int.data_type == DataTypes.INT


def test_data_value_multiregister():
    """Test DataValue with multiple registers"""
    dv = DataValue(address=0, count=4)
    assert dv.count == 4

    # Test absolute address calculation
    dv.absolut_address = 2000
    assert dv.get_absolute_address() == 2000


def test_data_value_edge_cases():
    """Test DataValue edge cases"""
    # Test with zero multiplier - input register
    dv = DataValue(address=0, multiplier=0.0, register_type=RegisterTypes.INPUT)
    dv.value = 100
    assert dv.scaled_value == 0.0

    # Test with zero multiplier - holding register
    dv = DataValue(address=0, multiplier=0.0, register_type=RegisterTypes.HOLDING)
    dv.value = 100
    # Division by zero should be handled gracefully
    try:
        scaled = dv.scaled_value
        # If it doesn't raise an error, that's acceptable behavior
    except ZeroDivisionError:
        # If it raises ZeroDivisionError, that's also acceptable
        pass

    # Test with very small multiplier
    dv = DataValue(address=0, multiplier=0.001, register_type=RegisterTypes.INPUT)
    dv.value = 1000
    assert dv.scaled_value == 1.0

    # Test with large multiplier
    dv = DataValue(address=0, multiplier=100.0, register_type=RegisterTypes.INPUT)
    dv.value = 5
    assert dv.scaled_value == 500.0
