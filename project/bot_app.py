import requests
import re
from decimal import Decimal
from datetime import datetime
from models import Profile, Currency, Transaction_type, Balance, Transaction
from models import session 
from flask import Flask, request, jsonify, abort
from flask_marshmallow import Marshmallow


# API request for currency price

def currency_price(currency):
    service_url = 'https://api.coincap.io/v2/assets/'
    url = service_url + currency
    response = requests.get(url)
    js = response.json()
    return (js['data']['priceUsd'])

bitcoin = currency_price('bitcoin')
ethereum = currency_price('ethereum')
aragon = currency_price('aragon')
solana = currency_price('solana')
dogecoin = currency_price('dogecoin')

currency_prices = {
  'USDT' : 1,
  'BTC' : float(bitcoin), 
  'ETH' : float(ethereum), 
  'ANT' : float(aragon), 
  'SOL' : float(solana), 
  'DOGE' : float(dogecoin)
  }


# create datetime isoformat variable

dt = datetime.now()
dt = dt.isoformat()


# Old code without flask


#currency_prices for testing without Flask. Only with user class functions

# currency_prices = {
#   1 : 1, # USDT
#   2 : 18828.0, # BTC
#   3 : 1356.0, # ETH
#   4 : 237.2, # BNB
#   5 : 65.0, # SOL
#   6 : 0.05 # DOGE
#   }


#for key, val in currency_prices.items():
  #print (key, (': {}$').format(val))


# class User():

#   def __init__(self, name, tg_user_id):
#     self.name = name
#     self.tg_user_id = tg_user_id
#     profile_check = session.query(Profile).filter_by(name = name, tg_user_id = tg_user_id).first()
#     if not profile_check:
#       new_profile = Profile(name, tg_user_id)
#       session.add(new_profile)
#       session.commit()
#       uuid = (session.query(Profile).filter_by(name = name, tg_user_id = tg_user_id).first()).id
#       start_balance = Balance(uuid, 1, 10000.0)
#       session.add(start_balance)
#       session.commit()
#     uuid = (session.query(Profile).filter_by(name = name, tg_user_id = tg_user_id).first()).id
#     self.uuid = uuid
    
#   # def __repr__(self):
#   #   return (('Welcome {}!\nYou balance: {},').format(self.name, self.balance))
  
#   def get_balance(self):
#     wallet = []
#     for row in session.query(Balance).filter(Balance.profile_id == self.uuid):
#       wallet.append(row)
#     return wallet

#   def exchange_rate(self, currency_sell, currency_buy):
#     return (Decimal(currency_prices[currency_sell] / currency_prices[currency_buy]))

#   def swap(self, currency_sell, currency_buy, amount_currency_sell):
#     sell_on_balance = session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_sell).first()
#     if amount_currency_sell > sell_on_balance.total:
#       raise Exception ("You don't have enough funds")
#     sell_on_balance.total -= Decimal(amount_currency_sell)
#     sell_data_log = Transaction(self.uuid, dt, currency_sell, amount_currency_sell, 2)
#     session.add(sell_data_log)
#     session.commit()

#     buy_on_balance = session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_buy).first()
#     buy_on_balance.total += Decimal(amount_currency_sell) * User.exchange_rate(self, currency_sell, currency_buy)
#     buy_data_log = Transaction(self.uuid, dt, currency_buy, Decimal(amount_currency_sell) * User.exchange_rate(self, currency_sell, currency_buy), 1)
#     session.add(buy_data_log)
#     session.commit()
#     session.add(sell_on_balance, buy_on_balance)
#     session.commit()

#   def buy(self, currency_buy, currency_sell, amount_currency_buy):
#     check_currency_sell = session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_sell).first()
#     if not check_currency_sell:
#       raise Exception ("you don't have the currency for which you want to buy")
#     currency_buy_in_wallet = session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_buy).first()
#     if not currency_buy_in_wallet:
#       new_currency_in_wallet = Balance(self.uuid, currency_buy, 0.0)
#       session.add(new_currency_in_wallet)
#       session.commit()
#     amount_currency_sell = Decimal(amount_currency_buy) / User.exchange_rate(self, currency_sell, currency_buy)
#     User.swap(self, currency_sell, currency_buy, amount_currency_sell)

