import unittest
from mock import patch

from test_util import TEST_API_KEY, load_response
from zencoder import Zencoder

class TestAccounts(unittest.TestCase):
    def setUp(self):
        self.zen = Zencoder(api_key=TEST_API_KEY)

    @patch("requests.Session.post")
    def test_account_create(self, post):
        post.return_value = load_response(201, 'fixtures/account_create.json')

        response = self.zen.account.create('test@example.com', tos=1)

        self.assertEquals(response.code, 201)
        self.assertEquals(response.body['password'], 'foo')
        self.assertEquals(response.body['api_key'], 'abcd1234')

    @patch("requests.Session.get")
    def test_account_details(self, get):
        get.return_value = load_response(200, 'fixtures/account_details.json')
        resp = self.zen.account.details()

        self.assertEquals(resp.code, 200)
        self.assertEquals(resp.body['account_state'], 'active')
        self.assertEquals(resp.body['minutes_used'], 12549)

    @patch("requests.Session.put")
    def test_account_integration(self, put):
        put.return_value = load_response(204)

        resp = self.zen.account.integration()

        self.assertEquals(resp.code, 204)
        self.assertEquals(resp.body, None)

    @patch("requests.Session.put")
    def test_account_live_unauthorized(self, put):
        put.return_value = load_response(402)

        resp = self.zen.account.live()
        self.assertEquals(resp.code, 402)

    @patch("requests.Session.put")
    def test_account_live_authorized(self, put):
        put.return_value = load_response(204)

        resp = self.zen.account.live()
        self.assertEquals(resp.code, 204)

if __name__ == "__main__":
    unittest.main()

