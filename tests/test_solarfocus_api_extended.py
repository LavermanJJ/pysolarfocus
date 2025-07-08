"""Extended tests for SolarfocusAPI class"""
import unittest.mock as mock
from unittest.mock import MagicMock, patch

from pysolarfocus import (
    ApiVersions,
    DomesticHotWaterMode,
    HeatingCircuitCooling,
    HeatingCircuitHeatingMode,
    HeatingCircuitMode,
    HeatPumpSgReadyMode,
    SolarfocusAPI,
    Systems,
)


def test_solarfocus_api_connect():
    """Test SolarfocusAPI connect method"""
    with patch("pysolarfocus.ModbusConnector") as mock_modbus_class:
        mock_modbus_instance = MagicMock()
        mock_modbus_class.return_value = mock_modbus_instance

        api = SolarfocusAPI(ip="localhost")

        # Test successful connection
        mock_modbus_instance.connect.return_value = True
        result = api.connect()
        assert result is True

        # Test failed connection
        mock_modbus_instance.connect.return_value = False
        result = api.connect()
        assert result is False


def test_solarfocus_api_is_connected():
    """Test SolarfocusAPI is_connected property"""
    with patch("pysolarfocus.ModbusConnector") as mock_modbus_class:
        mock_modbus_instance = MagicMock()
        mock_modbus_class.return_value = mock_modbus_instance

        api = SolarfocusAPI(ip="localhost")

        # Test connected state
        mock_modbus_instance.is_connected = True
        assert api.is_connected is True

        # Test disconnected state
        mock_modbus_instance.is_connected = False
        assert api.is_connected is False


def test_solarfocus_api_repr():
    """Test SolarfocusAPI __repr__ method"""
    api = SolarfocusAPI(ip="localhost", system=Systems.VAMPAIR, api_version=ApiVersions.V_25_030)

    repr_str = repr(api)
    assert "SolarfocusAPI" in repr_str
    assert "Vampair" in repr_str
    assert "25.030" in repr_str
    assert "---" in repr_str


def test_solarfocus_api_update_individual_components():
    """Test individual component update methods"""
    with patch("pysolarfocus.ModbusConnector") as mock_modbus_class:
        mock_modbus_instance = MagicMock()
        mock_modbus_class.return_value = mock_modbus_instance

        api = SolarfocusAPI(ip="localhost", system=Systems.VAMPAIR, api_version=ApiVersions.V_25_030)

        # Mock component update methods to return False (simulate connection failure)
        for heating_circuit in api.heating_circuits:
            heating_circuit.update = MagicMock(return_value=False)

        for buffer in api.buffers:
            buffer.update = MagicMock(return_value=False)

        for boiler in api.boilers:
            boiler.update = MagicMock(return_value=False)

        for solar in api.solar:
            solar.update = MagicMock(return_value=False)

        api.heatpump.update = MagicMock(return_value=False)
        api.photovoltaic.update = MagicMock(return_value=False)

        # Test individual update methods
        assert api.update_heating() is False
        assert api.update_buffer() is False
        assert api.update_boiler() is False
        assert api.update_solar() is False
        assert api.update_heatpump() is False
        assert api.update_photovoltaic() is False


