# from flask import Flask is like const express = require('express')
# jsonify lets us send JSON HTTP responses
# g lets us use global variable for the life of (i.e. in the context of )
from flask import Flask, jsonify, g

# get a pakage that will let us handle CORS
# https://flask-cors.readthedocs.io.en/latest/
from flask_cors import CORS

# we need to import and configure the login manager
# https://flask-login.readthedocs.io.en/latest/#flask_login.LoginManager
# LM is the main tool for coordinating sessions/login stuff in our app
from flask_login import LoginManager

from resources.dogs import dogs # import blueprint from ./resources/dogs
from resources.users import users
# in python you import a file and you get everything in the "global scope" of that file
# so this statement imports all variables and methods from that file as properties on the models object (e.g. models.initialize() is available here)
# noe we did not explicitly export anything in models.py
# google 'namespacing in python'
import models

DEBUG = True # primt nice helpful error messages since we're in development
PORT = 8000

# this is like the const app = express()
# instantiating the Flask class
app = Flask(__name__)

#according to this
# https://flask-login.readthedocs.io/en/latest/#configuring-your-application
# we need to do several things

# 1. set up a secret key
# https://flask.palletprojects.com/en/1.1.x.quickstart/#sessions
app.secret_key = "Good Tea. Nice House. This is very secret."

# 2. instantiate LoginManager to get a login_manager
login_manager = LoginManager()

#3. actually connect the app with teh login manager
login_manager.init_app(app)

# CORS = Cross Origin Resource Sharing
# a web domain is an "origin"
# This app is localhost:8000, that's an origin
# our React app is localhouse:3000, that's a different origin
# Browsers implement CORS to prevent a JS app from sending requests to origins other than the one the browser originally went to to get the JS
# (i.e. say some JS tries to send data to some nefarious 3rd party)
# configuring CORS lets browser say "here's who I'm expecting to hear from"
# (certain origins)
# first arg -- we add cors to blueprints
# second arg -- list of allowed origins
# third arg -- lets us accept requests with cookies attached, this allows us to use sessions for auth
CORS(dogs, origins=['http://localhost:3000'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)


# we are using blueprints to make "controllers"
# "use this bluprint (component/piece/section of the app) to handle the dog stuff"
# analogous to app.use('/dogs', dogController)
# the point of the api v no is to let you build an upgraded API with a different url prefix, adn let yoru old API remain intact so that you don't break a bunch of apps already built on top of yoru old API with the old URLS
app.register_blueprint(dogs, url_prefix='/api/v1/dogs')
app.register_blueprint(users, url_prefix='/api/v1/users')


# we dont want ot hog up the SQL connection pool so we should connect to the DB before every request and close the db connection after every request
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

# here's how you write a route in flask
# note the default URL ends in /
@app.route('/') # @ symbol here means this is a decorator
def index():
	return 'Hello, world!'

# it's finicky abou types -- eg you can't return a list
# check the error message at this route
# @app.route('/test')
# def test_list():
# 	return ['hello', 'there']

# lets use the jsonify module to try to send the lst as json
# @app.route('/test_json')
# def test_json():
# 	# we are using jsonify to create a JSON response
# 	# this is analogous to res.json() in express
# 	return jsonify(['hello', 'there'])

# @app.route('/cat_json')
# def get_cat_json():
# 	# you can pass key value pairs into jsonify()
# 	return jsonify(name="Nico", age=15)

# you can use a dictionary as the value of one of the key-value pairs in jsonify()
# @app.route('/nested_json')
# def get_nested_json():
# 	nico = {
# 		'name': 'Nico',
# 		'age': 15
# 	}
# 	return jsonify(name="Reuben", age=14, cat=nico)

# url parameters in flask look like this
# username is teh URL param below like :username in express
# @app.route('/say_hello/<username>')
# def say_hello(username): # this func takes URL param as arg
# 	return "Hello {}".format(username)

# this is like app.listen() in express -- at the bottom
# __name__ being '__main__' here mean sthat we just ran this file as opposed to exporting it and importing it somewhere else
if __name__=='__main__':
	# when we start the app set up our tables (if necessary) as defined in models.py
	# remember in express we required db.js before app.listen
	models.initialize()
	app.run(debug=DEBUG, port=PORT)