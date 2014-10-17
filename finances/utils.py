import re
import hashlib

import bottle

from . import app


get_param = lambda name: bottle.request.params.getunicode(name)

get_cookie = lambda name: bottle.request.get_cookie(
    name, secret=app.config['SECRET_KEY']
)

set_cookie = lambda name, val: bottle.response.set_cookie(
    name, val, secret=app.config['SECRET_KEY']
)

delete_cookie = lambda name: bottle.response.delete_cookie(name)


def login_required(func):
    def wrapper(*args, **kwargs):
        from . import User
        user_id = get_cookie('user_id')

        if not user_id:
            bottle.redirect('/login')

        try:
            user = User.get(id=user_id)
        except User.DoesNotExist:
            bottle.redirect('/login')

        return func(user, *args, **kwargs)
    return wrapper


def get_hash(text):
    return hashlib.sha224(text.encode()).hexdigest()


def is_valid_email(email):
    return bool(re.search('.+@.+\..+', email))


def get_email_pass():
    email = get_param('email')
    password = get_param('password')

    errors = []

    if not email:
        errors.append('Email is empty')

    if not password:
        errors.append('Password is empty')

    return email, password, errors