def test_solarfocus_api_update_success():
    """Test successful component updates"""
    with patch("pysolarfocus.ModbusConnector") as mock_modbus_class:
        mock_modbus_instance = MagicMock()
        mock_modbus_class.return_value = mock_modbus_instance

        api = SolarfocusAPI(ip="localhost", system=Systems.VAMPAIR, api_version=ApiVersions.V_25_030)

        # Mock component update methods to return True (simulate successful update)
        for heating_circuit in api.heating_circuits:
            heating_circuit.update = MagicMock(return_value=True)

        for buffer in api.buffers:
            buffer.update = MagicMock(return_value=True)

        for boiler in api.boilers:
            boiler.update = MagicMock(return_value=True)

        for solar in api.solar:
            solar.update = MagicMock(return_value=True)

        api.heatpump.update = MagicMock(return_value=True)
        api.photovoltaic.update = MagicMock(return_value=True)
        api.biomassboiler.update = MagicMock(return_value=True)

        for fresh_water_module in api.fresh_water_modules:
            fresh_water_module.update = MagicMock(return_value=True)

        for circulation in api.circulations:
            circulation.update = MagicMock(return_value=True)

        for differential_module in api.differential_modules:
            differential_module.update = MagicMock(return_value=True)

        # Test individual update methods
        assert api.update_heating() is True
        assert api.update_buffer() is True
        assert api.update_boiler() is True
        assert api.update_solar() is True
        assert api.update_heatpump() is True
        assert api.update_photovoltaic() is True
        assert api.update_biomassboiler() is True
        assert api.update_fresh_water_modules() is True
        assert api.update_circulation() is True
        assert api.update_differential_modules() is True


def test_solarfocus_api_setters_valid_indices():
    """Test setter methods with valid indices"""
    with patch("pysolarfocus.ModbusConnector") as mock_modbus_class:
        mock_modbus_instance = MagicMock()
        mock_modbus_class.return_value = mock_modbus_instance

        api = SolarfocusAPI(ip="localhost", heating_circuit_count=2, boiler_count=2, system=Systems.VAMPAIR)

        # Mock the data value commit methods
        for heating_circuit in api.heating_circuits:
            heating_circuit.mode = MagicMock()
            heating_circuit.mode.commit = MagicMock(return_value=True)
            heating_circuit.cooling = MagicMock()
            heating_circuit.cooling.commit = MagicMock(return_value=True)
            heating_circuit.heating_mode = MagicMock()
            heating_circuit.heating_mode.commit = MagicMock(return_value=True)

        for boiler in api.boilers:
            boiler.mode = MagicMock()
            boiler.mode.commit = MagicMock(return_value=True)
            boiler.single_charge = MagicMock()
            boiler.single_charge.commit = MagicMock(return_value=True)

        api.heatpump.smart_grid = MagicMock()
        api.heatpump.smart_grid.commit = MagicMock(return_value=True)
        api.heatpump.evu_lock = MagicMock()
        api.heatpump.evu_lock.commit = MagicMock(return_value=True)

        # Test valid indices
        assert api.set_heating_circuit_mode(0, HeatingCircuitMode.ALWAYS_ON) is True
        assert api.set_heating_circuit_mode(1, HeatingCircuitMode.AUTOMATIC) is True
        assert api.set_heating_circuit_cooling(0, HeatingCircuitCooling.COOLING) is True
        assert api.set_heating_circuit_heating_mode(0, HeatingCircuitHeatingMode.HEATING) is True
        assert api.set_domestic_hot_water_mode(0, DomesticHotWaterMode.ALWAYS_ON) is True
        assert api.set_domestic_hot_water_single_charge(0, True) is True
        assert api.set_heat_pump_sg_ready_mode(HeatPumpSgReadyMode.NORMAL_OPERATION) is True
        assert api.set_heat_pump_evu_lock(True) is True


def test_solarfocus_api_setters_commit_failure():
    """Test setter methods when commit fails"""
    with patch("pysolarfocus.ModbusConnector") as mock_modbus_class:
        mock_modbus_instance = MagicMock()
        mock_modbus_class.return_value = mock_modbus_instance

        api = SolarfocusAPI(ip="localhost", heating_circuit_count=1, boiler_count=1, system=Systems.VAMPAIR)

        # Mock the data value commit methods to return False
        api.heating_circuits[0].mode = MagicMock()
        api.heating_circuits[0].mode.commit = MagicMock(return_value=False)

        api.boilers[0].mode = MagicMock()
        api.boilers[0].mode.commit = MagicMock(return_value=False)

        # Test commit failure
        assert api.set_heating_circuit_mode(0, HeatingCircuitMode.ALWAYS_ON) is False
        assert api.set_domestic_hot_water_mode(0, DomesticHotWaterMode.ALWAYS_ON) is False


