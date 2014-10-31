import re
import base64
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

        res = func(user, *args, **kwargs) or {}
        res['user'] = user

        return res
    return wrapper


def get_hash(text):
    return base64.b64encode((hashlib.sha256(text.encode()).digest()))


def get_email_pass():
    email = get_param('email')
    password = get_param('password')

    errors = []

    if not email:
        errors.append('Email is empty')

    if not password:
        errors.append('Password is empty')

    return email, password, errors


def validate_email(email):
    errors = []

    if not bool(re.search('.+@.+\..+', email)):
        errors.append('Email is not valid')

    return errors


def validate_password(password):
    errors = []

    if len(password) < 6:
        errors.append(
            'Length of password must be greater than 5 letters'
        )

    if not re.search('\d+', password):
        errors.append('The password should contain numbers')

    if not re.search('[a-zA-Z]+', password):
        errors.append('The password should contain letters')

    return errors
