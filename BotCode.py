import random
btc_cost = random.uniform(5000, 60000)
print ("BTC cost: {}".format(str(round(btc_cost, 8))))

class user(object):
  def __init__(self, name):
    self.name = name
    self.balance = {"USD" : 10000, "BTC": 0}
  
  def __repr__(self):
    return ("welcome {}, you balance: {}").format(self.name, self.balance)
  
  def get_balance(self):
    return self.balance
  
  def buy(self):
    start = True
    while start:
      try:
        amount_btc = (float(input("Enter BTC amount you want buy: ")))
        if (amount_btc * btc_cost) > self.balance["USD"]:
          try_again = (input("There are not enough funds in your account. Enter Y fo continue, enter N for exit: "))
          try_again = try_again.upper()
          if try_again == "Y":
            continue
          else:
            break
        else:
          self.balance["BTC"] += amount_btc
          self.balance["BTC"] = round(self.balance["BTC"], 8)
          self.balance["USD"] -= btc_cost * amount_btc
          self.balance["USD"] = round(self.balance["USD"], 8)
          return self.balance
      except Exception:
        print ('Incorrect input. Please, enter a valid value.')
  
  def sell(self):
    start = True
    while start:
      try:
        amount_btc = (float(input("Enter BTC amount you want sell: ")))
        if (amount_btc) > self.balance["BTC"]:
          try_again = (input("There are not enough funds in your account. Enter Y fo continue, enter N for exit: "))
          try_again = try_again.upper()
          if try_again == "Y":
            continue
          else:
            break
        else:
          self.balance["BTC"] -= amount_btc
          self.balance["BTC"] = round(self.balance["BTC"], 8)
          self.balance["USD"] += btc_cost * amount_btc
          self.balance["USD"] = round(self.balance["USD"], 8)
          return self.balance
      except Exception:
        print ('Incorrect input. Please, enter a valid value.')
  
vadim = user("Vadim")
print (vadim)
vadim.buy()
print (vadim.get_balance())
vadim.sell()
print (vadim.get_balance())