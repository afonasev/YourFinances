
from bottle import view
from bottle import error
from bottle import redirect
from bottle import static_file

from .core import app
from .core import get
from .core import set_cookie
from .core import delete_cookie
from .core import login_required
from .models import User


@app.route('/')
def index():
    redirect('/spending')


@app.route('/spending')
@view('spending')
@login_required
def spending():
    pass


@app.route('/incoming')
@view('incoming')
@login_required
def incoming():
    pass


def validate_name_pass_form(func):
    def wrapper():
        username = get('username')
        password = get('password')

        if not username or not password:
            return

        if len(username) < 6:
            return {'error': 'Username must be longer than 5 letters'}

        return func(username.lower(), password)
    return wrapper


@app.route('/register', method=['GET', 'POST'])
@view('register')
@validate_name_pass_form
def register(username, password):
    try:
        User.register(username, password)
    except User.RegisterError as exc:
        return {'error': exc}

    set_cookie('username', username)
    redirect('/')


@app.route('/login', method=['GET', 'POST'])
@view('login')
@validate_name_pass_form
def login(username, password):
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
    redirect('/login')


@app.route('/<filetype>/<filepath>')
def static(filepath, filetype=None):
    static_path = './finances/static/' + filetype
    return static_file(filepath, root=static_path)


@error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format! ERROR %r' % code


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist! ERROR %r' % code
