"""Tests for photovoltaic component"""

from pysolarfocus import ApiVersions
from pysolarfocus.components.base.data_value import DataValue
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
