import unittest
import os
from zencoder import Zencoder

class TestZencoder(unittest.TestCase):
    def setUp(self):
        """ Initialize Zencoder for testing """
        pass

    def test_api_key(self):
        """ initialize zencoder object and test api key """
        api_key = 'testapikey'
        zc = Zencoder(api_key=api_key)
        self.assertEquals(zc.api_key, api_key)

    def test_api_key_env_var(self):
        """ tests the ZENOCODER_API_KEY environment var """
        os.environ['ZENCODER_API_KEY'] = 'abcd123'
        zc = Zencoder()
        self.assertEquals(zc.api_key, 'abcd123')

    def test_default_api_version(self):
        os.environ['ZENCODER_API_KEY'] = 'abcd123'
        zc = Zencoder()
        self.assertEquals(zc.base_url, 'https://app.zencoder.com/api/v2/')

    def test_set_api_version(self):
        os.environ['ZENCODER_API_KEY'] = 'abcd123'
        zc = Zencoder(api_version='v1')
        self.assertEquals(zc.base_url, 'https://app.zencoder.com/api/v1/')

    def test_set_api_edge_version(self):
        os.environ['ZENCODER_API_KEY'] = 'abcd123'
        zc = Zencoder(api_version='edge')
        self.assertEquals(zc.base_url, 'https://app.zencoder.com/api/')

    def test_zero_content_length(self):
        os.environ['ZENCODER_API_KEY'] = 'abcd123'
        zc = Zencoder()
        content = None
        self.assertEquals(zc.job.content_length(content), "0")

    def test_zero_content_length(self):
        os.environ['ZENCODER_API_KEY'] = 'abcd123'
        zc = Zencoder()
        content = "foobar"
        self.assertEquals(zc.job.content_length(content), "6")

if __name__ == "__main__":
    unittest.main()

