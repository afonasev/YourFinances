import os

import bottle


app = bottle.Bottle()

get = lambda name: bottle.request.params.get(name)

get_cookie = lambda name: bottle.request.get_cookie(
    name, secret=app.config['secret_key']
)

set_cookie = lambda name, val: bottle.response.set_cookie(
    name, val, secret=app.config['secret_key']
)

delete_cookie = lambda name: bottle.response.delete_cookie(name)


def login_required(func):
    def wrapper(*args, **kwargs):
        if not get_cookie('username'):
            bottle.redirect('/login')
        return func(*args, **kwargs)
    return wrapper
