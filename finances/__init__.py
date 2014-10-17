import logging

import bottle
import peewee

app = bottle.Bottle()

try:
    import config
except ImportError:
    import example_config as config

app.config.update({
    'SECRET_KEY': config.SECRET_KEY,
    'STATIC_PATH': config.STATIC_PATH,
})

bottle.TEMPLATE_PATH = [config.VIEWS_PATH]

from . import models

database = peewee.SqliteDatabase(config.DB_PATH)
models.database.initialize(database)

logger = logging.getLogger('peewee')
logger.setLevel(logging.FATAL)
logger.addHandler(logging.StreamHandler())

from .controllers import *
