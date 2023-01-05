from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import mapper, sessionmaker
from flask_marshmallow import Marshmallow
from app import app


# connection SQLalchemy on CryptoBotDB

engine = create_engine('postgresql+psycopg2://postgres:example@127.0.0.1:5433/CryptoBotDB')
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
  def __init__(self, profile_id, timestamp, currency_id, amount, transaction_type_id):
    self.profile_id = profile_id
    self.timestamp = timestamp
    self.currency_id = currency_id
    self.amount = amount
    self.transaction_type_id = transaction_type_id


mapper(Profile, profile)
mapper(Currency, currency)
mapper(Transaction_type, transaction_type)
mapper(Balance, balance)
mapper(Transaction, transaction)


# create session

DBSession = sessionmaker(bind=engine)
session = DBSession()


ma = Marshmallow(app)


# create Marshmallow model from data base table

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
