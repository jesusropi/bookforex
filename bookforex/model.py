from bookforex import db


class Trade(db.Model):
    id = db.Column(db.String, primary_key=True, autoincrement=False)
    sell_currency = db.Column(db.String)
    sell_amount = db.Column(db.Float)
    buy_currency = db.Column(db.String)
    buy_amount = db.Column(db.Float)
    rate = db.Column(db.Float)
    date_booked = db.Column(db.DateTime)

    def __init__(self, id, sell_currency, sell_amount, buy_currency, 
    buy_amount, rate, date_booked):
        self.id = id
        self.sell_currency = sell_currency
        self.sell_amount = sell_amount
        self.buy_currency = buy_currency
        self.buy_amount = buy_amount
        self.rate = rate
        self.date_booked = date_booked
