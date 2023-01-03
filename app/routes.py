from app import app
from .static import Validation, UserProfile, CurrencyInfo, Wallet
from flask import request, jsonify


# create profile

@app.route('/v1/profile', methods = ['POST'])
def create_new_user():
  Validation().user_schema_check(request)
  new_user_profile = UserProfile().create(request.json)
  return jsonify(new_user_profile), 201

# user profile info

@app.route('/v1/profile/<tg_user_id>', methods = ['GET'])
def get_user_info(tg_user_id):
  user_information = UserProfile().get_information(tg_user_id)
  return jsonify(user_information)

# update user name

@app.route('/v1/profile/<tg_user_id>', methods = ['PUT'])
def rename(tg_user_id):
  Validation().user_schema_check(request)
  update_user_information = UserProfile().update(request.json, tg_user_id)
  return jsonify(update_user_information)

# delete user

@app.route('/v1/profile/<tg_user_id>', methods = ['DELETE'])
def delete_user(tg_user_id):
  UserProfile().delete(tg_user_id)
  return jsonify({"message": "user delete"})

# currency price

@app.route('/v1/currency/price/<ticker>', methods = ['GET'])
def get_price_value(ticker):
  price_information = CurrencyInfo().get_price_value(ticker)
  return jsonify(price_information)

# user balance

@app.route('/v1/profile/<tg_user_id>/balance', methods = ['GET'])
def get_user_balances(tg_user_id):
  balance_info = Wallet().user_balance(tg_user_id)
  return jsonify(balance_info)

# user transaction

@app.route('/v1/profile/<tg_user_id>/transactions', methods = ['GET'])
def get_user_transaction(tg_user_id):
  transactions = Wallet().user_transaction(tg_user_id)
  return jsonify(transactions)

# buy currency

@app.route('/v1/<tg_user_id>/buy', methods = ['POST'])
def buy_currency(tg_user_id):
  Validation().trading_schema_check(request)
  Wallet().buy(tg_user_id, request.json)
  return jsonify("Transaction successfully")

# sell currency

@app.route('/v1/<tg_user_id>/sell', methods = ['POST'])
def sell_currency(tg_user_id):
  Validation().trading_schema_check(request)
  Wallet().sell(tg_user_id, request.json)
  return jsonify('Transaction successfully')
