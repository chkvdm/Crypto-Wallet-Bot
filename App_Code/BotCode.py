import requests
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, and_
from sqlalchemy.orm import mapper, relationship, sessionmaker
from decimal import Decimal
from datetime import datetime, timezone



dt = datetime.now()
dt = dt.replace(tzinfo=timezone.utc)



## API request for currency price

#def currency_price(currency):
    #service_url = 'https://api.coincap.io/v2/assets/'
    #url = service_url + currency
    #response = requests.get(url)
    #js = response.json()
    #return (js['data']['priceUsd'])

#btc_cost = currency_price('bitcoin')
#eth_cost = currency_price('ethereum')
#bnb_cost = currency_price('binance-coin')
#sol_cost = currency_price('solana')
#doge_cost = currency_price('dogecoin')

#currency_prices = {
  #'USD' : 1,
  #'BTC' : float(btc_cost), 
  #'ETH' : float(eth_cost), 
  #'BNB' : float(bnb_cost), 
  #'SOL' : float(sol_cost), 
  #'DOGE' : float(doge_cost)
  #}



#currency_prices for testing
currency_prices = {
  1 : 1, # USDT
  2 : 18828.0, # BTC
  3 : 1356.0, # ETH
  4 : 237.2, # BNB
  5 : 65.0, # SOL
  6 : 0.05 # DOGE
  }



#for key, val in currency_prices.items():
  #print (key, (': {}$').format(val))



# connection on CryptoBotDB

engine = create_engine('postgresql+psycopg2://postgres:@localhost/CryptoBotDB')
meta = MetaData(engine)



# import table from CryptoBotDB

profile = Table('profile', meta, autoload=True) 
currency = Table('currency', meta, autoload=True) 
transaction_name = Table('transaction_name', meta, autoload=True) 
balance = Table('balance', meta, autoload=True) 
transaction = Table('transaction', meta, autoload=True) 



# relating tables to classes

class Profile():
  def __init__(self, name, tg_user_id):
    self.name = name
    self.tg_user_id = tg_user_id

class Currency():
  def __init__(self, name):
    self.name = name

class Transaction_name():
  def __init__(self, name):
    self.name = name

class Balance():
  def __init__(self, profile_id, currency_id, total):
    self.profile_id = profile_id
    self.currency_id = currency_id
    self.total = total

class Transaction():
  def __init__(self, profile_id, timestamp, currency_id, amount, trasaction_name):
    self.profile_id = profile_id
    self.timestamp = timestamp
    self.currency_id = currency_id
    self.amount = amount
    self.transaction_name = trasaction_name

mapper(Profile, profile)
mapper(Currency, currency)
mapper(Transaction_name, transaction_name)
mapper(Balance, balance)
mapper(Transaction, transaction)

DBSession = sessionmaker(bind=engine)
session = DBSession()



class User():

  def __init__(self, name, tg_user_id):
    self.name = name
    self.tg_user_id = tg_user_id
    profile_check = session.query(Profile).filter_by(name = name, tg_user_id = tg_user_id).first()
    if not profile_check:
      new_profile = Profile(name, tg_user_id)
      session.add(new_profile)
      session.commit()
      uuid = (session.query(Profile).filter_by(name = name, tg_user_id = tg_user_id).first()).id
      session.add_all([
        Balance(uuid, 1, 10000.0),
        Balance(uuid, 2, 0.0),
        Balance(uuid, 3, 0.0),
        Balance(uuid, 4, 0.0),
        Balance(uuid, 5, 0.0),
        Balance(uuid, 6, 0.0)
      ])
      session.commit()
    uuid = (session.query(Profile).filter_by(name = name, tg_user_id = tg_user_id).first()).id
    self.uuid = uuid
    
  #def __repr__(self):
    #return (('Welcome {}!\nYou balance: {},').format(self.name, self.balance))
  
  def get_balance(self):
    wallet = []
    for row in session.query(Balance).filter(Balance.profile_id == self.uuid):
      wallet.append(row)
    return wallet

  def exchange_rate(self, currency_sell, currency_buy):
    return (Decimal(currency_prices[currency_sell] / currency_prices[currency_buy]))

  def swap(self, currency_sell, currency_buy, amount_currency_sell):
    sell_on_balance = session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_sell).first()
    if amount_currency_sell > sell_on_balance.total:
      raise Exception ("You don't have enough funds")

    sell_on_balance.total -= Decimal(amount_currency_sell)
    #sell_data_log = Transaction(self.uuid, dt.isoformat(), currency_sell, amount_currency_sell, 2)
    #session.add(sell_data_log)
    #session.commit()

    buy_on_balance = session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_buy).first()
    buy_on_balance.total += Decimal(amount_currency_sell) * User.exchange_rate(self, currency_sell, currency_buy)
    #buy_data_log = Transaction(self.uuid, dt.isoformat(), currency_buy, Decimal(amount_currency_sell) * User.exchange_rate(self, currency_sell, currency_buy), 1)
    #session.add(buy_data_log)
    #session.commit()

    session.add(sell_on_balance, buy_on_balance)
    session.commit()

  def buy(self, currency_buy, currency_sell, amount_currency_buy):
    amount_currency_sell = Decimal(amount_currency_buy) / User.exchange_rate(self, currency_sell, currency_buy)
    User.swap(self, currency_sell, currency_buy, amount_currency_sell)

  def sell(self, currency_sell, currency_buy, amount_currency_sell):
    User.swap(self, currency_sell, currency_buy, amount_currency_sell)


