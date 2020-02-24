# this file is like dogcongtroller.js
import models

from flask import Blueprint, request, jsonify
# request -- data from client's request is sent to the global request object
# we can use this object to get the json or form data or whatever
# reassigned on every request that has a body

from flask_login import current_user, login_required

# this is some useful extra tools that come with peewee
from playhouse.shortcuts import model_to_dict

# blueprint is a way to modularize apps, and group related functinoality
# https://flask.pallersprojects.com/en/1.1.x/tutorial/views/
# we are using blueprints to make something analogous to a controller
# first arg is the blueprint's name
# second arg is its import_name
dogs = Blueprint('dogs', 'dogs')

@dogs.route('/', methods=['GET'])
@login_required # make this route unavailable to users who aren't logged in
def dogs_index():
	"""get all the dogs from the database as JSON"""
	all_dogs_query = models.Dog.select()
	"""get all the dogs from the db associated with the logged in user as JSON"""
	# the s work can be also done using list comprehension
	current_user_dog_dicts = [model_to_dict(d) for d in current_user.dogs]
	print(current_user_dog_dicts)

	return jsonify(
		data=current_user_dog_dicts,
		message=f"Successfully retrieved {len(current_user_dog_dicts)} dogs for {current_user.email}",
		status=200
	), 200

# dog show route
@dogs.route('/<id>/', methods=['GET'])
def get_one_dog(id):
	dog=models.Dog.get_by_id(id)
	#if user not logged in they just see name and breed
	if not current_user.is_authenticated:
		return jsonify(
			data={
				'name': dog.name,
				'breed': dog.breed
			},
			message="Registered users can access more info about this dog",
			status=200
		), 200
	# if they are logged in they see name, breed, adn owner info
	else:
		dog_dict=model_to_dict(dog)
		dog_dict.pop('created_at')

	return jsonify(
		data=dog_dict,
		message="Found dog with id {}".format(dog.id),
		status=200
	), 200

# dogs CREATE route
@ dogs.route('/', methods=['POST'])
@login_required
def create_dog():
	# .get_json() attatched to request object will extract the JSON from the request body
	payload = request.get_json()
	print(payload)
	# use our peewee model to add something to database
	dog = models.Dog.create(
		name=payload['name'],
		breed=payload['breed'], 
		owner=current_user.id
	)
	dog_dict=model_to_dict(dog)
	dog_dict['owner'].pop('password')
	# notice you can add 201 to the return and you will send a proper HTTP status cod
	return jsonify(data=dog_dict, status={'message': 'Successfully created dog!'}), 201

# dog destroy route
@dogs.route('/<id>/', methods=['Delete'])
@login_required
def delete_dog(id):
	
	# first, get the dog
	dog_to_delete = models.Dog.get_by_id(id)

	# if the owner matches
	if current_user.id == dog_to_delete.owner.id:
		# delete the dog
		# another way to delete stuff http://docs.peewee-orm.com/en/latest/peewee/querying.html#deleting-records
		dog_to_delete.delete_instance()

		return jsonify(
			data = {},
			message="Successfully deleted dog with id {}".format(id),
			status=200
		), 200

	else: 
		return jsonify(
			data = {'error': 'Forbidden'},
			message="Dog's owner_id does not match that of logged in user. User can only delete their own dog.",
			status=403
		), 403

# dogs UPDATE route
@dogs.route('/<id>/', methods=['PUT'])
@login_required # this shouldn't work at all if not logged in
def updateDog(id):
	payload = request.get_json()

	# # to include the updated data (for the benefit of the front end developers), the way we have it written, we'd need to do another query
	# updated_dog = models.Dog.get_by_id(id)

	#get the dog
	dog = models.Dog.get_by_id(id)

	# see if this dogs user is the logged in user -- if so
	if dog.owner.id == current_user.id:
		# update the fields that were included in the request body
		# you must include an else or you'll get an error
		dog.name=payload['name'] if 'name' in payload else None
		dog.breed=payload['breed'] if 'breed' in payload else None
		dog.save()
		# http://docs.peewee-orm.com/en/latest/peewee/querying.html#updating-existing-records
		dog_dict = model_to_dict(dog)

		return jsonify(
			data=dog_dict,
			message="Successfully udpated dog with id {}".format(id),
			status=200
		), 200
	# if this dog does not belong to logged in user
	else:
		#return you can only update your own dogs
		return jsonify(
			data={'error': 'Forbidden'},
			message=f"Dog's owner_id ({dog.owner.id}) does not match that of logged in user ({current_user.id}). User can only update their own dogs.",
			status=403
		), 403

# route that will take an id and let us create a dog associated with the owner that has that id
@dogs.route('/<owner_id>', methods=['POST'])
def create_dog_with_owner(owner_id):
	payload = request.get_json()
	print(payload)

	# create dog associated with <owner_id>
	dog = models.Dog.create(
		name=payload['name'],
		breed=payload['breed'],
		owner=owner_id
	)

	dog_dict = model_to_dict(dog)

	#remove password from the owner
	dog_dict['owner'].pop('password')

	return jsonify(
		data=dog_dict,
		message="Successfully created dog with owner",
		status=201
	), 201


