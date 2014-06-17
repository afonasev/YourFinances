
from nose.tools import eq_

from finances import controllers


def test_mistake403():
    eq_(
        controllers.mistake403(403),
        'The parameter you passed has the wrong format! ERROR 403',
    )


def test_mistake404():
    eq_(
        controllers.mistake404(404),
        'Sorry, this page does not exist! ERROR 404'
    )
