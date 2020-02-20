# this file is like dogcongtroller.js
import models

from flask import Blueprint, request
# request -- data from client's request is sent to the global request object
# we can use this object to get the json or form data or whatever
# reassigned on every request that has a body

# first arg is the blueprint's name
# second arg is its import_name
dogs = Blueprint('dogs', 'dogs')

@dogs.route('/', methods=['GET'])
def dogs_index():
	return "dogs resource working"

# dogs CREATE route
@ dogs.route('/', methods=['POST'])
def create_dog():
	# .get_json() attatched to request object will extract the JSON from the request body
	payload = request.get_json()
	print(payload)
	
	return "you hit dog create route"