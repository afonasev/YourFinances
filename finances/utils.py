import re
import base64
import hashlib

import bottle

from . import app


class ApplicationError(Exception):
    pass


def get(name):
    val = bottle.request.params.getunicode(name)
    return val.strip() if val else None

get_cookie = lambda name: bottle.request.get_cookie(
    name, secret=app.config['SECRET_KEY']
)

set_cookie = lambda name, val: bottle.response.set_cookie(
    name, val, secret=app.config['SECRET_KEY']
)

del_cookie = lambda name: bottle.response.delete_cookie(name)


def get_user():
    from .models import User
    user_id = get_cookie('user_id')
    if User._check(id=user_id):
        return User.get(id=user_id)
    return None


def view(tpl_name, **defaults):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except ApplicationError as exc:
                return {'error': exc}
            return res
        return bottle.view(tpl_name, **defaults)(wrapper)
    return decorator


def redirect_back():
    try:
        referer = bottle.request.headers['referer']
    except KeyError:
        bottle.redirect('/')

    host = bottle.request.remote_addr

    if host in referer:
        route = re.findall(r'//.*?(/.*)', referer)[0]
        bottle.redirect(route)

    bottle.redirect('/')


def login_required(func):
    def wrapper(*args, **kwargs):
        user = get_user()
        if not user:
            bottle.redirect('/login')
        return func(user, *args, **kwargs)
    return wrapper


def get_hash(text):
    return base64.b64encode((hashlib.sha256(text.encode()).digest()))
