
import bottle

from bottle import view, redirect

from . import app
from . import utils
from .models import User, Account
from .utils import login_required, errors_handler


@app.get('/')
def index():
    redirect('/account')


@app.get('/account')
@view('account/list')
@login_required
def account_list(user):
    res = {}

    is_personal = utils.get('is_personal')
    if is_personal is not None:
        res['is_personal'] = bool(int(is_personal))

    return res


@app.post('/account')
@view('account/list')
@login_required
@errors_handler
def account_create(user):
    Account.reg(
        owner=user,
        name=utils.get('name'),
        is_personal=utils.get('is_personal') or False,
    )


@app.post('/account/<name>')
@view('account/list')
@login_required
@errors_handler
def account(user, name):
    account = Account.get(name=name, owner=user)

    if utils.get('name'):
        account.name = utils.get('name')

    if utils.get('balance') is not None:
        account.balance = utils.get('balance')

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
@errors_handler
def register_do():
    user = User.reg(utils.get('email'), utils.get('password'))
    utils.set_cookie('user_id', user.id)
    redirect('/')


@app.get('/login')
@view('auth/login')
def login():
    pass


@app.post('/login')
@view('auth/login')
@errors_handler
def login_do():
    user = User.auth(utils.get('email'), utils.get('password'))
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
