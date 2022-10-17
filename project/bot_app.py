import requests
from decimal import Decimal
from datetime import datetime
from models import Profile, Balance, Transaction
from models import session 


dt = datetime.now()
dt = dt.isoformat()



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
      start_balance = Balance(uuid, 1, 10000.0)
      session.add(start_balance)
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
    sell_data_log = Transaction(self.uuid, dt, currency_sell, amount_currency_sell, 2)
    session.add(sell_data_log)
    session.commit()

    buy_on_balance = session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_buy).first()
    buy_on_balance.total += Decimal(amount_currency_sell) * User.exchange_rate(self, currency_sell, currency_buy)
    buy_data_log = Transaction(self.uuid, dt, currency_buy, Decimal(amount_currency_sell) * User.exchange_rate(self, currency_sell, currency_buy), 1)
    session.add(buy_data_log)
    session.commit()
    session.add(sell_on_balance, buy_on_balance)
    session.commit()

  def buy(self, currency_buy, currency_sell, amount_currency_buy):
    check_currency_sell =  session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_sell).first()
    if not check_currency_sell:
      raise Exception ("you don't have the currency for which you want to buy")
    currency_buy_in_wallet = session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_buy).first()
    if not currency_buy_in_wallet:
      new_currency_in_wallet = Balance(self.uuid, currency_buy, 0.0)
      session.add(new_currency_in_wallet)
      session.commit()
    amount_currency_sell = Decimal(amount_currency_buy) / User.exchange_rate(self, currency_sell, currency_buy)
    User.swap(self, currency_sell, currency_buy, amount_currency_sell)

  def sell(self, currency_sell, currency_buy, amount_currency_sell):
    check_currency_sell =  session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_sell).first()
    if not check_currency_sell:
      raise Exception ("you don't have the currency for sell")
    currency_buy_in_wallet = session.query(Balance).filter(Balance.profile_id == self.uuid, Balance.currency_id == currency_buy).first()
    if not currency_buy_in_wallet:
      new_currency_in_wallet = Balance(self.uuid, currency_buy, 0.0)
      session.add(new_currency_in_wallet)
      session.commit()
    User.swap(self, currency_sell, currency_buy, amount_currency_sell)
