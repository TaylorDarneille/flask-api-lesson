# all our models will go in this file

# peewee is similar ot mongoose
from peewee import *
# import * means everything, including:
# SqliteDatabase -- adapter that lets us connect to sqlite databases (see below)
# and
# Model -- the Model() class is what we will inherit from when defining our models (similar to using some stuff from the mongoos module when creating a schema and then a model in mongoose)

# sqlite is a way to ha a "database" that's just stored in a file
# it's great fo rdevelopment because you can have easily portable data (on git, eg)
# later when deploying, we will change this to psql
DATABASE = SqliteDatabase('dogs.sqlite')
# analogous to MONGO_DB_URL = 'mongodb://localhost/dogs', {...}


# defining our Dog model
# note Dog inherits from Model, this gives us methods to do CRUD actions and to define attribute/field/column names and types
# see here: http://docs.peewee-orm.com/en/latest/peewee/models.html#
# http://docs.peewee-orm.com/en/latest/peewee/models.html#fields
class Dog(Model):
	name = CharField() # string
	owner = CharField() # string for now, later we will implement a relation
	breed = CharField()
	# this is how you specify default values
	created_at = DateTimeField(default=datetime.datetime.now) #mistake on purpose

	# special constructor that gives our class instructions on how to connect to a specific database
	class Mega:
		database = DATABASE # use the DB defined above as DATABASE for this model

# define a method that will get called in app.py to set up DBs/connection
# similar to how we ran /db/db.js in server.js in express unit
def initialize(): # note we are making this name up
	DATABASE.connect() # analogous to mongoose.connect(...)

	# we need to explicitly create the tables based on the schema definitions above
	DATABASE.create_tables([Dog], safe=True)
	print("Connected to DB and created tables if they weren't already there")

	# with SQL, dont' leave DB connection open, we dont want to hog up space in the connection pool
	DATABASE.close()