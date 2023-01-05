from flask import abort
from .price_api import currency_prices
from .errors import *


# methods for currency

class CurrencyInfo():
  def __init__(self):
    self = self

  def check_currency_support(self, ticker):
    if ticker not in currency_prices:
      abort(400, description = f"this currency is not supported. We are supported: {', '.join(currency_prices)}")
    else:
      return None

  def get_price_value(self, ticker):
    if CurrencyInfo().check_currency_support(ticker) == None:
      currency_price = currency_prices[ticker]
      return currency_price