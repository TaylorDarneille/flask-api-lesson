import datetime

# all our models will go in this file

# peewee is similar ot mongoose
from peewee import *
# import * means everything, including:
# SqliteDatabase -- adapter that lets us connect to sqlite databases (see below)
# and
# Model -- the Model() class is what we will inherit from when defining our models (similar to using some stuff from the mongoos module when creating a schema and then a model in mongoose)

# we weill use this module ot set up User model, sessions, logins, authentication, require authentication for certain things, etc.
# the UserMixin in what we need to make our User model
# https://flask-login.readthedocs.io/en/latest/
from flask_login import UserMixin


# sqlite is a way to have a "database" that's just stored in a file
# it's great for development because you can have easily portable data (on git, eg)
# later when deploying, we will change this to psql
DATABASE = SqliteDatabase('dogs.sqlite')
# analogous to MONGO_DB_URL = 'mongodb://localhost/dogs', {...}

# to behave correcly in flask-login's session/login/etc functionality, the User class must have some methods and properties that Model from peewee doesn't have
# we could write these ourselves, adn/or we could also have our User class inherit from UserMixin (in addition to pweewee's Model class), which will provide/implement them for us
# https://flask-login.readthedocs.io.en/latest/#your-user-class
class User(UserMixin, Model):
	username=CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()

	class Meta: database=DATABASE

# defining our Dog model
# note Dog inherits from Model, this gives us methods to do CRUD actions and to define attribute/field/column names and types
# see here: http://docs.peewee-orm.com/en/latest/peewee/models.html#
# http://docs.peewee-orm.com/en/latest/peewee/models.html#fields
class Dog(Model):
	name = CharField() # string
	
	# to set up our 1:M relationship between users and dogs we will need a foreign key
	# http://docs.peewee-orm.com/en/latest/peewee/example.html#models
	owner = ForeignKeyField(User, backref='dogs')
	# if we had a dog model instance in a variable called some_dog, the FK will let us go some_dog.owner to get the owner
	# and if we had a user model instance in a var called some_user, the bakref will allow us ot go some_user.dogs ot get a list of dog instances

	breed = CharField()
	# this is how you specify default values
	created_at = DateTimeField(default=datetime.datetime.now) # mistake on purpose
	# we often need to import things in python that might be built in in other languages
	# this keeps python lightweight

	# special constructor that gives our class instructions on how to connect to a specific database
	class Meta:
		database = DATABASE # use the DB defined above as DATABASE for this model

# define a method that will get called in app.py to set up DBs/connection
# similar to how we ran /db/db.js in server.js in express unit
def initialize(): # note we are making this name up
	DATABASE.connect() # analogous to mongoose.connect(...)

	# we need to explicitly create the tables based on the schema definitions above
	DATABASE.create_tables([User, Dog], safe=True)
	print("Connected to DB and created tables if they weren't already there")

	# with SQL, dont' leave DB connection open, we dont want to hog up space in the connection pool
	DATABASE.close()