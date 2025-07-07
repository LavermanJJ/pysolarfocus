"""Tests for pysolarfocus core functionality"""

from pysolarfocus import (
    ApiVersions,
    DomesticHotWaterMode,
    HeatingCircuitCooling,
    HeatingCircuitMode,
    HeatPumpSgReadyMode,
    SolarfocusAPI,
    Systems,
)


def test_systems_enum_values():
    assert Systems.VAMPAIR.value == "Vampair"
    assert Systems.THERMINATOR.value == "Therminator"
    assert Systems.ECOTOP.value == "Ecotop"
    assert Systems.PELLETELEGANCE.value == "Pellet Elegance"
    assert Systems.OCTOPLUS.value == "Octoplus"


def test_api_versions_enum_values():
    assert ApiVersions.V_20_110.value == "20.110"
    assert ApiVersions.V_21_140.value == "21.140"
    assert ApiVersions.V_22_090.value == "22.090"
    assert ApiVersions.V_23_010.value == "23.010"
    assert ApiVersions.V_23_020.value == "23.020"
    assert ApiVersions.V_23_040.value == "23.040"
    assert ApiVersions.V_23_080.value == "23.080"
    assert ApiVersions.V_25_030.value == "25.030"


def test_api_version_comparison():
    """Test that version comparison works correctly"""
    assert ApiVersions.V_25_030.greater_or_equal("20.110")
    assert ApiVersions.V_25_030.greater_or_equal("25.030")
    assert not ApiVersions.V_21_140.greater_or_equal("25.030")
    assert ApiVersions.V_21_140.greater_or_equal("20.110")


def test_solarfocus_api_init_validation():
    """Test input validation during SolarfocusAPI initialization"""
    try:
        SolarfocusAPI(ip="localhost", heating_circuit_count=10)
        assert False, "Should raise assertion error for invalid heating circuit count"
    except AssertionError:
        pass

    try:
        SolarfocusAPI(ip="localhost", buffer_count=5)
        assert False, "Should raise assertion error for invalid buffer count"
    except AssertionError:
        pass

    try:
        SolarfocusAPI(ip="localhost", boiler_count=5)
        assert False, "Should raise assertion error for invalid boiler count"
    except AssertionError:
        pass

    try:
        SolarfocusAPI(ip="localhost", fresh_water_module_count=5)
        assert False, "Should raise assertion error for invalid fresh water module count"
    except AssertionError:
        pass

    try:
        SolarfocusAPI(ip="localhost", system="invalid")
        assert False, "Should raise assertion error for invalid system type"
    except AssertionError:
        pass

    # Valid initialization should work
    api = SolarfocusAPI(ip="localhost", heating_circuit_count=2, buffer_count=2, boiler_count=2, system=Systems.VAMPAIR, api_version=ApiVersions.V_25_030)
    assert api.system == Systems.VAMPAIR
    assert api.api_version == ApiVersions.V_25_030


def test_solarfocus_api_update_methods():
    """Test all update methods"""
    api = SolarfocusAPI(ip="localhost", heating_circuit_count=2, buffer_count=2, boiler_count=2, system=Systems.VAMPAIR, api_version=ApiVersions.V_25_030)

    # Components that don't belong to VAMPAIR system return True
    assert api.update_biomassboiler() == True
    assert api.update_solar() == True

    # Components that belong to VAMPAIR but can't connect return False
    assert api.update_heating() == False
    assert api.update_buffer() == False
    assert api.update_boiler() == False
    assert api.update_heatpump() == False
    assert api.update_photovoltaic() == False
    assert api.update_fresh_water_modules() == True
    assert api.update_circulation() == True
    assert api.update_differential_modules() == True

    # Overall update should return False since components can't connect
    assert api.update() == False


def test_solarfocus_api_setters():
    """Test setter methods with validation"""
    api = SolarfocusAPI(ip="localhost", heating_circuit_count=2, boiler_count=2, system=Systems.VAMPAIR)

    # Test invalid index handling
    assert api.set_heating_circuit_mode(5, HeatingCircuitMode.ALWAYS_ON) == False
    assert api.set_heating_circuit_cooling(5, HeatingCircuitCooling.COOLING) == False
    assert api.set_domestic_hot_water_mode(5, DomesticHotWaterMode.ALWAYS_ON) == False
    assert api.set_domestic_hot_water_single_charge(5, True) == False

    # Test heat pump specific setters with wrong system type
    api_therm = SolarfocusAPI(ip="localhost", system=Systems.THERMINATOR)
    assert api_therm.set_heat_pump_sg_ready_mode(HeatPumpSgReadyMode.NORMAL_OPERATION) == False
    assert api_therm.set_heat_pump_evu_lock(True) == False
