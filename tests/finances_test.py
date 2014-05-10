
from nose.tools import eq_

import finances


def test_index():
    eq_(finances.index(), 'My first! app! By your name here')


def test_something():
    eq_(finances.something('Livi'), 'My first! app! By Livi')


def test_mistake404():
    eq_(finances.mistake404(404), 'Sorry, this page does not exist!')


def test_mistake403():
    eq_(finances.mistake403(403), 'The parameter you passed has the wrong format!')
