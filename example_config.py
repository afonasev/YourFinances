# make finances_config.py with your parameters
import os


_basedir = os.path.abspath(os.path.dirname(__file__))

STATIC_PATH = os.path.join(_basedir, './finances/static/')
VIEWS_PATH = os.path.join(_basedir, './finances/views/')
DB_PATH = os.path.join(_basedir, './data.db')

SECRET_KEY = os.urandom(64)
