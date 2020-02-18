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
# not Dog inherits from Model, this gives us methods to do CRUD actions and to define attribute/field/column names and types
# see here: http://docs.peewee-orm.com/en/latest/peewee/models.html#
# http://docs.peewee-orm.com/en/latest/peewee/models.html#fields