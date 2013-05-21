import unittest
from zencoder import Zencoder

from mock import patch

from test_util import TEST_API_KEY, load_response
from zencoder import Zencoder

class TestOutputs(unittest.TestCase):
    def setUp(self):
        self.zen = Zencoder(api_key=TEST_API_KEY)

    @patch("requests.Session.get")
    def test_output_details(self, get):
        get.return_value = load_response(200, 'fixtures/output_details.json')

        resp = self.zen.output.details(22222)
        self.assertEquals(resp.code, 200)
        self.assertTrue(resp.body['id'] > 0)

    @patch("requests.Session.get")
    def test_output_progress(self, get):
        get.return_value = load_response(200, 'fixtures/output_progress.json')

        resp = self.zen.output.progress(123456)
        self.assertEquals(resp.code, 200)
        self.assertEquals(resp.body['state'], 'processing')

if __name__ == "__main__":
    unittest.main()

