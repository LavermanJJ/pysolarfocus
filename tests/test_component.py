from pysolarfocus.components.base.component import Component
from pysolarfocus.components.base.data_value import DataValue


def _assign_absolute_addresses(data_values: list[DataValue], start_address):
    for data_value in data_values:
        data_value.absolut_address = start_address


def test_calculate_ranges_handles_simple_case():
    absolute_address = 500
    data_values = [
        DataValue(address=0),
        DataValue(address=1),
        DataValue(address=2),
        DataValue(address=3),
        DataValue(address=4),
    ]
    _assign_absolute_addresses(data_values, absolute_address)
    slices = Component._calculate_ranges(data_values)
    assert len(slices) == 1
    assert slices[0].absolute_address == absolute_address
    assert slices[0].relative_address == 0
    assert slices[0].count == 5


def test_calculate_ranges_handles_skipped_values():
    # Tests if 503 is skipped
    absolute_address = 500
    data_values = [
        DataValue(address=0),
        DataValue(address=1),
        DataValue(address=2),
        DataValue(address=4),
        DataValue(address=5),
    ]
    _assign_absolute_addresses(data_values, absolute_address)
    slices = Component._calculate_ranges(data_values)
    assert len(slices) == 2
    assert slices[0].absolute_address == absolute_address
    assert slices[0].relative_address == 0
    assert slices[0].count == 3
    assert slices[1].absolute_address == 504
    assert slices[1].relative_address == 4
    assert slices[1].count == 2


def test_calculate_ranges_handles_multiregister_values():
    absolute_address = 500
    data_values = [
        DataValue(address=0, count=2),
        DataValue(address=2, count=3),
        DataValue(address=5),
    ]
    _assign_absolute_addresses(data_values, absolute_address)
    slices = Component._calculate_ranges(data_values)
    assert len(slices) == 1
    assert slices[0].absolute_address == absolute_address
    assert slices[0].relative_address == 0
    assert slices[0].count == 6


def test_calculate_ranges_handles_multiregister_and_skipped_values():
    absolute_address = 500
    data_values = [
        DataValue(address=0, count=2),
        DataValue(address=2, count=3),
        DataValue(address=20, count=10),
    ]
    _assign_absolute_addresses(data_values, absolute_address)
    slices = Component._calculate_ranges(data_values)
    assert len(slices) == 2
    assert slices[0].absolute_address == absolute_address
    assert slices[0].relative_address == 0
    assert slices[0].count == 5
    assert slices[1].absolute_address == absolute_address + 20
    assert slices[1].relative_address == 20
    assert slices[1].count == 10


def test_calculate_ranges_handles_multiple_skipped_values():
    # Test the Heating Circuit configuration
    absolute_address = 32600
    data_values = [
        DataValue(address=0),
        DataValue(address=2),
        DataValue(address=3),
        DataValue(address=5),
        DataValue(address=6),
        DataValue(address=7),
    ]
    _assign_absolute_addresses(data_values, absolute_address)
    slices = Component._calculate_ranges(data_values)
    assert len(slices) == 3

    assert slices[0].absolute_address == absolute_address
    assert slices[0].relative_address == 0
    assert slices[0].count == 1

    assert slices[1].absolute_address == absolute_address + 2
    assert slices[1].relative_address == 2
    assert slices[1].count == 2

    assert slices[2].absolute_address == absolute_address + 5
    assert slices[2].relative_address == 5
    assert slices[2].count == 3
