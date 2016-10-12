import string
import random
import json
import requests
from flask import Flask, jsonify, request, render_template, redirect, url_for
from datetime import datetime
from decimal import Decimal
from bookforex import app, db
from model import Trade

FIXIER_URL = 'http://api.fixer.io/latest?base='


@app.route('/')
def trades_view():
    """ View: render index table with trades booked

    :return: render template index.html
    """
    values = Trade.query.all()

    for v in values:
        v.date_booked = datetime_to_str_date(v.date_booked)
        v.buy_amount = moneyfmt(Decimal(v.buy_amount),
                                places=2, sep='.', dp=',', neg='-')
        v.sell_amount = moneyfmt(Decimal(v.sell_amount),
                                 places=2, sep='.', dp=',', neg='-')
    return render_template('index.html', query=values)


@app.route('/create-trade')
def create_trade_view(name=None):
    return render_template('create-trade.html', name=name)


@app.route('/trade', methods=["POST"])
def save_trade_form():
    """Save validate new trade at DB or render error message if it is not valid

    :return: render index table if no errors, else error template
    """
    base = requests.get(FIXIER_URL + request.form['sellcurrency'])
    if base.status_code == 200:
        fixer = base.json()

        if validate_trade(request, fixer):
                rate = fixer['rates'][request.form['buycurrency']]
                trade = Trade(generate_key(),
                              request.form['sellcurrency'],
                              money_to_float(request.form['sellamount']),
                              request.form['buycurrency'],
                              money_to_float(request.form['buyamount']),
                              rate, datetime.now())
        else:
            template = "Form info: Sell CCY: {}, Sell amount {}, Buy CCY {}, \
                        Buy Amount {}".format(request.form['sellcurrency'],
                                              request.form['sellamount'],
                                              request.form['buycurrency'],
                                              request.form['buyamount'])
            return render_template('create-trade-error.html',
                                   message="Sorry, data form incorrect (info: \
                                   " + template + ")...")

        db.session.add(trade)
        db.session.commit()

    else:
        return render_template('create-trade-error.html',
                               message="Sorry, can't connect to Fixer \
                               Server (status code: \
                               " + str(base.status_code) + ")...")
    return redirect(url_for('trades_view'))


@app.errorhandler(404)
def page_not_found(e):
    """Manage 404 error. Render template.

    :param int: Error 404
    :return: template and error code
    """
    return render_template('404.html'), 404


def validate_trade(request, fixer):
    """ Returns True if the validation was well. Checks in server Fixer.

    :param dict request: Data from form
    :param dict fixer: Fixers response json for that request base
    :return boolean
    """
    sell_amount = request.form['sellamount']
    buy_amount = request.form['buyamount']
    rates = fixer['rates'].get(request.form['buycurrency'])

    buy_amount_fixer = moneyfmt(Decimal(truncate((rates *
                                money_to_float(sell_amount)), 2)),
                                places=2, sep='.', dp=',', neg='-')

    if ((request.form['sellcurrency'] == fixer['base']) and (rates) and
            (buy_amount_fixer == str(buy_amount))):
        return True
    else:
        return False


def truncate(number, zeros):
    """Truncate the number without rounding to two decimal places
    (eg. 456.678 -> 456.67)

    :param float number: Float to truncate
    :return float
    """
    return math.floor(number * (10 ** zeros)) / (10 ** zeros)


def money_to_float(money):
    """Convert money string to float (eg. '3.456,34' -> 3456.34)

    :param srt money: String to convert
    :return float
    """
    return float((money.replace('.', '')).replace(',', '.'))


def datetime_to_str_date(date):
    """Converts date to format string

    :param Datetime: date
    :return str
    """
    return date.strftime("%d/%m/%Y %H:%M")


def generate_id(size=7, chars=string.ascii_uppercase + string.digits):
    """Generate random str (7, by default, alphanumerics)

    :param Int: size
    :param chars: string.ascii_uppercase + string.digits
    return str
    """
    return ''.join(random.choice(chars) for _ in range(size))


def generate_key():
    """Return random and unique key with the next format: 'TR' + 7 alphanumerics

    :return: key
    """
    unique = False
    result = 1
    key = ''
    while (not unique):
        key = generate_id()
        result = db.session.query(db.exists().where(Trade.id == key)).scalar()
        if not result:
            unique = True
    return 'TR' + key


def moneyfmt(value, places=2, curr='', sep=',', dp='.', pos='',
             neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    :param Int places: Required number of places after the decimal point
    :param str curr: Optional currency symbol before the sign (may be blank)
    :param str sep: Optional grouping separator (comma, period, space,
    or blank)
    :param str dp: Decimal point indicator (comma or period) only specify as
    blank when places is zero
    :param str pos: Optional sign for positive numbers: '+', space or blank
    :param str neg: Optional sign for negative numbers: '-', '(',
    space or blank
    :param str trailneg: Optional trailing minus indicator:  '-', ')', space or
    blank
    :return: Money str
    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
            build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))
