from decimal import Decimal
from pytest_flask.fixtures import client
from bookforex.view import truncate, money_to_float, moneyfmt, trades_view


# Test views
def test_validate_get_trades_view(client):
    assert client.get(url_for('trades_view')).status_code == 200
    #assert response.status_code == 400
    #assert response.json['message'] == INVALID_ACTION_MESSAGE


# Test utils views
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
