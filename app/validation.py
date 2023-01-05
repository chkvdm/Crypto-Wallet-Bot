import re
from flask import abort
from jsonschema import validate
from .models import session
from .models import Profile
from .errors import *


# methods for validation a name and telegramm ID

class Validation():
  def __init__(self):
    self = self

  def user_schema_check(self, req):
    # validation JSON in the request
    if req.get_json(silent = True) == None:
      abort (400, description = "data not entered or incorrect")
    schema = {
      "type" : "object",
      "properties" : {
        "name": {"type" : "string"},
        "tg_user_id": {"type" : "number"}
      }
    }
    try: 
      validate(instance=req.json, schema=schema)
      return None
    except:
      abort(400, description = "wrong name or telegram ID")

  def trading_schema_check(self, req):
    # validation JSON in the request
    if req.get_json(silent = True) == None:
      abort (400, description = "data not entered or incorrect")
    schema = {
      "type" : "object",
      "properties" : {
        "ticker_buy": {"type": "string"},
        "ticker_sell": {"type": "string"},
        "amount_currency_buy": {"type": "number"}
      }
    }
    try: 
      validate(instance=req.json, schema=schema)
      return None
    except:
      abort(400, description = "wrong ticker or amount")

  def tg_user_id_validate(self, tg_user_id):
    # validation telegram ID format
    if re.fullmatch('[0-9]{4,32}', str(tg_user_id)) == None:
      abort (400, description = f"invalid telegram ID")
    # validation of availability a telegram ID 
    if not session.query(Profile).filter_by(tg_user_id = str(tg_user_id)).first():
      return None
    else:
      abort(403, description = f"The telegram ID '{tg_user_id}' is alredy exist.")

  def name_validate(self, name):
    # validation name format
    if re.fullmatch ('[a-z0-9_]{4,32}$', name) == None:
      abort(400, description = "invalid name format.")
    # validation of availability a name 
    if not session.query(Profile).filter_by(name = name).first():
      return None
    else:
      abort(403, description = f"The name '{name}' alredy exist.")