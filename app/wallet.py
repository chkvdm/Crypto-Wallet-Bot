from decimal import Decimal
from flask import abort
from .models import session
from .price_api import currency_prices
from datetime import datetime, timezone
from .models import Profile, Currency, Transaction_type, Balance, Transaction
from .currency_info import CurrencyInfo
from .errors import *


# user's wallet methods

class Wallet():
  def __init__(self):
    self = self

  def hello_user_balance(self, tg_user_id):
    profile_id = (session.query(Profile).filter_by(tg_user_id = str(tg_user_id)).one()).id
    if not profile_id:
      abort (404, description = "User not found")
    # welcome benefit = 10000.0 USDT
    hello_usdt_bonus = 10000.0
      # user uuid 
      # uuid - the value of the field 'id' that is automatically assigned to the user at the time of registration. 
      # For convenience, in all functions, we make the value of the uuid field equal to the variable 'profile_id'
    # welcome benefit money transfer
    hello_usdt_bonus_top_up = Balance(profile_id, (session.query(Currency).filter_by(name = 'USDT').one()).id, hello_usdt_bonus)
    session.add(hello_usdt_bonus_top_up)
    # welcome benefit money transfer log
    hello_transaction_log = Transaction(profile_id, datetime.now(timezone.utc).isoformat(), (session.query(Currency).filter_by(name = 'USDT').one()).id, hello_usdt_bonus,\
      (session.query(Transaction_type).filter_by(name = 'hello bonus').one()).id)
    session.add(hello_transaction_log)
    session.commit()

  def user_balance(self, tg_user_id):
    profile_id = session.query(Profile).filter_by(tg_user_id = tg_user_id).first()
    if not profile_id:
      abort (404, description = f"User not found")
    user_balance_list = session.query(Balance.total, Currency.name).\
      join(Currency, Balance.currency_id == Currency.id).filter(Balance.profile_id == profile_id.id).all()
    if not user_balance_list:
      return 'You do not have the currency in wallet'
    else:
      user_balance_list = [
        {
          'total':row.total,
          'сurrency':row.name
        } for row in user_balance_list
      ]
      return user_balance_list

  def user_transaction(self, tg_user_id):
    profile_id = session.query(Profile).filter_by(tg_user_id = tg_user_id).first()
    if not profile_id:
      abort (404, description = f"User not found")
    user_transaction_list = session.query(Transaction.timestamp, Transaction.amount, Currency.name.label("currency"), Transaction_type.name).\
      join(Currency, Transaction.currency_id == Currency.id). \
        join(Transaction_type, Transaction.transaction_type_id == Transaction_type.id). \
          filter(Transaction.profile_id == profile_id.id). \
            order_by(Transaction.timestamp.desc()).limit(10).all()
    if not user_transaction_list:
      return 'No transactions available'
    else:
      user_transaction_list = [
        {
          'timestamp':row.timestamp,
          'amount':row.amount,
          'currency':row.currency,
          'transaction_type':row.name
        } for row in user_transaction_list
      ]
      return user_transaction_list

  def exchange_rate(ticker_sell, ticker_buy):
    return (Decimal(currency_prices[ticker_sell] / currency_prices[ticker_buy]))

  def swap(currency_sell_id, currency_buy_id, amount_currency_sell, ticker_sell, ticker_buy, profile_id):
    # sele transaction
    sell_on_balance = session.query(Balance).filter_by(profile_id = profile_id, currency_id = currency_sell_id).first()
    sell_on_balance.total -= Decimal(amount_currency_sell)
    # sale transaction log
    sell_data_log = Transaction(profile_id, datetime.now(timezone.utc).isoformat(), currency_sell_id, amount_currency_sell,\
      (session.query(Transaction_type).filter_by(name = 'sell').one()).id)
    session.add(sell_data_log)
    # buy transaction
    buy_on_balance = session.query(Balance).filter_by(profile_id = profile_id, currency_id = currency_buy_id).first()
    buy_on_balance.total += Decimal(amount_currency_sell) * Wallet.exchange_rate(ticker_sell, ticker_buy)
    # buy transaction log
    buy_data_log = Transaction(profile_id, datetime.now(timezone.utc).isoformat(), currency_buy_id, Decimal(amount_currency_sell) * Wallet.exchange_rate(ticker_sell, ticker_buy),\
      (session.query(Transaction_type).filter_by(name = 'buy').one()).id)
    session.add(buy_data_log)
    session.add(sell_on_balance, buy_on_balance)
    session.commit()

  def currency_sell_control(currency_sell_id, ticker_buy, ticker_sell, amount_currency_buy, profile_id):
    # check availability currency which sell on balance
    check_currency_sell = session.query(Balance).filter_by(profile_id = profile_id, currency_id = currency_sell_id).first()
    if not check_currency_sell:
      abort(404, description = f"You do not have {ticker_sell}")
    # validation amount
    if check_currency_sell.total < Decimal(amount_currency_buy) / Wallet.exchange_rate(ticker_sell, ticker_buy):
      abort(404, description = "you do not have enough funds")

  def buy(self, tg_user_id, trading_information):
    # ticker_sell - currency to change
    # ticker_buy - currency to which we change
    ticker_buy = trading_information['ticker_buy']
    ticker_sell = trading_information['ticker_sell']
    amount_currency_buy = trading_information['amount_currency_buy']
    # currency support check
    CurrencyInfo().check_currency_support(ticker_buy)
    CurrencyInfo().check_currency_support(ticker_sell)
    currency_buy_id = (session.query(Currency).filter_by(name = ticker_buy).one()).id
    currency_sell_id = (session.query(Currency).filter_by(name = ticker_sell).one()).id
    profile_id = (session.query(Profile).filter_by(tg_user_id = tg_user_id).one()).id
    # validation availability currency which sell on balance
    Wallet.currency_sell_control(currency_sell_id, ticker_buy, ticker_sell, amount_currency_buy, profile_id)
    # check field with currency which we buy in table 'balance' in data base
    currency_buy_in_wallet = session.query(Balance).filter_by(profile_id = profile_id, currency_id = currency_buy_id).first()
    if not currency_buy_in_wallet:
      new_currency_in_wallet = Balance(profile_id, currency_buy_id, 0.0)
      session.add(new_currency_in_wallet)
      session.commit()
    amount_currency_sell = Decimal(amount_currency_buy) / Wallet.exchange_rate(ticker_sell, ticker_buy)
    Wallet.swap(currency_sell_id, currency_buy_id, amount_currency_sell, ticker_sell, ticker_buy, profile_id)

  def sell(self, tg_user_id, trading_information):
    # ticker_sell - currency to change
    # ticker_buy - currency to which we change
    ticker_sell = trading_information['ticker_sell']
    ticker_buy = trading_information['ticker_buy']
    amount_currency_sell = trading_information['amount_currency_sell']
    CurrencyInfo().check_currency_support(ticker_buy)
    CurrencyInfo().check_currency_support(ticker_sell)
    amount_currency_buy = Decimal(amount_currency_sell) * Wallet.exchange_rate(ticker_sell, ticker_buy)
    trading_sell_information = {
      "ticker_sell": ticker_sell,
      "ticker_buy": ticker_buy,
      "amount_currency_buy": amount_currency_buy
    }
    Wallet.buy(self, tg_user_id, trading_sell_information)