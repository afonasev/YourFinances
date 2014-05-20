
from bottle import error
from bottle import redirect
from bottle import static_file

from . import errors

from .core import app
from .core import get
from .core import view
from .core import set_cookie
from .core import delete_cookie

from .models import User


@app.route('/')
@view('home')
def home():
    pass


@app.route('/register', method=['GET', 'POST'])
@view('register')
def register():
    username = get('username')
    password = get('password')

    if not username:
        return

    if not password:
        return {'error': 'Password blank!'}

    username = username.lower()

    try:
        User.register(username, password)
    except (User.RegisterError, errors.ValidationError) as exc:
        return {'error': exc}

    set_cookie('username', username)
    redirect('/')


@app.route('/login', method=['GET', 'POST'])
@view('login')
def login():
    username = get('username')
    password = get('password')

    if not username:
        return

    if not password:
        return {'error': 'Password blank!'}

    username = username.lower()

    try:
        User.auth(username, password)
    except User.DoesNotExist:
        return {'error': 'User with that name does not exists!'}
    except User.AuthError as exc:
        return {'error': exc}

    set_cookie('username', username)
    redirect('/')


@app.route('/logout')
def logout():
    delete_cookie('username')
    redirect('/')


@app.route('/<filetype>/<filepath:path>')
def static(filepath, filetype=None):
    static_path = './finances/static/' + filetype
    return static_file(filepath, root=static_path)


@error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'
