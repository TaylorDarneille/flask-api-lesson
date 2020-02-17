# this app.py file is like server.js in the express unit
from flask import Flask # like const express = require('express')

DEBUG = True # print nice helpful error messages since we're in development
PORT = 8000

# this is like const app = express()
# instantiating the Flask class
app = Flask(__name__)

# here's how you write a route in flask
# note the default URL ends in /
@app.route('/') # @ symbol here means this i sa decorator
def index():
	return 'Hello, world!'

# this i slike app.listen() in express -- at the bottom
# __name__ being '__main__' here means that we just ran this file as opposed to exporting it and importing it somewhere else
if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT)