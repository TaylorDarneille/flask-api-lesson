# from flask import Flask is like const express = require('express')
# jsonify lets us send JSON HTTP responses
# g lets us use global variable for the life of (i.e. in the context of )
from flask import Flask, jsonify, g

# get a pakage that will let us handle CORS
# https://flask-cors.readthedocs.io.en/latest/
from flask_cors import CORS

from resources.dogs import dogs # import blueprint from ./resources/dogs

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

# "use this bluprint (component/piece/section of the app) to handle the dog stuff"
# analogous to app.use('/dogs', dogController)
app.register_blueprint(dogs, url_prefix='/api/v1/dogs')

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