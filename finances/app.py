
from bottle import TEMPLATE_PATH
from bottle import static_file
from bottle import request
from bottle import Bottle
from bottle import view


TEMPLATE_PATH.insert(0, './finances/views')
app = Bottle()


@app.route('/')
@view('index')
def index():
    return {
        'title': 'Hello!',
        'content': 'My first page',
    }


@app.get('/login')
def login():
    return '''
       <form action="/login" method="post">
           Username: <input name="username" type="text" />
           Password: <input name="password" type="password" />
           <input value="Login" type="submit" />
       </form>
    '''


@app.post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    return "<p>Your login information was correct. %s %s</p>" % (username, password)


@app.route('/static/<filepath:path>')
@app.route('/<filetype>/<filepath:path>')
def static(filepath, filetype=None):
    static_path = './finances/static'

    if filetype is not None:
        static_path += '/' + filetype

    return static_file(filepath, root=static_path)
