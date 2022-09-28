import requests

def currency_price(currency):
    service_url = 'https://api.coincap.io/v2/assets/'
    url = service_url + currency
    response = requests.get(url)
    js = response.json()
    return (js['data']['priceUsd'])

btc_cost = currency_price('bitcoin')
eth_cost = currency_price('ethereum')
bnb_cost = currency_price('binance-coin')
sol_cost = currency_price('solana')
doge_cost = currency_price('dogecoin')

currency_prices = {
  'USD' : 1,
  'BTC' : float(btc_cost), 
  'ETH' : float(eth_cost), 
  'BNB' : float(bnb_cost), 
  'SOL' : float(sol_cost), 
  'DOGE' : float(doge_cost)
  }

for key, val in currency_prices.items():
  print (key, (': {}$').format(val))

class user(object):
  def __init__(self, name):
    self.name = name
    self.balance = {
      'USD' : 10000.0, 
      'BTC' : 0, 
      'ETH' : 0, 
      'BNB' : 0, 
      'SOL' : 0, 
      'DOGE' : 0
      }
  
  def __repr__(self):
    return (('Welcome {}!\nYou balance: {},').format(self.name, self.balance))
  
  def get_balance(self):
    return self.balance

  def exchange_rate(self, currency_sell, currency_buy):
    return (float(currency_prices[currency_sell] / currency_prices[currency_buy]))

  def swap(self, currency_sell, currency_buy, amount_currency_sell):
    if amount_currency_sell > self.balance[currency_sell]:
      raise Exception ("You don't have enough funds")
    self.balance[currency_sell] -= amount_currency_sell
    self.balance[currency_sell] = round((self.balance[currency_sell]), 8)
    self.balance[currency_buy] += amount_currency_sell * user.exchange_rate(self, currency_sell, currency_buy)
    self.balance[currency_buy] = round((self.balance[currency_buy]), 8)

  def buy(self, currency_buy, currency_sell, amount_currency_buy):
    amount_currency_sell = amount_currency_buy / user.exchange_rate(self, currency_sell, currency_buy)
    user.swap(self, currency_sell, currency_buy, amount_currency_sell)

  def sell(self, currency_sell, currency_buy, amount_currency_sell):
    user.swap(self, currency_sell, currency_buy, amount_currency_sell)

vadim = user('Vadim')