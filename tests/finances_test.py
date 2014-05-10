
from nose.tools import eq_

import finances


def test_finances_square():
    eq_(finances.square(3), 9)


def test_finances_square2():
    eq_(finances.square(2), 4)
