"""Tests for modbus wrapper"""
import unittest.mock as mock
from unittest.mock import MagicMock

from pysolarfocus.components.base.register_slice import RegisterSlice
from pysolarfocus.modbus_wrapper import ModbusConnector


def test_modbus_connector_init():
    """Test ModbusConnector initialization"""
    conn = ModbusConnector("localhost", 502, 1)
    assert conn.ip == "localhost"
    assert conn.port == 502
    assert conn.slave_id == 1
    assert conn.client is not None


def test_modbus_connector_connection():
    """Test ModbusConnector connection methods"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        conn = ModbusConnector("localhost", 502, 1)

        # Test is_connected
        mock_client_instance.is_socket_open.return_value = True
        assert conn.is_connected is True

        mock_client_instance.is_socket_open.return_value = False
        assert conn.is_connected is False

        # Test connect
        mock_client_instance.connect.return_value = True
        assert conn.connect() is True

        mock_client_instance.connect.return_value = False
        assert conn.connect() is False


def test_read_input_registers_success():
    """Test successful read_input_registers"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        # Mock successful response
        mock_response = MagicMock()
        mock_response.isError.return_value = False
        mock_response.registers = [100, 200, 300]
        mock_client_instance.read_input_registers.return_value = mock_response
        mock_client_instance.is_socket_open.return_value = True

        conn = ModbusConnector("localhost", 502, 1)

        slices = [RegisterSlice(500, 0, 3)]
        success, result = conn.read_input_registers(slices, 3)

        assert success is True
        assert result == [100, 200, 300]


def test_read_input_registers_not_connected():
    """Test read_input_registers when not connected"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.is_socket_open.return_value = False

        conn = ModbusConnector("localhost", 502, 1)

        slices = [RegisterSlice(500, 0, 3)]
        success, result = conn.read_input_registers(slices, 3)

        assert success is False
        assert result is None


def test_read_input_registers_error():
    """Test read_input_registers with modbus error"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        # Mock error response
        mock_response = MagicMock()
        mock_response.isError.return_value = True
        mock_client_instance.read_input_registers.return_value = mock_response
        mock_client_instance.is_socket_open.return_value = True

        conn = ModbusConnector("localhost", 502, 1)

        slices = [RegisterSlice(500, 0, 3)]
        success, result = conn.read_input_registers(slices, 3)

        assert success is False
        assert result is None


def test_read_input_registers_exception():
    """Test read_input_registers with exception"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.is_socket_open.return_value = True
        mock_client_instance.read_input_registers.side_effect = Exception("Connection error")

        conn = ModbusConnector("localhost", 502, 1)

        slices = [RegisterSlice(500, 0, 3)]
        success, result = conn.read_input_registers(slices, 3)

        assert success is False
        assert result is None


def test_read_holding_registers_success():
    """Test successful read_holding_registers"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        # Mock successful response
        mock_response = MagicMock()
        mock_response.isError.return_value = False
        mock_response.registers = [400, 500, 600]
        mock_client_instance.read_holding_registers.return_value = mock_response
        mock_client_instance.is_socket_open.return_value = True

        conn = ModbusConnector("localhost", 502, 1)

        slices = [RegisterSlice(32000, 0, 3)]
        success, result = conn.read_holding_registers(slices, 3)

        assert success is True
        assert result == [400, 500, 600]


def test_read_holding_registers_not_connected():
    """Test read_holding_registers when not connected"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.is_socket_open.return_value = False

        conn = ModbusConnector("localhost", 502, 1)

        slices = [RegisterSlice(32000, 0, 3)]
        success, result = conn.read_holding_registers(slices, 3)

        assert success is False
        assert result is None


def test_read_holding_registers_error():
    """Test read_holding_registers with modbus error"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        # Mock error response
        mock_response = MagicMock()
        mock_response.isError.return_value = True
        mock_client_instance.read_holding_registers.return_value = mock_response
        mock_client_instance.is_socket_open.return_value = True

        conn = ModbusConnector("localhost", 502, 1)

        slices = [RegisterSlice(32000, 0, 3)]
        success, result = conn.read_holding_registers(slices, 3)

        assert success is False
        assert result is None


def test_write_register_success():
    """Test successful write_register"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        # Mock successful response
        mock_response = MagicMock()
        mock_response.isError.return_value = False
        mock_client_instance.write_registers.return_value = mock_response
        mock_client_instance.is_socket_open.return_value = True

        conn = ModbusConnector("localhost", 502, 1)

        result = conn.write_register(123, 32000)

        assert result is True
        mock_client_instance.write_registers.assert_called_once_with(32000, [123], slave=1)


def test_write_register_not_connected():
    """Test write_register when not connected"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.is_socket_open.return_value = False

        conn = ModbusConnector("localhost", 502, 1)

        result = conn.write_register(123, 32000)

        assert result is False


def test_write_register_error():
    """Test write_register with modbus error"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        # Mock error response
        mock_response = MagicMock()
        mock_response.isError.return_value = True
        mock_client_instance.write_registers.return_value = mock_response
        mock_client_instance.is_socket_open.return_value = True

        conn = ModbusConnector("localhost", 502, 1)

        result = conn.write_register(123, 32000)

        assert result is False


def test_write_register_exception():
    """Test write_register with exception"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.is_socket_open.return_value = True
        mock_client_instance.write_registers.side_effect = Exception("Connection error")

        conn = ModbusConnector("localhost", 502, 1)

        result = conn.write_register(123, 32000)

        assert result is False


def test_multiple_register_slices():
    """Test reading multiple register slices"""
    with mock.patch("pysolarfocus.modbus_wrapper.ModbusClient") as mock_client:
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        # Mock responses for multiple slices
        mock_response1 = MagicMock()
        mock_response1.isError.return_value = False
        mock_response1.registers = [100, 200]

        mock_response2 = MagicMock()
        mock_response2.isError.return_value = False
        mock_response2.registers = [300, 400, 500]

        mock_client_instance.read_input_registers.side_effect = [mock_response1, mock_response2]
        mock_client_instance.is_socket_open.return_value = True

        conn = ModbusConnector("localhost", 502, 1)

        slices = [RegisterSlice(500, 0, 2), RegisterSlice(510, 2, 3)]
        success, result = conn.read_input_registers(slices, 5)

        assert success is True
        assert result == [100, 200, 300, 400, 500]
