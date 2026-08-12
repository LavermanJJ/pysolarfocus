"""Tests for photovoltaic component"""

from unittest.mock import MagicMock

from pysolarfocus import ApiVersions
from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.base.enums import RegisterTypes
from pysolarfocus.components.photovoltaic import Photovoltaic


def test_photovoltaic_data_values():
    """Test data values for photovoltaic component"""
    pv = Photovoltaic(api_version=ApiVersions.V_25_030)

    # Check basic attributes
    assert isinstance(pv.power, DataValue)
    assert isinstance(pv.house_consumption, DataValue)
    assert isinstance(pv.heatpump_consumption, DataValue)
    assert isinstance(pv.grid_import, DataValue)
    assert isinstance(pv.grid_export, DataValue)
    assert isinstance(pv.overcharge_possible, DataValue)
    assert isinstance(pv.overcharge_active, DataValue)
    assert isinstance(pv.smart_meter, DataValue)
    assert isinstance(pv.photovoltaic, DataValue)
    assert isinstance(pv.grid_im_export, DataValue)

    # Check addresses
    assert pv.power.address == 0
    assert pv.house_consumption.address == 2
    assert pv.heatpump_consumption.address == 4
    assert pv.grid_import.address == 6
    assert pv.grid_export.address == 8
    assert pv.overcharge_possible.address == 10
    assert pv.overcharge_active.address == 11
    assert pv.smart_meter.address == 0
    assert pv.photovoltaic.address == 1
    assert pv.grid_im_export.address == 2

    # The HEMS setpoint has been introduced with 26.020
    assert not hasattr(pv, "hems_target_electrical_power")


def test_photovoltaic_hems_target_electrical_power():
    """Test the HEMS setpoint (register 33415) added in api version 26.020"""
    pv = Photovoltaic(api_version=ApiVersions.V_26_020)

    assert isinstance(pv.hems_target_electrical_power, DataValue)
    assert pv.hems_target_electrical_power.register_type == RegisterTypes.HOLDING
    assert pv.hems_target_electrical_power.address == 8
    assert pv.hems_target_electrical_power.count == 1
    # W, unscaled according to the Solarfocus specification
    assert pv.hems_target_electrical_power.multiplier is None

    pv.initialize(MagicMock())
    assert pv.hems_target_electrical_power.get_absolute_address() == 33415


def test_photovoltaic_holding_slices_skip_foreign_registers():
    """Registers 33410-33414 belong to other components and must not be read"""
    pv = Photovoltaic(api_version=ApiVersions.V_26_020).initialize(MagicMock())

    assert pv.holding_count == 9
    slices = pv.holding_slices
    assert len(slices) == 2

    assert slices[0].absolute_address == 33407
    assert slices[0].relative_address == 0
    assert slices[0].count == 3

    assert slices[1].absolute_address == 33415
    assert slices[1].relative_address == 8
    assert slices[1].count == 1


def test_photovoltaic_parses_hems_target_electrical_power():
    """The value of register 33415 is taken from the last holding register"""
    pv = Photovoltaic(api_version=ApiVersions.V_26_020).initialize(MagicMock())

    # 33407, 33408, 33409, gap (33410-33414), 33415
    assert pv._parse([100, 200, 300, 0, 0, 0, 0, 0, 2500], RegisterTypes.HOLDING)

    assert pv.smart_meter.value == 100
    assert pv.photovoltaic.value == 200
    assert pv.grid_im_export.value == 300
    assert pv.hems_target_electrical_power.value == 2500
    assert pv.hems_target_electrical_power.scaled_value == 2500
