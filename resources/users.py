#this is like a "user controller" or maybe an "auth controller"
import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
# login_user is a funciton tha twill do the session stuff we did manually in express
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

		# this is where we actually use flask-login
		# this "logs in" the user and starts a session
		login_user(created_user)

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

@users.route('/login/', methods=['POST'])
def login():
	payload = request.get_json()
	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()

	try:
		#look up user by email
		user = models.User.get(models.User.email==payload['email'])

		# if we didn't cause a modelsDoesNotExist, then lets check their password
		user_dict = model_to_dict(user)

		# check the user's password using bcrypt
		# check_password_hash: 1st arg = hashed pw you are checking against
		# 2nd arg = pw attempt (i.e. what the user entered)
		password_is_good = check_password_hash(user_dict['password'], payload['password'])

		if password_is_good:
			# THIS IS HOW YOU LOG USER IN IN THE APP USING flask_login
			login_user(user)

			user_dict.pop('password')

			return jsonify(
				data=user_dict,
				message="Successfully logged in {}".format(user_dict['email']),
				status=200
			), 200
		else:
			print('password is no good')

			return jsonify(
				data={},
				message="Email or Password is no good",
				status=401
			), 401

	except models.DoesNotExist: # this means user not found
		print('username is no good')
		return jsonify(
			data={},
			message="Email or Password is incorrect",
			status=401
		), 401

# NOTE: as it is right now, you can put in the wrong username but have the right email and password and get logged in

# we may delete this route later, for now we will use it ot help us manually add a dog using the relation
# it will list all the users
@users.route('/all/', methods=['GET'])
def user_index():
	users = models.User.select()

	user_dicts = [model_to_dict(u) for u in users]
	print(user_dicts) # observe: these contain password

	# let's delete the passwords and not send them back to the user
	# excuse to see how map() works in python
	# define a callback to be run on every dict in user_dicts
	def remove_password(u):
		u.pop('password')
		return u

	user_dicts_without_pw = map(remove_password, user_dicts)

	# this is what is returned
	print(user_dicts_without_pw)
	# it is a map, not a list
	print(type(user_dicts_without_pw))
	# so we should convert it back
	user_dicts_list = list(user_dicts_without_pw)
	print(user_dicts_list)

	return jsonify(data=user_dicts_list), 200

# teaching tool --- route ot show which user is logged in
# demonstrating how to use current_user
# this requires user_loader to be set up in app.py
@users.route('/logged_in', methods=['GET'])
def get_logged_in_user():
	# READ THIS https://flask-login.readthedocs.io.en/latest/#flask_login.current_user
	# because we called login_user and set up user_loader
	print(current_user) # this i sthe logged in user
	print(type(current_user)) # <class 'werkzeug.local.LocalProxy> -- google it if you're interested
	user_dict = model_to_dict(current_user)
	print(user_dict)
	return jsonify(data=user_dict), 200