#   def sell(self, currency_sell, currency_buy, amount_currency_sell):
#     check_currency_sell =  session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_sell).first()
#     if not check_currency_sell:
#       raise Exception ("you don't have the currency for sell")
#     currency_buy_in_wallet = session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_buy).first()
#     if not currency_buy_in_wallet:
#       new_currency_in_wallet = Balance(self.uuid, currency_buy, 0.0)
#       session.add(new_currency_in_wallet)
#       session.commit()
#     User.swap(self, currency_sell, currency_buy, amount_currency_sell)





###############   Actual code   ###############

app = Flask(__name__)
ma = Marshmallow(app)


# create Marshmallow model

class ProfileSchema(ma.Schema):
  class Meta:
    fields = ('name', 'tg_user_id')

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)


class BalanceSchema(ma.Schema):
  class Meta:
    fields = ('profile_id', 'currency_id', 'total')

balance_schema = BalanceSchema()
balances_schema = BalanceSchema(many=True)


class TransactionSchema(ma.Schema):
  class Meta:
    fields = ('profile_id', 'timestamp', 'currency_id', 'amount', 'transaction_type_id')

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)


# Registering an Error Handler

@app.errorhandler(400)
def custom400(error):
  response = jsonify({'message': error.description})
  return response


# *********  API endpoint  *********** #


# create new user

@app.route('/api/v1/profile/', methods = ['POST'])
def create_new_user():
  name = request.json['name']
  tg_user_id = request.json['tg_user_id']
  data_check = Validation(name, tg_user_id)
  if data_check.tg_user_id_validate() == None and data_check.name_validate() == None:
    new_user = UserProfile(tg_user_id)
    new_user.create(name)
    new_balance = Wallet(tg_user_id)
    new_balance.hello_user_balance()
  new_user_profile = profile_schema.dump(session.query(Profile).filter_by(tg_user_id = tg_user_id).one())
  return jsonify(new_user_profile)


# user profile info

@app.route('/api/v1/profile/<tg_user_id>', methods = ['GET'])
def get_user_info(tg_user_id):
  user_information = UserProfile(tg_user_id).information_display()
  return jsonify(user_information)


# update user name

@app.route('/api/v1/profile/<tg_user_id>', methods = ['PUT'])
def update_name(tg_user_id):
  new_name = request.json['new_name']
  new_name_check = Validation(new_name, tg_user_id)
  if new_name_check.name_validate() == None:
    user = UserProfile(tg_user_id)
    user.update(new_name)
  update_profile = profile_schema.dump(session.query(Profile).filter_by(tg_user_id = tg_user_id).one())
  return jsonify(update_profile)


# delete user

@app.route('/api/v1/profile/<tg_user_id>', methods = ['DELETE'])
def delete_user(tg_user_id):
  name = request.json['name']
  # ????? \/
  if not session.query(Profile).filter_by(tg_user_id = tg_user_id, name = name).first():
  # ????? /\
    abort (404, description = f"User {tg_user_id} not found")
  else:
    shut_up_user = UserProfile(tg_user_id)
    shut_up_user.delete(name)
  return jsonify('user delete')


# currency price

@app.route('/api/v1/price/<ticker>', methods = ['GET'])
def get_price_value(ticker):
  price_information = CurrencyInfo(ticker).get_price_value()
  return jsonify(price_information)


# user balance

@app.route('/api/v1/profile/<tg_user_id>/balance', methods = ['GET'])
def get_user_balances(tg_user_id):
  balance_info = Wallet(tg_user_id).user_balance()
  return jsonify(balance_info)


# user transaction

@app.route('/api/v1/transaction/<tg_user_id>', methods = ['GET'])
def get_user_transaction_list(tg_user_id):
  transactions = Wallet(tg_user_id).transaction_list()
  return jsonify(transactions)


# buy currency

