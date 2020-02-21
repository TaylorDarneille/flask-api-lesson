# this file is like dogcongtroller.js
import models

from flask import Blueprint, request, jsonify
# request -- data from client's request is sent to the global request object
# we can use this object to get the json or form data or whatever
# reassigned on every request that has a body

# this is some useful extra tools that come with peewee
from playhouse.shortcuts import model_to_dict

# blueprint is a way to modularize apps, and group related functinoality
# https://flask.pallersprojects.com/en/1.1.x/tutorial/views/
# we are using blueprints to make something analogous to a controller
# first arg is the blueprint's name
# second arg is its import_name
dogs = Blueprint('dogs', 'dogs')

@dogs.route('/', methods=['GET'])
def dogs_index():
	"""get all the dogs from the database as JSON"""
	all_dogs_query = models.Dog.select()
	# What is this thing we get back?
	# print("")
	# print("building dogs index")
	# print(all_dogs_query) # looks like sequel
	# print(all_dogs_query[0]) # appears to be a dog
	# print(type(all_dogs_query)) # http://docs.peewee-orm.com/en/latest/peewee/api.html#ModelSelect
	# print(all_dogs_query.__dict__) # looks like a query
	# print (model_to_dict(all_dogs_query[0])) # definitely a dog!
	
	# we need a list of dictionaries ...
	# list_of_dog_dicts = []
	# for item in all_dogs_query:
	# 	print("")
	# 	print(item) # id?
	# 	print(model_to_dict(item))
	# 	list_of_dog_dicts.append(model_to_dict(item))
	

	# the above work can be also done using list comprehension
	dog_dicts = [model_to_dict(d) for d in all_dogs_query]

	return jsonify(
		data=dog_dicts,
		message=f"Successfully retrieved {len(dog_dicts)} dogs",
		status=200
	), 200



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

# dog destroy route
@dogs.route('/<id>', methods=['Delete'])
def delete_dog(id):
	# you are trying to delete dog with the following id
	delete_query = models.Dog.delete().where(models.Dog.id==id)
	delete_query.execute() # you need this for delete and upate
	return jsonify(
		data = {},
		message="Successfully deleted dog with id {}".format(id),
		status=200
	), 200

# dogs UPDATE route
@dogs.route('/<id>', methods=['PUT'])
def updateDog(id):
	payload = request.get_json()
	update_query = models.Dog.update(
		name=payload['name'],
		breed=payload['breed'],
		owner=payload['owner']
	).where(models.Dog.id==id)
	# fun bonus see if you can write this shorter using the unpack operator:
	# https://codeyarns.github.io/tech/2012-04-25-upack-operator-in-python.html
	# the above query could be written like this
	update_query.execute()

	# to include the updated data (for the benefit of the front end developers), the way we have it written, we'd need to do another query
	updated_dog = models.Dog.get_by_id(id)

	return jsonify(
		data=model_to_dict(updated_dog),
		message="Successfully udpated dog with id {}".format(id),
		status=200
	), 200



