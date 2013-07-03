import unittest
import os
from zencoder import Zencoder
import zencoder

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

    def test_set_base_url(self):
        os.environ['ZENCODER_API_KEY'] = 'abcd123'
        zc = Zencoder(base_url='https://localhost:800/foo/')
        self.assertEquals(zc.base_url, 'https://localhost:800/foo/')

    def test_set_base_url_and_version_fails(self):
        os.environ['ZENCODER_API_KEY'] = 'abcd123'

        self.assertRaises(zencoder.core.ZencoderError,
                          Zencoder,
                          base_url='https://localhost:800/foo/',
                          api_version='v3')

    def test_set_timeout(self):
        api_key = 'testapikey'
        zc = Zencoder(api_key=api_key, timeout=999)

        self.assertEquals(zc.job.requests_params['timeout'], 999)

    def test_set_proxies(self):
        api_key = 'testapikey'
        proxies = {
            'https': 'https://10.10.1.10:1080'
        }
        zc = Zencoder(api_key=api_key, proxies=proxies)

        self.assertEquals(zc.job.requests_params['proxies'], proxies)

    def test_set_verify_false(self):
        api_key = 'testapikey'
        zc = Zencoder(api_key=api_key, verify=False)

        self.assertEquals(zc.job.requests_params['verify'], False)

    def test_set_cert_path(self):
        api_key = 'testapikey'
        cert = '/path/to/cert.pem'
        zc = Zencoder(api_key=api_key, cert=cert)

        self.assertEquals(zc.job.requests_params['cert'], cert)

if __name__ == "__main__":
    unittest.main()

