"""Tests for fresh water module cascade and circulation module components"""

from pysolarfocus import ApiVersions
from pysolarfocus.components.fresh_water_module import (
    CirculationModule,
    FreshWaterModule,
    FreshWaterModuleCascade,
)


class TestFreshWaterModuleCascade:
    """Test FreshWaterModuleCascade component"""

    def test_initialization_v23_040(self):
        """Test initialization with V23.040 API version"""
        cascade = FreshWaterModuleCascade(api_version=ApiVersions.V_23_040)

        assert cascade.input_address == 800
        assert hasattr(cascade, "state")
        assert hasattr(cascade, "total_flow_rate")
        assert hasattr(cascade, "target_temperature")

        # Check data value configurations
        assert cascade.state.address == 0
        assert cascade.total_flow_rate.address == 1
        assert cascade.total_flow_rate.multiplier == 0.1
        assert cascade.target_temperature.address == 2
        assert cascade.target_temperature.multiplier == 0.1

    def test_initialization_older_version(self):
        """Test initialization with older API version"""
        cascade = FreshWaterModuleCascade(api_version=ApiVersions.V_23_020)

        assert cascade.input_address == 800
        # Should only have basic initialization, no data values for older versions
        assert not hasattr(cascade, "total_flow_rate")
        assert not hasattr(cascade, "target_temperature")

    def test_custom_input_address(self):
        """Test initialization with custom input address"""
        cascade = FreshWaterModuleCascade(input_address=850, api_version=ApiVersions.V_23_040)
        assert cascade.input_address == 850


class TestCirculationModule:
    """Test CirculationModule component"""

    def test_initialization_v23_040(self):
        """Test initialization with V23.040 API version"""
        module = CirculationModule(api_version=ApiVersions.V_23_040)

        assert module.input_address == 850
        assert hasattr(module, "dhw_supply_temperature")
        assert hasattr(module, "dhw_flow_rate")

        # Check data value configurations
        assert module.dhw_supply_temperature.address == 0
        assert module.dhw_supply_temperature.multiplier == 0.1
        assert module.dhw_flow_rate.address == 1
        assert module.dhw_flow_rate.multiplier == 0.1

    def test_initialization_older_version(self):
        """Test initialization with older API version"""
        module = CirculationModule(api_version=ApiVersions.V_23_020)

        assert module.input_address == 850
        # Should only have basic initialization, no data values for older versions
        assert not hasattr(module, "dhw_supply_temperature")
        assert not hasattr(module, "dhw_flow_rate")

    def test_custom_input_address(self):
        """Test initialization with custom input address"""
        module = CirculationModule(input_address=900, api_version=ApiVersions.V_23_040)
        assert module.input_address == 900


class TestFreshWaterModuleUpdated:
    """Test the updated FreshWaterModule component"""

    def test_flow_rate_multiplier_fix(self):
        """Test that flow_rate now has correct multiplier (0.1)"""
        fwm = FreshWaterModule(api_version=ApiVersions.V_23_040)

        assert hasattr(fwm, "flow_rate")
        assert fwm.flow_rate.multiplier == 0.1

    def test_component_integration(self):
        """Test that all components can be initialized together"""
        fwm = FreshWaterModule(api_version=ApiVersions.V_23_040)
        cascade = FreshWaterModuleCascade(api_version=ApiVersions.V_23_040)
        circulation = CirculationModule(api_version=ApiVersions.V_23_040)

        # Check that all have different addresses
        assert fwm.input_address == 700
        assert cascade.input_address == 800
        assert circulation.input_address == 850

        # Check that they all have the expected attributes
        assert hasattr(fwm, "flow_rate")
        assert hasattr(cascade, "total_flow_rate")
        assert hasattr(circulation, "dhw_flow_rate")
