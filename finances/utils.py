import re
import base64
import hashlib

import bottle

from . import app


class ApplicationError(Exception):
    pass


get = lambda name: bottle.request.params.getunicode(name)

get_cookie = lambda name: bottle.request.get_cookie(
    name, secret=app.config['SECRET_KEY']
)

set_cookie = lambda name, val: bottle.response.set_cookie(
    name, val, secret=app.config['SECRET_KEY']
)

del_cookie = lambda name: bottle.response.delete_cookie(name)


def errors_handler(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)

        except ApplicationError as exc:
            return {'error': exc}

        return res
    return wrapper


def login_required(func):
    def wrapper(*args, **kwargs):
        from . import User
        user_id = get_cookie('user_id')

        if not user_id:
            bottle.redirect('/login')

        if not User.check(id=user_id):
            bottle.redirect('/login')
        user = User.get(id=user_id)

        res = func(user, *args, **kwargs) or {}
        res['user'] = user

        return res
    return wrapper


def get_hash(text):
    return base64.b64encode((hashlib.sha256(text.encode()).digest()))
