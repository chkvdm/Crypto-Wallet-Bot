from flask import jsonify

from app import app


# registering an error handlers

@app.errorhandler(400)
def error_json_custom(error):
  response = jsonify({'message': error.description}), 400
  return response

@app.errorhandler(403)
def error_json_custom(error):
  response = jsonify({'message': error.description}), 403
  return response

@app.errorhandler(404)
def error_json_custom(error):
  response = jsonify({'message': error.description}), 404
  return response

@app.errorhandler(405)
def error_json_custom(error):
  response = jsonify({'message': error.description}), 405
  return response

@app.errorhandler(409)
def error_json_custom(error):
  response = jsonify({'message': error.description}), 409
  return response

@app.errorhandler(500)
def error_json_custom(error):
  response = jsonify({'message': error.description}), 500
  return response
