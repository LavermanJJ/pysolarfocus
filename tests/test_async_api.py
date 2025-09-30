"""Tests for async Solarfocus API functionality"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from pysolarfocus import (
    ApiVersions,
    AsyncSolarfocusAPI,
    Systems,
)
from pysolarfocus.async_modbus_wrapper import AsyncModbusConnector
from pysolarfocus.async_component_manager import AsyncComponentManager


@pytest.mark.asyncio
async def test_async_modbus_connector_connect():
    """Test AsyncModbusConnector connect method"""
    with patch("pysolarfocus.async_modbus_wrapper.ModbusConnector") as mock_modbus_class, \
         patch("pysolarfocus.async_modbus_wrapper.AsyncModbusTcpClient") as mock_async_client_class:
        
        mock_sync_connector = MagicMock()
        mock_modbus_class.return_value = mock_sync_connector
        
        mock_async_client = AsyncMock()
        mock_async_client_class.return_value = mock_async_client
        
        async_connector = AsyncModbusConnector("localhost", 502, 1)
        
        # Test successful connection
        mock_sync_connector.connect.return_value = True
        mock_async_client.connect.return_value = None  # async connect doesn't return anything
        mock_async_client.connected = True
        
        result = await async_connector.connect()
        assert result is True
        assert async_connector.is_connected is True
        
        # Test failed connection
        mock_async_client.connected = False
        result = await async_connector.connect()
        assert result is False


@pytest.mark.asyncio
async def test_async_modbus_connector_read_operations():
    """Test AsyncModbusConnector read operations"""
    with patch("pysolarfocus.async_modbus_wrapper.ModbusConnector") as mock_modbus_class, \
         patch("pysolarfocus.async_modbus_wrapper.AsyncModbusTcpClient") as mock_async_client_class:
        
        mock_sync_connector = MagicMock()
        mock_modbus_class.return_value = mock_sync_connector
        mock_sync_connector.is_connected = True
        
        mock_async_client = AsyncMock()
        mock_async_client_class.return_value = mock_async_client
        
        async_connector = AsyncModbusConnector("localhost", 502, 1)
        async_connector._is_connected = True  # Simulate connected state
        async_connector._client = mock_async_client
        
        # Mock register slices
        mock_slice = MagicMock()
        mock_slice.absolute_address = 100
        mock_slice.relative_address = 0
        mock_slice.count = 2
        
        # Test read_input_registers
        mock_response = MagicMock()
        mock_response.isError.return_value = False
        mock_response.registers = [100, 200]
        mock_async_client.read_input_registers.return_value = mock_response
        
        success, data = await async_connector.read_input_registers([mock_slice], 2)
        assert success is True
        assert data == [100, 200]
        
        # Test read_holding_registers
        mock_async_client.read_holding_registers.return_value = mock_response
        success, data = await async_connector.read_holding_registers([mock_slice], 2)
        assert success is True
        assert data == [100, 200]


@pytest.mark.asyncio
async def test_async_modbus_connector_write_operation():
    """Test AsyncModbusConnector write operation"""
    with patch("pysolarfocus.async_modbus_wrapper.ModbusConnector") as mock_modbus_class, \
         patch("pysolarfocus.async_modbus_wrapper.AsyncModbusTcpClient") as mock_async_client_class:
        
        mock_sync_connector = MagicMock()
        mock_modbus_class.return_value = mock_sync_connector
        mock_sync_connector.is_connected = True
        
        mock_async_client = AsyncMock()
        mock_async_client_class.return_value = mock_async_client
        
        async_connector = AsyncModbusConnector("localhost", 502, 1)
        async_connector._is_connected = True  # Simulate connected state
        async_connector._client = mock_async_client
        
        # Test write_register
        mock_response = MagicMock()
        mock_response.isError.return_value = False
        mock_async_client.write_registers.return_value = mock_response
        
        result = await async_connector.write_register(123, 1000)
        assert result is True


@pytest.mark.asyncio
async def test_async_solarfocus_api_initialization():
    """Test AsyncSolarfocusAPI initialization and component creation"""
    with patch("pysolarfocus.async_api.AsyncModbusConnector") as mock_async_modbus_class:
        mock_async_modbus_instance = MagicMock()
        mock_async_modbus_class.return_value = mock_async_modbus_instance
        
        # Create mock sync connector
        mock_sync_connector = MagicMock()
        mock_async_modbus_instance._sync_connector = mock_sync_connector
        
        api = AsyncSolarfocusAPI(
            ip="localhost", 
            system=Systems.VAMPAIR, 
            api_version=ApiVersions.V_25_030
        )
        
        # Mock the component manager's create_components method
        with patch.object(api.component_manager, 'create_components') as mock_create:
            mock_create.return_value = None
            
            # Mock component manager components
            api.component_manager.components = {
                "heating_circuits": [MagicMock()],
                "boilers": [MagicMock()],
                "buffers": [MagicMock()],
                "solar": [MagicMock()],
                "heatpump": MagicMock(),
                "photovoltaic": MagicMock(),
                "biomassboiler": MagicMock(),
            }
            
            await api.initialize()
            
            # Verify components were created
            mock_create.assert_called_once()
            assert len(api.heating_circuits) == 1
            assert len(api.boilers) == 1
            assert len(api.buffers) == 1
            assert len(api.solar) == 1
            assert api.heatpump is not None
            assert api.photovoltaic is not None
            assert api.biomassboiler is not None


@pytest.mark.asyncio
async def test_async_solarfocus_api_connect():
    """Test AsyncSolarfocusAPI connect method"""
    with patch("pysolarfocus.async_api.AsyncModbusConnector") as mock_async_modbus_class:
        mock_async_modbus_instance = AsyncMock()
        mock_async_modbus_class.return_value = mock_async_modbus_instance
        
        api = AsyncSolarfocusAPI(ip="localhost")
        
        # Test successful connection
        mock_async_modbus_instance.connect.return_value = True
        result = await api.connect()
        assert result is True
        
        # Test failed connection
        mock_async_modbus_instance.connect.return_value = False
        result = await api.connect()
        assert result is False


@pytest.mark.asyncio
async def test_async_solarfocus_api_update_methods():
    """Test AsyncSolarfocusAPI update methods"""
    with patch("pysolarfocus.async_api.AsyncModbusConnector") as mock_async_modbus_class:
        mock_async_modbus_instance = MagicMock()
        mock_async_modbus_class.return_value = mock_async_modbus_instance
        
        api = AsyncSolarfocusAPI(
            ip="localhost", 
            system=Systems.VAMPAIR, 
            api_version=ApiVersions.V_25_030
        )
        
        # Mock component manager update methods
        with patch.object(api.component_manager, 'update_all') as mock_update_all:
            with patch.object(api.component_manager, 'update') as mock_update:
                mock_update_all.return_value = True
                mock_update.return_value = True
                
                # Test update
                result = await api.update()
                assert result is True
                mock_update_all.assert_called_once()
                
                # Test individual update methods
                result = await api.update_heating()
                assert result is True
                mock_update.assert_called_with("heating_circuits")
                
                result = await api.update_buffer()
                assert result is True
                mock_update.assert_called_with("buffers")
                
                result = await api.update_boiler()
                assert result is True
                mock_update.assert_called_with("boilers")


@pytest.mark.asyncio
async def test_async_solarfocus_api_partial_update():
    """Test AsyncSolarfocusAPI partial update functionality"""
    with patch("pysolarfocus.async_api.AsyncModbusConnector") as mock_async_modbus_class:
        mock_async_modbus_instance = MagicMock()
        mock_async_modbus_class.return_value = mock_async_modbus_instance
        
        api = AsyncSolarfocusAPI(ip="localhost")
        
        # Mock component manager update method
        with patch.object(api.component_manager, 'update') as mock_update:
            mock_update.return_value = True
            
            # Test parallel partial update
            result = await api.update_partial(["heating_circuits", "buffers"], parallel=True)
            assert result is True
            assert mock_update.call_count == 2
            
            mock_update.reset_mock()
            
            # Test sequential partial update
            result = await api.update_partial(["heating_circuits", "buffers"], parallel=False)
            assert result is True
            assert mock_update.call_count == 2


@pytest.mark.asyncio
async def test_async_component_manager_parallel_update():
    """Test AsyncComponentManager parallel update functionality"""
    with patch("pysolarfocus.async_component_manager.AsyncModbusConnector") as mock_async_modbus_class:
        mock_async_modbus_instance = MagicMock()
        mock_async_modbus_class.return_value = mock_async_modbus_instance
        
        manager = AsyncComponentManager(mock_async_modbus_instance)
        
        # Create mock components
        mock_component1 = AsyncMock()
        mock_component1.update.return_value = True
        mock_component2 = AsyncMock()
        mock_component2.update.return_value = True
        
        manager.components = {
            "component1": mock_component1,
            "component2": mock_component2
        }
        
        # Test parallel update
        result = await manager.update_all(parallel=True)
        assert result is True
        
        # Verify both components were updated
        mock_component1.update.assert_called_once()
        mock_component2.update.assert_called_once()


@pytest.mark.asyncio
async def test_async_connection_health():
    """Test connection health monitoring"""
    with patch("pysolarfocus.async_api.AsyncModbusConnector") as mock_async_modbus_class:
        mock_async_modbus_instance = MagicMock()
        mock_async_modbus_class.return_value = mock_async_modbus_instance
        mock_async_modbus_instance.get_connection_health.return_value = {
            "is_connected": True,
            "last_connection_attempt": 1234567890.0,
            "connection_backoff": 1.0,
            "ip": "localhost",
            "port": 502,
            "slave_id": 1
        }
        
        api = AsyncSolarfocusAPI(ip="localhost")
        health = api.get_connection_health()
        
        assert health["is_connected"] is True
        assert health["ip"] == "localhost"
        assert health["port"] == 502


def test_async_api_initialization_validation():
    """Test AsyncSolarfocusAPI initialization validation"""
    # Test invalid system type - pass a non-enum value
    with pytest.raises(Exception):  # Should raise InvalidConfigurationError
        AsyncSolarfocusAPI(ip="localhost", system="invalid_system")  # type: ignore
    
    # Test invalid api version - pass a non-enum value
    with pytest.raises(Exception):  # Should raise InvalidConfigurationError
        AsyncSolarfocusAPI(ip="localhost", api_version="invalid_version")  # type: ignore


@pytest.mark.asyncio 
async def test_async_solarfocus_api_repr():
    """Test AsyncSolarfocusAPI __repr__ method"""
    with patch("pysolarfocus.async_api.AsyncModbusConnector") as mock_async_modbus_class:
        mock_async_modbus_instance = MagicMock()
        mock_async_modbus_instance.is_connected = True
        mock_async_modbus_class.return_value = mock_async_modbus_instance
        
        api = AsyncSolarfocusAPI(
            ip="localhost", 
            system=Systems.VAMPAIR, 
            api_version=ApiVersions.V_25_030
        )
        
        # Mock component manager for health check
        with patch.object(api.component_manager, 'is_healthy') as mock_healthy:
            mock_healthy.return_value = True
            
            repr_str = repr(api)
            assert "AsyncSolarfocusAPI" in repr_str
            assert "Vampair" in repr_str
            assert "25.030" in repr_str
            assert "Connected" in repr_str
            assert "Healthy" in repr_str
