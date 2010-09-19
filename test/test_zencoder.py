import unittest
from zencoder import Zencoder

class TestZencoder(unittest.TestCase):
    def setUp(self):
        """ Initialize Zencoder for testing """
        pass

    def test_api_key(self):
        """ initialize zencoder object and test api key """
        api_key = 'abcd123'
        zc = Zencoder(api_key=api_key)
        self.assertEquals(zc.api_key, api_key)

if __name__ == "__main__":
    unittest.main()

