
import bottle

from bottle import view, redirect

from . import app
from . import utils
from .models import User
from .models import Account
from .utils import redirect_back
from .utils import login_required
from .utils import errors_handler
from .utils import ApplicationError


class PageNotExist(ApplicationError):
    pass


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
    redirect_back()


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
    redirect_back()


@app.get('/account/delete/<name>')
@login_required
def account_delete(user, name):
    Account.get(name=name, owner=user).delete_instance()
    redirect_back()


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
    utils.del_cookie('user_id')
    redirect('/login')


@app.get('/<filetype>/<filepath>')
def static(filetype, filepath):
    return bottle.static_file(
        filepath, root=app.config['STATIC_PATH'] + filetype
    )


@app.error(404)
@view('error404')
@errors_handler
def mistake404(code):
    raise PageNotExist('Sorry, this page does not exist (404 error)')
