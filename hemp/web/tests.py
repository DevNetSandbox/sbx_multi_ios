import app
import unittest


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_correct_http_response(self):
        resp = self.app.get('/')
        self.assertEquals(resp.status_code, 200)

    def test_correct_content(self):
        resp = self.app.get('/')
        self.assertEquals(resp.data, 'Hello, IMAPEX!')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()