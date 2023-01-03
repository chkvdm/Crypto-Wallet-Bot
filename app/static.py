from .models import Profile, Currency, Transaction_type, Balance, Transaction
from .models import session, profile_schema
from .errors import *
from .price_api import currency_prices
from flask import abort
from jsonschema import validate
import re
from decimal import Decimal
from datetime import datetime, timezone


# methods for validation a name and telegramm ID

class Validation():
  def __init__(self):
    self = self

  def user_schema_check(self, req):
    # validation JSON in the request
    if req.get_json(silent = True) == None:
      abort (400, description = "data not entered or incorrect")
    schema = {
      "type" : "object",
      "properties" : {
        "name": {"type" : "string"},
        "tg_user_id": {"type" : "number"}
      }
    }
    try: 
      validate(instance=req.json, schema=schema)
      return None
    except:
      abort(400, description = "wrong name or telegram ID")

  def trading_schema_check(self, req):
    # validation JSON in the request
    if req.get_json(silent = True) == None:
      abort (400, description = "data not entered or incorrect")
    schema = {
      "type" : "object",
      "properties" : {
        "ticker_buy": {"type": "string"},
        "ticker_sell": {"type": "string"},
        "amount_currency_buy": {"type": "number"}
      }
    }
    try: 
      validate(instance=req.json, schema=schema)
      return None
    except:
      abort(400, description = "wrong ticker or amount")

  def tg_user_id_validate(self, tg_user_id):
    # validation telegram ID format
    if re.fullmatch('[0-9]{4,32}', str(tg_user_id)) == None:
      abort (400, description = f"invalid telegram ID")
    # validation of availability a telegram ID 
    if not session.query(Profile).filter_by(tg_user_id = str(tg_user_id)).first():
      return None
    else:
      abort(403, description = f"The telegram ID '{tg_user_id}' is alredy exist.")

  def name_validate(self, name):
    # validation name format
    if re.fullmatch ('[a-z0-9_]{4,32}$', name) == None:
      abort(400, description = "invalid name format.")
    # validation of availability a name 
    if not session.query(Profile).filter_by(name = name).first():
      return None
    else:
      abort(403, description = f"The name '{name}' alredy exist.")


# user's profile methods

class UserProfile():
  def __init__(self):
    self = self

  def create(self, user_information):
    name = user_information['name']
    tg_user_id = user_information['tg_user_id']
    # validation name and telegram ID format
    if Validation().name_validate(name) == None and Validation().tg_user_id_validate(tg_user_id) == None:
      # create new user profile
      new_profile = Profile(name, tg_user_id)
      session.add(new_profile)
      session.commit()
      # accrual welcome benefit 10000 USDT
      Wallet().hello_user_balance(tg_user_id)
      profile = profile_schema.dump(session.query(Profile).filter_by(tg_user_id = str(tg_user_id)).one())
    return profile

  def get_information(self, tg_user_id):
    user_info = session.query(Profile).filter_by(tg_user_id = tg_user_id).first()
    if not user_info:
      abort(404, description = "user not found")
    user_info_result = profile_schema.dump(user_info)
    return user_info_result

  def update(self, user_information, tg_user_id):
    user_info = session.query(Profile).filter_by(tg_user_id = str(tg_user_id)).first()
    if not user_info:
      abort(404, description = "user not found")
    new_name = user_information['name']
    # validation of availability a new name 
    if Validation().name_validate(new_name) == None:
      profile_name = session.query(Profile).filter_by(tg_user_id = tg_user_id).first()
      profile_name.name = new_name
      session.add(profile_name)
      session.commit()
      user_with_new_name = profile_schema.dump(session.query(Profile).filter_by(tg_user_id = tg_user_id).one())
    return user_with_new_name

  def delete(self, tg_user_id):
    user_info = session.query(Profile).filter_by(tg_user_id = tg_user_id).first()
    if not user_info:
      abort(404, description = "user not found")
    session.delete(user_info)
    session.commit()
    return None


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
