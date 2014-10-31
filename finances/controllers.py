
import bottle

from bottle import view, redirect

from . import app
from . import utils
from .models import User, Account
from .utils import login_required


@app.get('/')
def index():
    redirect('/account')


@app.get('/account')
@view('account/list')
@login_required
def account_list(user):
    is_personal = utils.get_param('is_personal')
    if is_personal is not None:
        return {'is_personal': bool(int(is_personal))}


@app.post('/account')
@view('account/list')
@login_required
def account_create(user):
    name = utils.get_param('name')
    is_personal = bool(utils.get_param('is_personal'))

    errors = []

    if not name:
        errors.append('Account name is empty')

    elif len(name) < 6:
        errors.append(
            'Length of account name must be greater than 5 letters'
        )

    if errors:
        return {'errors': errors}

    try:
        Account.reg(owner=user, name=name, is_personal=is_personal)
    except Account.UniqueError:
        return {'errors': ['Account with this name already exists']}


@app.post('/account/<name>')
@view('account/list')
@login_required
def account(user, name):
    account = Account.get(name=name, owner=user)
    errors = []

    new_name = utils.get_param('name')

    if new_name:
        if len(new_name) < 6:
            return {'errors': 'Account name is empty'}
        account.name = new_name

    balance = utils.get_param('balance')

    if balance is not None:
        account.balance = balance

    account.save()
    redirect('/account')


@app.get('/account/delete/<name>')
@login_required
def account_delete(user, name):
    Account.get(name=name, owner=user).delete_instance()
    redirect('/account')


@app.get('/register')
@view('auth/register')
def register():
    pass


@app.post('/register')
@view('auth/register')
def register_do():
    email, password, errors = utils.get_email_pass()

    if email:
        errors.extend(utils.validate_email(email))

    if password:
        errors.extend(utils.validate_password(password))

    if errors:
        return {'errors': errors}

    try:
        user = User.reg(email, password)
    except User.UniqueError:
        return {'errors': ['User with this email already exists']}

    utils.set_cookie('user_id', user.id)
    redirect('/')


@app.get('/login')
@view('auth/login')
def login():
    pass


@app.post('/login')
@view('auth/login')
def login_do():
    email, password, errors = utils.get_email_pass()

    if errors:
        return {'errors': errors}

    try:
        user = User.auth(email, password)
    except User.DoesNotExist:
        return {'errors': ['Wrong email or password']}

    utils.set_cookie('user_id', user.id)
    redirect('/')


@app.get('/logout')
def logout():
    utils.delete_cookie('user_id')
    redirect('/login')


@app.get('/<filetype>/<filepath>')
def static(filetype, filepath):
    return bottle.static_file(
        filepath, root=app.config['STATIC_PATH'] + filetype
    )


@bottle.error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format! ERROR %r' % code


@bottle.error(404)
def mistake404(code):
    return 'Sorry, this page does not exist! ERROR %r' % code