@app.route('/api/v1/<tg_user_id>/buy/', methods = ['POST'])
def buy_currency(tg_user_id):
  ticker_buy = request.json['ticker_buy']
  ticker_sell = request.json['ticker_sell']
  amount_currency_buy = request.json['amount_currency_buy']
  Wallet(tg_user_id).buy(ticker_buy, ticker_sell, amount_currency_buy)
  return jsonify("Transaction successfully")


# sell currency

@app.route('/api/v1/<tg_user_id>/sell/', methods = ['POST'])
def sell_currency(tg_user_id):
  ticker_sell = request.json['ticker_sell']
  ticker_buy = request.json['ticker_buy']
  amount_currency_sell = request.json['amount_currency_sell']
  Wallet(tg_user_id).sell(ticker_sell, ticker_buy, amount_currency_sell)
  return jsonify('Transaction successfully')


# class for name and telegramm id checking methods

class Validation():
  def __init__(self, name, tg_user_id):
    self.name = name
    self.tg_user_id = tg_user_id

  def tg_user_id_validate(self):
    if len(self.tg_user_id) > 50 or re.fullmatch('@[A-Za-z][A-Za-z0-9]{1,50}$', self.tg_user_id) == None:
      abort (409, description = f"{self.tg_user_id} is invalid telegram id")
    if not session.query(Profile).filter_by(tg_user_id = self.tg_user_id).first():
      return None
    else:
      abort(409, description = f"Can not be empty. {self.tg_user_id} alredy exist.")

  def name_validate(self):
    if not re.fullmatch ('[A-Za-z][A-Za-z0-9_]{2,32}$', self.name):
      abort(409, description = "Invalid name format")
    if not session.query(Profile).filter_by(name = self.name).first():
      return None
    else:
      abort(409, description = f"Name can not be empty. {self.name} alredy exist.")


# class for user's methods

class UserProfile():
  def __init__(self, tg_user_id):
    self.tg_user_id = tg_user_id

  def create(self, name):
    new_profile = Profile(name, self.tg_user_id)
    session.add(new_profile)
    session.commit()
    return None

  def information_display(self):
    user_info = session.query(Profile).filter_by(tg_user_id = self.tg_user_id).first()
    if not user_info:
      abort(404, description = f"{self.tg_user_id} not found")
    user_info_result = profile_schema.dump(user_info)
    return user_info_result

  def update(self, new_name):
    profile_name = session.query(Profile).filter_by(tg_user_id = self.tg_user_id).one()
    profile_name.name = new_name
    session.add(profile_name)
    session.commit()
    return None

  def delete(self, name):
    user_for_delete = session.query(Profile).filter_by(tg_user_id = self.tg_user_id, name = name).first()
    session.delete(user_for_delete)
    session.commit()
    return None


# class for methods with currency

class CurrencyInfo():
  def __init__(self, ticker):
    self.ticker = ticker

  def get_price_value(self):
    currency_price = currency_prices[self.ticker]
    return currency_price


# class for user's wallet methods

