#this is like a "user controller" or maybe an "auth controller"
import models

from flask import Blueprint, request

#maket this a blueprint
users = Blueprint('users','users')

@users.route('/', methods=['GET'])
def test_user_resource():
	return "we have a user resource"

@users.route('/register/', methods=['POST'])
def register():
	print(request.get_json())
	return "check terminal"