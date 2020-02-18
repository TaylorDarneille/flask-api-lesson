# this app.py file is like server.js in the express unit

# from flask import Flask is like const express = require('express')
# jsonify lets us send JSON HTTP responses
from flask import Flask, jsonify

DEBUG = True # primt nice helpful error messages since we're in development
PORT = 8000

# this is like the const app = express()
# instantiating the Flask class
app = Flask(__name__)

# here's how you write a route in flask
# note the default URL ends in /
@app.route('/') # @ symbol here means this is a decorator
def index():
	return 'Hello, world!'

# it's finicky abou types -- eg you can't return a list
# check the error message at this route
@app.route('/test')
def test_list():
	return ['hello', 'there']

# lets use the jsonify module to try to send the lst as json
@app.route('/test_json')
def test_json():
	# we are using jsonify to create a JSON response
	# this is analogous to res.json() in express
	return jsonify(['hello', 'there'])

@app.route('/cat_json')
def get_cat_json():
	# you can pass key value pairs into jsonify()
	return jsonify(name="Nico", age=15)

# you can use a dictionary as the value of one of the key-value pairs in jsonify()
@app.route('/nested_json')
def get_nested_json():
	nico = {
		'name': 'Nico',
		'age': 15
	}
	return jsonify(name="Reuben", age=14, cat=nico)

# url parameters in flask look like this
# username is teh URL param below like :username in express
@app.route('/say_hello/<username>')
def say_hello(username): # this func takes URL param as arg
	return "Hello {}".format(username)

# this is like app.listen() in express -- at the bottom
# __name__ being '__main__' here mean sthat we just ran this file as opposed to exporting it and importing it somewhere else
if __name__=='__main__':
	app.run(debug=DEBUG, port=PORT)