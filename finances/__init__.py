
import bottle


index_html = 'My first! app! By {{ author }}'


@bottle.route('/:anything')
def something(anything=''):
    return bottle.template(index_html, author=anything)


@bottle.route('/')
def index():
    return bottle.template(index_html, author='your name here')


@bottle.error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format!'


@bottle.error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


app = bottle.default_app()
