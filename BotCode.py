import random

btc_cost = random.uniform(5000, 60000)
eth_cost = random.uniform(800, 5000)
bnb_cost = random.uniform(100, 1000)
sol_cost = random.uniform(10, 600)
doge_cost = random.uniform(0.03, 2)

currency_prices = {
  'BTC' : btc_cost, 
  'ETH' : eth_cost, 
  'BNB' : bnb_cost, 
  'SOL': sol_cost, 
  'DOGE': doge_cost
  }

for key, val in currency_prices.items():
  print (key, ': {}$'.format(str(round(val, 8))))



class user(object):
  def __init__(self, name):
    self.name = name
    self.balance = {"USD" : 10000}
  
  def __repr__(self):
    return (('Welcome {}!\nYou balance: {},').format(self.name, self.balance))
  
  def get_balance(self):
    return ('You balance {}'.format(self.balance))
  
  def buy(self):
    start = True
    while start:
      try:
        currency_type = (input("What currency do you want to buy: "))
        currency_type = currency_type.upper()
        if currency_type in currency_prices.keys():
          key = currency_type
          val = currency_prices[key]
          amount_currency = (float(input("Amount of currency: ")))
          if (amount_currency * val) <= self.balance['USD']:
            self.balance[key] = self.balance.get(key, 0) + amount_currency
            self.balance[key] = round(self.balance[key], 8)
            self.balance['USD'] -= amount_currency * val
            self.balance["USD"] = round(self.balance["USD"], 8)
          elif (amount_currency * val) > self.balance['USD']:
            try_again = (input("You don't have enough funds. Enter Y fo continue or press return for exit: "))
            try_again = try_again.upper()
            if try_again == "Y":
              continue
            else:
              return self.balance
          cnt = (input("Operation successful! You balance {}. Do you want to continue shopping? Enter Y fo continue or press return for exit: ".format(self.balance)))
          cnt = cnt.upper()
          if cnt == 'Y':
            continue
          else:
            return self.balance
        else:
          print ('Error! Select a currency from the list above.')
      except Exception:
        print ('Incorrect input. Please, enter a valid value.')
  
  def sell(self):
    start = True
    while start:
      try:
        currency_type = (input("What currency do you want to sell: "))
        currency_type = currency_type.upper()
        if currency_type in self.balance.keys():
          key = currency_type
          val = currency_prices[key]
          amount_currency = (float(input("Amount of currency: ")))
          if (amount_currency) <= self.balance[key]:
            self.balance[key] -= amount_currency
            self.balance[key] = round(self.balance[key], 8)
            self.balance['USD'] += amount_currency * val
            self.balance["USD"] = round(self.balance["USD"], 8)
          elif (amount_currency) > self.balance[key]:
            try_again = (input("You don't have enough funds. Enter Y fo continue or press return for exit: "))
            try_again = try_again.upper()
            if try_again == "Y":
              continue
            else:
              return self.balance
          cnt = (input("Operation successful! You balance {}. Do you want to continue selling? Enter Y fo continue or press return for exit: ".format(self.balance)))
          cnt = cnt.upper()
          if cnt == 'Y':
            continue
          else:
            return self.balance
        else:
          print ("You havn't {}. Please choice currency from you balance.".format(currency_type))
      except Exception:
        print ('Incorrect input. Please, enter a valid value.')
  

  