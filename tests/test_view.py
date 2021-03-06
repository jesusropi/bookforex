""" Test some functions of the module. It is necessary to implement tests for
views, database and other features, thus guiding the development tests.
For lack of time, they are included for show the line of work.
"""
from decimal import Decimal
from bookforex.view import truncate_two, money_to_float, moneyfmt


def test_truncate():
    assert truncate(456.678, 2) == 456.67
    assert truncate(456.6, 2) == 456.6
    assert truncate(456, 2) == 456
    assert truncate(456.333, 1) == 456.3
    assert truncate(12.123456, 3) == 12.123


def test_money_to_float():
    assert money_to_float('3.456,34') == 3456.34
    assert money_to_float('3.000.878,99') == 3000878.99
    assert money_to_float('0,00034') == 0.00034
    assert money_to_float('10') == 10


def test_moneyfmt():
    assert moneyfmt(Decimal(3000878.99), places=2, curr='', sep='.', dp=',',
                    pos='', neg='-', trailneg='') == '3.000.878,99'
    assert moneyfmt(Decimal(1034.9987), places=2, curr='', sep='.', dp=',',
                    pos='', neg='-', trailneg='') == '1.035,00'
    assert moneyfmt(Decimal(12), places=2, curr='', sep='.', dp=',',
                    pos='', neg='-', trailneg='') == '12,00'
    assert moneyfmt(Decimal(0), places=2, curr='', sep='.', dp=',',
                    pos='', neg='-', trailneg='') == '0,00'
