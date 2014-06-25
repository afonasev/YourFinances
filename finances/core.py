import hashlib

import bottle


app = bottle.Bottle()

get = lambda name: bottle.request.params.getunicode(name)

get_cookie = lambda name: bottle.request.get_cookie(
    name, secret=app.config['secret_key']
)

set_cookie = lambda name, val: bottle.response.set_cookie(
    name, val, secret=app.config['secret_key']
)

delete_cookie = lambda name: bottle.response.delete_cookie(name)


def login_required(func):
    def wrapper(*args, **kwargs):
        from . import User
        username = get_cookie('username')

        if not username:
            bottle.redirect('/login')

        try:
            user = User.get(name=username)
        except User.DoesNotExist:
            user = None

        if not user:
            bottle.redirect('/login')

        return func(user, *args, **kwargs)
    return wrapper


def get_hash(text):
    return hashlib.sha224(text.encode()).hexdigest()