class Wallet():
  def __init__(self, tg_user_id):
    self.tg_user_id = tg_user_id
  
  def user_balance(self):
    user_profile_id = session.query(Profile).filter_by(tg_user_id = self.tg_user_id).first()
    if not user_profile_id:
      abort (404, description = f"User {self.tg_user_id} not found")
    user_balance = session.query(Balance).filter_by(profile_id = user_profile_id.id).all()
    if not user_balance:
      return 'You do not have the means in wallet'
    else:
      user_balance_result = balances_schema.dump(user_balance)
      return user_balance_result

  def hello_user_balance(self):
    user_profile_id = session.query(Profile).filter_by(tg_user_id = self.tg_user_id).first()
    if not user_profile_id:
      abort (404, description = f"User {self.tg_user_id} not found")
    hello_usdt_bonus = 10000.0
    # user uuid
    # uuid - the value of the field 'id' that is automatically assigned to the user at the time of registration. 
    # For convenience, in all functions, we make the value of the uuid field equal to the variable 'profile_id' or id
    profile_id = (session.query(Profile).filter_by(tg_user_id = self.tg_user_id).one()).id
    # new user hello bonus = 10000.0 USDT
    hello_usdt_bonus_top_up = Balance(profile_id, (session.query(Currency).filter_by(name = 'USDT').one()).id, hello_usdt_bonus)
    session.add(hello_usdt_bonus_top_up)
    hello_transaction_log = Transaction(profile_id, dt, (session.query(Currency).filter_by(name = 'USDT').one()).id, hello_usdt_bonus,\
      (session.query(Transaction_type).filter_by(name = 'hello bonus').one()).id)
    session.add(hello_transaction_log)
    session.commit()

  def transaction_list(self):
    user_profile_id = session.query(Profile).filter_by(tg_user_id = self.tg_user_id).first()
    if not user_profile_id:
      abort (404, description = f"User {self.tg_user_id} not found")
    transaction_list = session.query(Transaction).filter_by(profile_id = user_profile_id.id).all()
    if not transaction_list:
      return 'No transactions available'
    result_list = transactions_schema.dump(transaction_list)
    return result_list

  def exchange_rate(ticker_sell, ticker_buy):
    return (Decimal(currency_prices[ticker_sell] / currency_prices[ticker_buy]))

  def swap(currency_sell_id, currency_buy_id, amount_currency_sell, ticker_sell, ticker_buy, profile_id):
    sell_on_balance = session.query(Balance).filter_by(profile_id = profile_id, currency_id = currency_sell_id).first()
    sell_on_balance.total -= Decimal(amount_currency_sell)
    sell_data_log = Transaction(profile_id, dt, currency_sell_id, amount_currency_sell,\
      (session.query(Transaction_type).filter_by(name = 'sell').one()).id)
    session.add(sell_data_log)
    buy_on_balance = session.query(Balance).filter_by(profile_id = profile_id, currency_id = currency_buy_id).first()
    buy_on_balance.total += Decimal(amount_currency_sell) * Wallet.exchange_rate(ticker_sell, ticker_buy)
    buy_data_log = Transaction(profile_id, dt, currency_buy_id, Decimal(amount_currency_sell) * Wallet.exchange_rate(ticker_sell, ticker_buy),\
      (session.query(Transaction_type).filter_by(name = 'buy').one()).id)
    session.add(buy_data_log)
    session.add(sell_on_balance, buy_on_balance)
    session.commit()

  def currency_sell_control(currency_sell_id, ticker_buy, ticker_sell, amount_currency_buy, profile_id):
    # availability control
    check_currency_sell = session.query(Balance).filter_by(profile_id = profile_id, currency_id = currency_sell_id).first()
    if not check_currency_sell:
      abort(404, description = f"You do not have {ticker_sell}")
    # amount control
    if check_currency_sell.total < Decimal(amount_currency_buy) / Wallet.exchange_rate(ticker_sell, ticker_buy):
      abort(404, description = "you do not have enough funds")

  def buy(self, ticker_buy, ticker_sell, amount_currency_buy):
    currency_buy_id = (session.query(Currency).filter_by(name = ticker_buy).one()).id
    currency_sell_id = (session.query(Currency).filter_by(name = ticker_sell).one()).id
    profile_id = (session.query(Profile).filter_by(tg_user_id = self.tg_user_id).one()).id
    Wallet.currency_sell_control(currency_sell_id, ticker_buy, ticker_sell, amount_currency_buy, profile_id)
    # if currency_sell_control - create new currency in user wallet
    currency_buy_in_wallet = session.query(Balance).filter_by(profile_id = profile_id, currency_id = currency_buy_id).first()
    if not currency_buy_in_wallet:
      new_currency_in_wallet = Balance(profile_id, currency_buy_id, 0.0)
      session.add(new_currency_in_wallet)
      session.commit()
    amount_currency_sell = Decimal(amount_currency_buy) / Wallet.exchange_rate(ticker_sell, ticker_buy)
    Wallet.swap(currency_sell_id, currency_buy_id, amount_currency_sell, ticker_sell, ticker_buy, profile_id)

  def sell(self, ticker_sell, ticker_buy, amount_currency_sell):
    # currency for which we sell - ticker_sell
    # currency for which we buy - ticker_buy.
    amount_currency_buy = Decimal(amount_currency_sell) * Wallet.exchange_rate(ticker_sell, ticker_buy)
    Wallet.buy(self, ticker_buy, ticker_sell, amount_currency_buy)

    


