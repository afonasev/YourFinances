import os

import bottle

bottle.TEMPLATE_PATH.remove('./views/')
bottle.TEMPLATE_PATH.append('./finances/views')

app = bottle.Bottle()
app.config['secret_key'] = os.urandom(40)
app.config['database'] = 'finances.db'

get = lambda name: bottle.request.params.get(name)
get_cookie = lambda name: bottle.request.get_cookie(name, secret=app.config['secret_key'])
set_cookie = lambda name, val: bottle.response.set_cookie(name, val, secret=app.config['secret_key'])
delete_cookie = lambda name: bottle.response.delete_cookie(name)


def view(tpl_name, **defaults):
    def decorator(func):
        def inside_decorator(f):
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                username = get_cookie('username')
                if result is not None:
                    result['username'] = username
                else:
                    result = {'username': username}
                return result
            return wrapper
        return bottle.view(tpl_name, **defaults)(inside_decorator(func))
    return decorator


from .controllers import *
