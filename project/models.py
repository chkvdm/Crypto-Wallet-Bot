from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import mapper, sessionmaker



# connection on CryptoBotDB

engine = create_engine('postgresql+psycopg2://postgres:@localhost/CryptoBotDB')
meta = MetaData(engine)



# import table from CryptoBotDB

profile = Table('profile', meta, autoload=True) 
currency = Table('currency', meta, autoload=True) 
transaction_type = Table('transaction_type', meta, autoload=True) 
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

class Transaction_type():
  def __init__(self, name):
    self.name = name

class Balance():
  def __init__(self, profile_id, currency_id, total):
    self.profile_id = profile_id
    self.currency_id = currency_id
    self.total = total

class Transaction():
  def __init__(self, profile_id, timestamp, currency_id, amount, trasaction_type_id):
    self.profile_id = profile_id
    self.timestamp = timestamp
    self.currency_id = currency_id
    self.amount = amount
    self.transaction_type_id = trasaction_type_id



mapper(Profile, profile)
mapper(Currency, currency)
mapper(Transaction_type, transaction_type)
mapper(Balance, balance)
mapper(Transaction, transaction)


# create session

DBSession = sessionmaker(bind=engine)
session = DBSession()