# API whithout classes

# # create new user

# @app.route('/api/v1/profile/', methods = ['POST'])
# def create_new_user():
#   name = request.json['name']
#   tg_user_id = request.json['tg_user_id']
#   hello_usdt_bonus = 10000.0
#   new_user = Profile(name, tg_user_id)
#   session.add(new_user)
#   session.commit()
#   # user uuid
#   uuid = (session.query(Profile).filter_by(name = name, tg_user_id = tg_user_id).one()).id
#   # uuid - the value of the field 'id' that is automatically assigned to the user at the time of registration. 
#   # For convenience, in all functions, we make the value of the uuid field equal to the variable 'profile_id'
#   profile_id = uuid
#   # new user hello bonus = 10000.0 USDT
#   hello_usdt_bonus_top_up = Balance(profile_id, (session.query(Currency).filter_by(name = 'USDT').one()).id, hello_usdt_bonus)
#   session.add(hello_usdt_bonus_top_up)
#   hello_transaction_log = Transaction(profile_id, dt, (session.query(Currency).filter_by(name = 'USDT').one()).id, hello_usdt_bonus,\
#     (session.query(Transaction_type).filter_by(name = 'hello bonus').one()).id)
#   session.add(hello_transaction_log)
#   session.commit()
#   new_user_profile = profile_schema.dump(session.query(Profile).filter_by(id = profile_id).one())
#   return jsonify(new_user_profile)


# # update user name

# @app.route('/api/v1/profile/<profile_id>', methods = ['PUT'])
# def update_user_name(profile_id):
#   name = request.json['name']
#   user_name = session.query(Profile).filter_by(id = profile_id).one()
#   user_name.name = name
#   session.add(user_name)
#   session.commit()
#   new_user_name = profile_schema.dump(user_name)
#   return jsonify(new_user_name)


# # user profile data 

# @app.route('/api/v1/profile/<profile_id>', methods = ['GET'])
# def get_user_data(profile_id):
#   profile_data = session.query(Profile).filter_by(id = profile_id).one()
#   profile_data_result = profile_schema.dump(profile_data)
#   return jsonify(profile_data_result)


# # user balance

# @app.route('/api/v1/profile/<profile_id>/balance', methods = ['GET'])
# def get_user_balances(profile_id):
#   user_balance = session.query(Balance).filter_by(profile_id = profile_id).all()
#   user_balance_result = balances_schema.dump(user_balance)
#   return jsonify(user_balance_result)


# # currency price

# @app.route('/api/v1/price/<ticker>', methods = ['GET'])
# def get_price_value(ticker):
#   currency_price = currency_prices[ticker]
#   return jsonify(currency_price)


# method for buy/sell endpoint

# def exchange_rate(ticker_sell, ticker_buy):
#   return (Decimal(currency_prices[ticker_sell] / currency_prices[ticker_buy]))


# def swap(currency_sell_id, currency_buy_id, amount_currency_sell, profile_id, ticker_sell, ticker_buy):
#   sell_on_balance = session.query(Balance).filter(Balance.profile_id == profile_id, Balance.currency_id == currency_sell_id).first()
#   sell_on_balance.total -= Decimal(amount_currency_sell)
#   sell_data_log = Transaction(profile_id, dt, currency_sell_id, amount_currency_sell,\
#     (session.query(Transaction_type).filter(Transaction_type.name == 'sell').one()).id)
#   session.add(sell_data_log)
#   buy_on_balance = session.query(Balance).filter(Balance.profile_id == profile_id, Balance.currency_id == currency_buy_id).first()
#   buy_on_balance.total += Decimal(amount_currency_sell) * exchange_rate(ticker_sell, ticker_buy)
#   buy_data_log = Transaction(profile_id, dt, currency_buy_id, Decimal(amount_currency_sell) * exchange_rate(ticker_sell, ticker_buy),\
#     (session.query(Transaction_type).filter(Transaction_type.name == 'buy').one()).id)
#   session.add(buy_data_log)
#   session.add(sell_on_balance, buy_on_balance)
#   session.commit()


