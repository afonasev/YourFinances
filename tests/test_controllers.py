
from webtest import TestApp

from finances import app


class TestFinances():
    test_case = {
        'data': {
            'login': 'user',
            'password': 'password',
            'site': 'yandex.ru',
            'length': 10,
        },
        'result': '0E8f1Ae2Cb',
        'result_when_ignore': '7D4e7Da2C3',
    }

    def setUp(self):
        self.app = TestApp(app)

    def test_page_not_found(self):
        msg = 'Page not found!'
        assert msg in self.app.get('/smt_page').data.decode()
