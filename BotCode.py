import random

btc_cost = random.uniform(5000, 60000)
eth_cost = random.uniform(800, 5000)
bnb_cost = random.uniform(100, 1000)
sol_cost = random.uniform(10, 600)
doge_cost = random.uniform(0.03, 2)

currency_prices = {
  'USD' : 1,
  'BTC' : btc_cost, 
  'ETH' : eth_cost, 
  'BNB' : bnb_cost, 
  'SOL' : sol_cost, 
  'DOGE' : doge_cost
  }

for key, val in currency_prices.items():
  print (key, ': {}$'.format(str(round(val, 8))))



class user(object):
  def __init__(self, name):
    self.name = name
    self.balance = {
      'USD' : 10000, 
      'BTC' : 0, 
      'ETH' : 0, 
      'BNB' : 0, 
      'SOL' : 0, 
      'DOGE' : 0
      }
  
  def __repr__(self):
    return (('Welcome {}!\nYou balance: {},').format(self.name, self.balance))
  
  def get_balance(self):
    print ('You balance {}'.format(self.balance))

  def e_rate(self, currency_sell, currency_buy):
    exch = round(float(currency_prices[currency_sell] / currency_prices[currency_buy]), 8)
    return exch

  def swap(self, currency_sell, currency_buy, amount_currency_sell):
    if amount_currency_sell > self.balance[currency_sell]:
      raise Exception ("You don't have enough funds")
    self.balance[currency_buy] += self.balance[currency_sell] * user.e_rate(self, currency_sell, currency_buy)
    self.balance[currency_buy] = round((self.balance[currency_buy]), 8)
    self.balance[currency_sell] -= amount_currency_sell
    self.balance[currency_sell] = round((self.balance[currency_sell]), 8)
    user.get_balance(self)

  def buy(self, currency_sell, currency_buy, amount_currency_sell):
    user.swap(self, currency_sell, currency_buy, amount_currency_sell)

  def sell(self, currency_sell, currency_buy, amount_currency_sell):
    user.swap(self, currency_sell, currency_buy, amount_currency_sell)


vadim = user('Vadim')
vadim.buy('USD', 'ETH', 2000)
vadim.sell('ETH', 'USD', 1)