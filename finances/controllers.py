import re

import peewee

from bottle import view
from bottle import error
from bottle import redirect
from bottle import static_file

from . import app

from .utils import get_param
from .utils import set_cookie
from .utils import delete_cookie
from .utils import is_valid_email
from .utils import login_required

from .models import User


@app.route('/')
def index():
    redirect('/accounts')


@app.route('/accounts')
@view('accounts')
@login_required
def accounts(user):
    # return {'accounts': Account.get_accounts(user)}
    pass


@app.route('/register', method=['GET'])
@view('register')
def register():
    pass


@app.route('/register', method=['POST'])
@view('register')
def _register():
    email = get_param('email')
    password = get_param('password')

    errors = []

    if not email:
        errors.append('Email empty')

    if not password:
        errors.append('Password empty')

    if email and not is_valid_email(email):
        errors.append('Invalid email')

    if password:
        if len(password) < 6:
            errors.append(
                'Length of password must be greater than 5 letters'
            )

        if re.match('\d+', password):
            errors.append('The password should contain numbers')

        if re.match('\w+', password):
            errors.append('The password should contain letters')

    if errors:
        return {'errors': errors}

    try:
        user = User.register(email, password)
    except peewee.IntegrityError as exc:
        if 'UNIQUE constraint failed' not in str(exc):
            raise

        return {'errors': ['User with this email already exists']}

    set_cookie('user_id', user.id)
    redirect('/')


@app.route('/login', method=['GET'])
@view('login')
def login():
    pass


@app.route('/login', method=['POST'])
@view('login')
def _login():
    email = get_param('email')
    password = get_param('password')

    errors = []

    if not email:
        errors.append('Email empty')

    if not password:
        errors.append('Password empty')

    if errors:
        return {'errors': errors}

    try:
        user = User.auth(email, password)
    except User.DoesNotExist:
        return {'errors': ['Wrong email or password']}

    set_cookie('user_id', user.id)
    redirect('/')


@app.route('/logout')
def logout():
    delete_cookie('user_id')
    redirect('/login')


@app.route('/<filetype>/<filepath>')
def static(filetype, filepath):
    return static_file(filepath, root=app.config['STATIC_PATH'] + filetype)


@error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format! ERROR %r' % code


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist! ERROR %r' % code