def test_solarfocus_api_different_systems():
    """Test API with different system types"""
    with patch("pysolarfocus.ModbusConnector") as mock_modbus_class:
        mock_modbus_instance = MagicMock()
        mock_modbus_class.return_value = mock_modbus_instance

        # Mock successful reads
        def mock_read_input_registers(slices, count):
            return (True, [0] * count)

        def mock_read_holding_registers(slices, count):
            return (True, [0] * count)

        mock_modbus_instance.read_input_registers.side_effect = mock_read_input_registers
        mock_modbus_instance.read_holding_registers.side_effect = mock_read_holding_registers

        # Test THERMINATOR system
        api_therm = SolarfocusAPI(ip="localhost", system=Systems.THERMINATOR)
        assert api_therm.system == Systems.THERMINATOR
        assert api_therm.update_biomassboiler() is True  # Should update for THERMINATOR
        assert api_therm.update_heatpump() is True  # Should return True for non-VAMPAIR

        # Test ECOTOP system
        api_ecotop = SolarfocusAPI(ip="localhost", system=Systems.ECOTOP)
        assert api_ecotop.system == Systems.ECOTOP
        assert api_ecotop.update_biomassboiler() is True  # Should update for ECOTOP

        # Test PELLETELEGANCE system
        api_pellet = SolarfocusAPI(ip="localhost", system=Systems.PELLETELEGANCE)
        assert api_pellet.system == Systems.PELLETELEGANCE
        assert api_pellet.update_biomassboiler() is True  # Should return True for non-THERMINATOR/ECOTOP

    # Test OCTOPLUS system
    api_octoplus = SolarfocusAPI(ip="localhost", system=Systems.OCTOPLUS)
    assert api_octoplus.system == Systems.OCTOPLUS


def test_solarfocus_api_version_dependent_features():
    """Test API features that depend on version"""
    # Test with older API version
    api_old = SolarfocusAPI(ip="localhost", api_version=ApiVersions.V_21_140)
    assert api_old.update_fresh_water_modules() is True  # Should return True for older versions
    assert api_old.update_circulation() is True  # Should return True for older versions
    assert api_old.update_differential_modules() is True  # Should return True for older versions

    # Test with newer API version
    api_new = SolarfocusAPI(ip="localhost", api_version=ApiVersions.V_25_030)
    # These should have actual components for newer versions
    assert hasattr(api_new, "fresh_water_modules")
    assert hasattr(api_new, "circulations")
    assert hasattr(api_new, "differential_modules")


def test_solarfocus_api_solar_count_validation():
    """Test solar count validation based on API version"""
    # Test with older API version (max 1 solar)
    api_old = SolarfocusAPI(ip="localhost", solar_count=1, api_version=ApiVersions.V_21_140)
    assert len(api_old.solar) == 1

    # Test with newer API version (max 4 solar)
    api_new = SolarfocusAPI(ip="localhost", solar_count=4, api_version=ApiVersions.V_25_030)
    assert len(api_new.solar) == 4


def test_solarfocus_api_circulation_and_differential_validation():
    """Test circulation and differential module validation"""
    # Test with API version that supports these features
    api = SolarfocusAPI(ip="localhost", circulation_count=3, differential_module_count=2, api_version=ApiVersions.V_25_030)

    assert len(api.circulations) == 3
    assert len(api.differential_modules) == 2


def test_solarfocus_api_fresh_water_modules_validation():
    """Test fresh water modules validation"""
    # Test with API version that supports fresh water modules
    api = SolarfocusAPI(ip="localhost", fresh_water_module_count=3, api_version=ApiVersions.V_23_020)

    assert len(api.fresh_water_modules) == 3
