"""Tests for ComponentFactory"""
import unittest.mock as mock
from unittest.mock import MagicMock

from pysolarfocus import ApiVersions, Systems
from pysolarfocus.component_factory import ComponentFactory
from pysolarfocus.modbus_wrapper import ModbusConnector


def test_component_factory_init():
    """Test ComponentFactory initialization"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)
    # Just test that the factory was created successfully
    assert factory is not None


def test_heating_circuit_factory():
    """Test heating circuit factory method"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    # Test with VAMPAIR system
    circuits = factory.heating_circuit(Systems.VAMPAIR, 2, ApiVersions.V_21_140)
    assert len(circuits) == 2

    # Test with THERMINATOR system
    circuits = factory.heating_circuit(Systems.THERMINATOR, 1, ApiVersions.V_21_140)
    assert len(circuits) == 1

    # Test with ECOTOP system
    circuits = factory.heating_circuit(Systems.ECOTOP, 1, ApiVersions.V_21_140)
    assert len(circuits) == 1


def test_boiler_factory():
    """Test boiler factory method"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    boilers = factory.boiler(Systems.VAMPAIR, 3, ApiVersions.V_21_140)
    assert len(boilers) == 3

    # Test with different count
    boilers = factory.boiler(Systems.VAMPAIR, 1, ApiVersions.V_21_140)
    assert len(boilers) == 1


def test_buffer_factory():
    """Test buffer factory method"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    # Test with VAMPAIR system and older API version
    buffers = factory.buffer(Systems.VAMPAIR, 2, ApiVersions.V_21_140)
    assert len(buffers) == 2

    # Test with THERMINATOR system
    buffers = factory.buffer(Systems.THERMINATOR, 1, ApiVersions.V_21_140)
    assert len(buffers) == 1

    # Test with ECOTOP system
    buffers = factory.buffer(Systems.ECOTOP, 1, ApiVersions.V_21_140)
    assert len(buffers) == 1

    # Test with newer API version
    buffers = factory.buffer(Systems.VAMPAIR, 2, ApiVersions.V_22_090)
    assert len(buffers) == 2


def test_fresh_water_modules_factory():
    """Test fresh water modules factory method"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    modules = factory.fresh_water_modules(Systems.VAMPAIR, 2, ApiVersions.V_23_020)
    assert len(modules) == 2

    # Test with different count
    modules = factory.fresh_water_modules(Systems.VAMPAIR, 4, ApiVersions.V_23_020)
    assert len(modules) == 4


def test_circulation_factory():
    """Test circulation factory method"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    circulations = factory.circulation(Systems.VAMPAIR, 3, ApiVersions.V_25_030)
    assert len(circulations) == 3

    # Test with different count
    circulations = factory.circulation(Systems.VAMPAIR, 1, ApiVersions.V_25_030)
    assert len(circulations) == 1


def test_differential_modules_factory():
    """Test differential modules factory method"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    modules = factory.differential_modules(Systems.VAMPAIR, 2, ApiVersions.V_25_030)
    assert len(modules) == 2

    # Test with different count
    modules = factory.differential_modules(Systems.VAMPAIR, 4, ApiVersions.V_25_030)
    assert len(modules) == 4


def test_heatpump_factory():
    """Test heatpump factory method"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    heatpump = factory.heatpump(Systems.VAMPAIR, ApiVersions.V_21_140)
    assert heatpump is not None

    # Test with different API version
    heatpump = factory.heatpump(Systems.VAMPAIR, ApiVersions.V_25_030)
    assert heatpump is not None


def test_photovoltaic_factory():
    """Test photovoltaic factory method"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    pv = factory.photovoltaic(Systems.VAMPAIR, ApiVersions.V_21_140)
    assert pv is not None

    # Test with different system
    pv = factory.photovoltaic(Systems.THERMINATOR, ApiVersions.V_21_140)
    assert pv is not None


def test_pelletsboiler_factory():
    """Test pelletsboiler factory method"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    boiler = factory.pelletsboiler(Systems.THERMINATOR, ApiVersions.V_21_140)
    assert boiler is not None

    # Test with different system
    boiler = factory.pelletsboiler(Systems.ECOTOP, ApiVersions.V_21_140)
    assert boiler is not None


def test_solar_factory():
    """Test solar factory method"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    solar_modules = factory.solar(Systems.VAMPAIR, 2, ApiVersions.V_21_140)
    assert len(solar_modules) == 2

    # Test with different count
    solar_modules = factory.solar(Systems.VAMPAIR, 4, ApiVersions.V_25_030)
    assert len(solar_modules) == 4

    # Test with single module
    solar_modules = factory.solar(Systems.VAMPAIR, 1, ApiVersions.V_21_140)
    assert len(solar_modules) == 1


def test_factory_address_calculation():
    """Test that factory methods generate correct address ranges"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    # Test heating circuit addresses
    circuits = factory.heating_circuit(Systems.VAMPAIR, 3, ApiVersions.V_21_140)
    assert len(circuits) == 3
    # Should have addresses 1100, 1150, 1200

    # Test boiler addresses
    boilers = factory.boiler(Systems.VAMPAIR, 3, ApiVersions.V_21_140)
    assert len(boilers) == 3
    # Should have addresses 500, 550, 600

    # Test buffer addresses
    buffers = factory.buffer(Systems.VAMPAIR, 3, ApiVersions.V_21_140)
    assert len(buffers) == 3
    # Should have addresses 1900, 1920, 1940

    # Test fresh water module addresses
    modules = factory.fresh_water_modules(Systems.VAMPAIR, 3, ApiVersions.V_23_020)
    assert len(modules) == 3
    # Should have addresses 700, 725, 750


def test_factory_with_zero_count():
    """Test factory methods with zero count"""
    mock_modbus = MagicMock()
    factory = ComponentFactory(mock_modbus)

    # Test with zero count
    circuits = factory.heating_circuit(Systems.VAMPAIR, 0, ApiVersions.V_21_140)
    assert len(circuits) == 0

    boilers = factory.boiler(Systems.VAMPAIR, 0, ApiVersions.V_21_140)
    assert len(boilers) == 0

    buffers = factory.buffer(Systems.VAMPAIR, 0, ApiVersions.V_21_140)
    assert len(buffers) == 0
