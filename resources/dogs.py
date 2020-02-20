# this file is like dogcongtroller.js
import models

from flask import Blueprint, request, jsonify
# request -- data from client's request is sent to the global request object
# we can use this object to get the json or form data or whatever
# reassigned on every request that has a body

# this is some useful extra tools that come with peewee
from playhouse.shortcuts import model_to_dict

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

	# us our peewee model to add something to database
	dog = models.Dog.create(name=payload['name'], owner=payload['owner'], breed=payload['breed'])

	print(dog) # just prints the ID -- check in sqlite3 on the command line
			   # run sqlite3 dogs.sqlite to open a CLI that lets you enter the SQL queries

	print(dog.__dict__) # this sometimes shows you more useful info
						# .__dict__ is a class attribute automatically added to python classes

	print(dir(dog)) # look at all the pretty methods!!!

	# notice you can't directly jsonify dog since it's not a dictionary or other jsonifiable thing
	# it causes TypeError: Object of type 'Dog' is not JSON serializable

	# we can use model_to_dict from playhouse to convert the model to a dict

	dog_dict=model_to_dict(dog)

	# notice you can add 201 to the return and you will send a proper HTTP status cod
	return jsonify(data=dog_dict, status={'message': 'Successfully created dog!'}), 201