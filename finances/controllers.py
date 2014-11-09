from datetime import datetime

import peewee
from bottle import redirect
from bottle import static_file

from . import app
from . import utils
from .models import User
from .models import Account
from .models import Transaction
from .utils import view
from .utils import redirect_back
from .utils import login_required
from .utils import ApplicationError


class PageNotExist(ApplicationError):
    pass


@app.get('/')
def index():
    redirect('/account')


@app.get('/register')
@view('auth/register')
def register():
    pass


@app.post('/register')
@view('auth/register')
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
def login_do():
    user = User.auth(utils.get('email'), utils.get('password'))
    utils.set_cookie('user_id', user.id)
    redirect('/')


@app.get('/logout')
def logout():
    utils.del_cookie('user_id')
    redirect('/login')


@app.get('/account')
@view('accounts')
@login_required
def accounts(user):
    res = {}

    # TODO: REFACTOR ME
    is_personal = utils.get('is_personal')
    if is_personal is not None:
        res['is_personal'] = bool(int(is_personal))

    return res


@app.post('/account')
@view('accounts')
@login_required
def create_account(user):
    Account.reg(
        owner=user, name=utils.get('name'),
        is_personal=utils.get('is_personal') or False,
    )
    redirect_back()


@app.post('/account/<name>')
@view('accounts')
@login_required
def update_account(user, name):
    # TODO: REFACTOR ME
    account = Account.get(name=name, owner=user)

    if utils.get('name'):
        account.name = utils.get('name')

    if utils.get('balance') is not None:
        account.balance = utils.get('balance')

    account.save()
    redirect_back()


@app.get('/account/delete/<name>')
@login_required
def delete_account(user, name):
    # TODO: REFACTOR ME
    try:
        Account.get(name=name, owner=user).delete_instance()
    except peewee.DoesNotExist:
        pass

    redirect_back()


@app.post('/transaction')
@view('accounts')
@login_required
def create_transaction(user):
    # TODO: REFACTOR ME
    date = utils.get('date')

    if date:
        date = datetime.strptime(date, '%Y-%m-%d').date()

    Transaction.reg(
        creator=user,
        source=Account.get(id=utils.get('source_id')),
        target=Account.get(id=utils.get('target_id')),
        amount=float(utils.get('amount')),
        description=utils.get('description'),
        date=date,
    )
    redirect_back()


@app.get('/transaction/delete/<id>')
@login_required
def delete_transaction(user, id):
    # TODO: REFACTOR ME
    try:
        user.transactions.where(Transaction.id == id).get().delete_instance()
    except peewee.DoesNotExist:
        pass

    redirect_back()


@app.get('/<filetype>/<filepath>')
def static(filetype, filepath):
    return static_file(filepath, root=app.config['STATIC_PATH'] + filetype)


@app.error(404)
@view('error404')
def mistake404(code):
    raise PageNotExist('Sorry, this page does not exist (404 error)')
