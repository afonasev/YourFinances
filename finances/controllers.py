import re
import datetime

import peewee

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
from .models import Type
from .models import Transaction


@app.route('/')
def index():
    redirect('/expenses')


@app.route('/expenses', method=['GET'])
@view('expenses')
@login_required
def expenses(user):
    return {
        'expenses': user.transactions.where(
            Transaction.type == Type.get(name='Расход')
        ).order_by(Transaction.date.desc(), Transaction.id.desc())
    }


@app.route('/expenses/add', method=['POST'])
@login_required
def expenses_delete(user):
    Transaction.create(
        user=user,
        type=Type.get(name='Расход'),
        category=get('category'),
        date=get('date') if get('date') else datetime.date.today(),
        value=get('value'),
        description=get('description'),
    )
    redirect('/expenses')


@app.route('/expenses/remove/<expense_id>', method=['GET'])
@login_required
def expenses_delete(user, expense_id):
    Transaction.delete_user_transaction(user, expense_id)
    redirect('/expenses')


@app.route('/incoming')
@login_required
def incoming(user):
    return 'В разработке...'


def validate_name_pass(func):
    def wrapper():
        username = get('username')
        password = get('password')

        if not username or not password:
            return

        if len(username) < 6:
            return {'error': 'Логин должен быть не короче 6 символов'}

        if len(password) < 6:
            return {'error': 'Пароль должен быть не короче 6 символов'}

        return func(username.lower(), password)
    return wrapper


@app.route('/register', method=['GET', 'POST'])
@view('register')
@validate_name_pass
def register(username, password):
    email = get('email')

    if not email:
        return

    if not is_valid_email(email):
        return {'error': 'Некорректный email адрес'}

    try:
        User.register(username, password, email)
    except peewee.IntegrityError as exc:
        if 'UNIQUE constraint failed' not in str(exc):
            raise

        return {
            'error': 'Пользователь с таким именем или email`ом уже существует'
        }

    set_cookie('username', username)
    redirect('/')


def is_valid_email(email):
    return bool(re.search('.+@.+\..+', email))


@app.route('/login', method=['GET', 'POST'])
@view('login')
@validate_name_pass
def login(username, password):
    try:
        User.auth(username, password)
    except User.DoesNotExist as exc:
        return {'error': 'Неверное имя пользователя или пароль'}

    set_cookie('username', username)
    redirect('/')


@app.route('/logout')
def logout():
    delete_cookie('username')
    redirect('/login')


@app.route('/<filetype>/<filepath>')
def static(filepath, filetype=None):
    return static_file(filepath, root=app.config['static_path'] + filetype)


@error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format! ERROR %r' % code


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist! ERROR %r' % code
