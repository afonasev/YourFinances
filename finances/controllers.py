import re

import peewee

from bottle import view
from bottle import error
from bottle import redirect
from bottle import static_file

from . import app

from .utils import set_cookie
from .utils import delete_cookie
from .utils import get_email_pass
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
    pass


@app.route('/register', method=['GET'])
@view('register')
def register():
    pass


@app.route('/register', method=['POST'])
@view('register')
def _register():
    email, password, errors = get_email_pass()

    if email and not is_valid_email(email):
        errors.append('Invalid email')

    if password:
        if len(password) < 6:
            errors.append(
                'Length of password must be greater than 5 letters'
            )

        if not re.search('\d+', password):
            errors.append('The password should contain numbers')

        if not re.search('[a-zA-Z]+', password):
            errors.append('The password should contain letters')

    if errors:
        return {'errors': errors}

    try:
        user = User.register(email, password)
    except peewee.IntegrityError as exc:
        if 'email is not unique' in str(exc):
            return {'errors': ['User with this email already exists']}
        raise

    except Exception as exc:
        print(exc)

    set_cookie('user_id', user.id)
    redirect('/')


@app.route('/login', method=['GET'])
@view('login')
def login():
    pass


@app.route('/login', method=['POST'])
@view('login')
def _login():
    email, password, errors = get_email_pass()

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
