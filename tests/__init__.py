import peewee

from finances import app
from finances import models

database = peewee.SqliteDatabase(':memory:')
models.database.initialize(database)

app.secret_key = 'VERY SECRET KEY'
