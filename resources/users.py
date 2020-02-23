#this is like a "user controller" or maybe an "auth controller"
import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from playhouse.shortcuts import model_to_dict

#maket this a blueprint
users = Blueprint('users','users')

@users.route('/', methods=['GET'])
def test_user_resource():
	return "we have a user resource"

@users.route('/register/', methods=['POST'])
def register():
	payload = request.get_json()
	# since emails are case insensitive in the world...
	payload['email'] = payload['email'].lower()
	# why not make usernames case insensitive too while we're at it
	payload['username'] = payload['username'].lower()

	try:
		# see if user exists
		# if they do, we dont' want to create them
		models.User.get(models.User.email == payload['email'])
		# extra challenge -- make it so this also does not allow duplicate username


		# this will throw an error ("models.DoesNotExist exception") if they don't exist
		# if it doens't throw that error, then the username is taken
		return jsonify(
			data={},
			message="A user with that email already exists",
			status=401
		), 401

	except models.DoesNotExist: # Except is like catchin JS
		# in this except, we are safe to create user
		print("in except")
		created_user = models.User.create(
			username=payload['username'],
			email=payload['email'],
			password=generate_password_hash(payload['password'])
		)

		user_dict=model_to_dict(created_user)
		print(user_dict)

		# note the type of the password
		print(type(user_dict['password']))

		# we can't jsonify the password (generate_password_hash gives us something of type "bytes" which is unserializable) and there is no reason to send hashed pw string back to the user anyway so let's delete it
		user_dict.pop('password')


		return jsonify(
			data=user_dict,
			messages=f"successfuly registered {user_dict['email']}",
			status=201
		), 201











