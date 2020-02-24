import os

# from flask import Flask is like const express = require('express')
# jsonify lets us send JSON HTTP responses
# g lets us use global variable for the life of (i.e. in the context of )
from flask import Flask, jsonify, g

# get a package that will let us handle CORS
# https://flask-cors.readthedocs.io.en/latest/
from flask_cors import CORS

# we need to import and configure the login manager
# https://flask-login.readthedocs.io.en/latest/#flask_login.LoginManager
# LM is the main tool for coordinating sessions/login stuff in our app
from flask_login import LoginManager

from resources.dogs import dogs
from resources.users import users
# in python you import a file and you get everything in the "global scope" of that file
# so this statement imports all variables and methods from that file as properties on the models object (e.g. models.initialize() is available here)
# note we did not explicitly export anything in models.py

# google 'namespacing in python'
import models

DEBUG = True # primt nice helpful error messages since we're in development
PORT = 8000

# this is like the const app = express()
# instantiating the Flask class
app = Flask(__name__)

# ------ flask-login things -------

# 1. set up a secret key
app.secret_key = "Equip Sunglasses"
# 2. instantiate LoginManager to get a login_manager
login_manager = LoginManager()
#3. actually connect the app with the login manager
login_manager.init_app(app)

# in register and login we did login_user(user that was found or created)
# that puts the ID of that user in session
# to use the user object use id that is, you must define a callback for user_loader(part of login manager) to us
# userloader will use this callback to load the user object
# see https://flask-login.readthedocs.io.en/latest/#how-it-works
@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

# https://flask-login.readthedocs.io/en/latest/#customizing-the-login-process
@login_manager.unauthorized_handler
def unautheroized():
	return jsonify(
		data={
			'error': 'User not logged in'
		},
		message="You must be logged in to access that resource",
		status=401
	), 401

# CORS = Cross Origin Resource Sharing
# first arg -- we add cors to blueprints
# second arg -- list of allowed origins
# third arg -- lets us accept requests with cookies attached, this allows us to use sessions for auth
CORS(dogs, origins=['http://localhost:3000'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)

# blueprints <> controllers
app.register_blueprint(dogs, url_prefix='/api/v1/dogs')
app.register_blueprint(users, url_prefix='/api/v1/users')

@app.before_request # use this decorator to cause a function to run before reqs
def before_request():
	"""Connect to the db before each request"""
	# store the database as a global var in g
	g.db=models.DATABASE
	g.db.connect()

@app.after_request # use this decorator to cause a function to run after reqs
def after_request(response):
	"""Close the db connection after each request"""
	g.db.close()
	return response # go ahead and send the response back to client (in our case this will be some JSON)

@app.route('/')
def index():
	return 'Hello, world!'

if 'ON_HEROKU' in os.environ:
	print('\non heroku!')
	models.initialize()

# this is like app.listen() in express -- at the bottom
# __name__ being '__main__' here means that we just ran this file as opposed to exporting it and importing it somewhere else
if __name__=='__main__':
	models.initialize() # this is defined in models.py
	app.run(debug=DEBUG, port=PORT)