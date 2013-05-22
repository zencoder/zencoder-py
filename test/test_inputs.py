import unittest
from zencoder import Zencoder

from mock import patch

from test_util import TEST_API_KEY, load_response
from zencoder import Zencoder

class TestInputs(unittest.TestCase):
    def setUp(self):
        self.zen = Zencoder(api_key=TEST_API_KEY)

    @patch("requests.Session.get")
    def test_input_details(self, get):
        get.return_value = load_response(200, 'fixtures/input_details.json')

        resp = self.zen.input.details(15432)
        self.assertEquals(resp.code, 200)
        self.assertTrue(resp.body['id'] > 0)

    @patch("requests.Session.get")
    def test_input_progress(self, get):
        get.return_value = load_response(200, 'fixtures/input_progress.json')

        resp = self.zen.input.progress(14325)
        self.assertEquals(resp.code, 200)
        self.assertEquals(resp.body['state'], 'processing')

if __name__ == "__main__":
    unittest.main()

