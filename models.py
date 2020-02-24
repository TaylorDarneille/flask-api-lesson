import os
import datetime
from peewee import *
from flask_login import UserMixin

# for deployment
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
	DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
	DATABASE = SqliteDatabase('dogs.sqlite')

# to behave correcly in flask-login's session/login/etc functionality, the User class must have some methods and properties that Model from peewee doesn't have
# we could write these ourselves, and/or we could also have our User class inherit from UserMixin (in addition to pweewee's Model class), which will provide/implement them for us
# https://flask-login.readthedocs.io.en/latest/#your-user-class
class User(UserMixin, Model):
	username=CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()

	class Meta:
		database=DATABASE

class Dog(Model):
	name = CharField() # string
	owner = ForeignKeyField(User, backref='dogs')
	breed = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

# this will get called in app.py
def initialize(): # note we are making this name up
	DATABASE.connect() # analogous to mongoose.connect(...)
	DATABASE.create_tables([User, Dog], safe=True)
	print("Connected to DB and created tables if they weren't already there")
	DATABASE.close() # close connection so you're not taking up space