# def currency_sell_control(currency_sell_id, ticker_buy, ticker_sell, amount_currency_buy, profile_id):
#   # availability control
#   check_currency_sell = session.query(Balance).filter(Balance.profile_id == profile_id, Balance.currency_id == currency_sell_id).first()
#   if not check_currency_sell:
#     #abort(404, description = f"You don't have {ticker_sell}")
#     raise Exception (f"You don't have {ticker_sell}")
#   # amount control
#   if check_currency_sell.total < Decimal(amount_currency_buy) / exchange_rate(ticker_sell, ticker_buy):
#     raise Exception ("you do not have enough funds")


# def buy(ticker_buy, ticker_sell, amount_currency_buy, profile_id):
#   currency_buy_id = (session.query(Currency).filter_by(name = ticker_buy).one()).id
#   currency_sell_id = (session.query(Currency).filter_by(name = ticker_sell).one()).id
#   currency_sell_control(currency_sell_id, ticker_buy, ticker_sell, amount_currency_buy, profile_id)
#   # if currency_sell_control - create new currency in user wallet
#   currency_buy_in_wallet = session.query(Balance).filter(Balance.profile_id == profile_id, Balance.currency_id == currency_buy_id).first()
#   if not currency_buy_in_wallet:
#     new_currency_in_wallet = Balance(profile_id, currency_buy_id, 0.0)
#     session.add(new_currency_in_wallet)
#     session.commit()
#   amount_currency_sell = Decimal(amount_currency_buy) / exchange_rate(ticker_sell, ticker_buy)
#   swap(currency_sell_id, currency_buy_id, amount_currency_sell, profile_id, ticker_sell, ticker_buy)


# def sell(ticker_sell, ticker_buy, amount_currency_sell, profile_id):
#   # currency for which we sell - ticker_sell
#   # currency for which we buy - ticker_buy.
#   amount_currency_buy = Decimal(amount_currency_sell) * exchange_rate(ticker_sell, ticker_buy)
#   buy(ticker_buy, ticker_sell, amount_currency_buy, profile_id)


# # currency buy

# @app.route('/api/v1/<profile_id>/buy/', methods = ['POST'])
# def buy_currency(profile_id):
#   ticker_buy = request.json['ticker_buy']
#   ticker_sell = request.json['ticker_sell']
#   amount_currency_buy = request.json['amount_currency_buy']
#   buy(ticker_buy, ticker_sell, amount_currency_buy, profile_id)
#   return jsonify('Transaction successfully')


# # currency sell

# @app.route('/api/v1/<profile_id>/sell/', methods = ['POST'])
# def currency_sell(profile_id):
#   ticker_sell = request.json['ticker_sell']
#   ticker_buy = request.json['ticker_buy']
#   amount_currency_sell = request.json['amount_currency_sell']
#   sell(ticker_sell, ticker_buy, amount_currency_sell, profile_id)
#   return jsonify('Transaction successfully')


# # user transaction list

# @app.route('/api/v1/transaction/<profile_id>', methods = ['GET'])
# def get_user_transaction_list(id):
#   transaction_list = session.query(Transaction).filter_by(profile_id = id).all()
#   result_list = transactions_schema.dump(transaction_list)
#   return jsonify(result_list)


# # delete user

# @app.route('/api/v1/profile/<profile_id>', methods = ['DELETE'])
# def user_delete(profile_id):
#   user_for_delete = session.query(Profile).filter_by(id = profile_id).one()
#   session.delete(user_for_delete)
#   session.commit()
#   return jsonify('user delete')


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
