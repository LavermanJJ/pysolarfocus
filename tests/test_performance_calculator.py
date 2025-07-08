"""Tests for PerformanceCalculator"""

from pysolarfocus.components.base.data_value import DataValue
from pysolarfocus.components.base.performance_calculator import PerformanceCalculator


def test_performance_calculator_init():
    """Test PerformanceCalculator initialization"""
    data1 = DataValue(address=0)
    data2 = DataValue(address=1)

    calc = PerformanceCalculator(data1, data2)

    assert calc.nominator == data1
    assert calc.denominator == data2


def test_performance_calculator_value():
    """Test PerformanceCalculator value property"""
    data1 = DataValue(address=0)
    data2 = DataValue(address=1)

    # Set some values
    data1.value = 100
    data2.value = 50

    calc = PerformanceCalculator(data1, data2)

    # Should calculate nominator / denominator
    assert calc.value == 2.0


def test_performance_calculator_scaled_value():
    """Test PerformanceCalculator scaled_value property"""
    data1 = DataValue(address=0)
    data2 = DataValue(address=1)

    # Set some values
    data1.value = 100
    data2.value = 25

    calc = PerformanceCalculator(data1, data2)

    # scaled_value should be same as value
    assert calc.scaled_value == 4.0
    assert calc.scaled_value == calc.value


def test_performance_calculator_zero_division():
    """Test PerformanceCalculator with zero division"""
    data1 = DataValue(address=0)
    data2 = DataValue(address=1)

    # Set denominator to zero
    data1.value = 100
    data2.value = 0

    calc = PerformanceCalculator(data1, data2)

    # Should handle division by zero gracefully
    assert calc.value == 0.0


def test_performance_calculator_with_multipliers():
    """Test PerformanceCalculator with data values that have multipliers"""
    data1 = DataValue(address=0, multiplier=0.1)
    data2 = DataValue(address=1, multiplier=0.1)

    # Set raw values
    data1.value = 1000  # scaled value = 100
    data2.value = 500  # scaled value = 50

    calc = PerformanceCalculator(data1, data2)

    # Should use scaled values for calculation
    assert calc.value == 2.0


def test_performance_calculator_negative_values():
    """Test PerformanceCalculator with negative values"""
    data1 = DataValue(address=0)
    data2 = DataValue(address=1)

    # Set negative values
    data1.value = -100
    data2.value = 25

    calc = PerformanceCalculator(data1, data2)

    # Should handle negative values
    assert calc.value == -4.0


def test_performance_calculator_zero_values():
    """Test PerformanceCalculator with zero values"""
    data1 = DataValue(address=0)
    data2 = DataValue(address=1)

    # Set nominator to zero
    data1.value = 0
    data2.value = 50

    calc = PerformanceCalculator(data1, data2)

    # Should return zero
    assert calc.value == 0.0
