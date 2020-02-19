# this file is like dogcongtroller.js
import models

from flask import Blueprint

# first arg is the blueprint's name
# second arg is its import_name
dogs = Blueprint('dogs', 'dogs')

@dogs.route('/')
def dogs_index():
	return "dogs resource working"