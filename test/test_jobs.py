import unittest
from mock import patch

from test_util import TEST_API_KEY, load_response
from zencoder import Zencoder

class TestJobs(unittest.TestCase):

    def setUp(self):
        self.zen = Zencoder(api_key=TEST_API_KEY)

    @patch("requests.Session.post")
    def test_job_create(self, post):
        post.return_value = load_response(201, 'fixtures/job_create.json')

        resp = self.zen.job.create('s3://zencodertesting/test.mov')

        self.assertEquals(resp.code, 201)
        self.assertTrue(resp.body['id'] > 0)
        self.assertEquals(len(resp.body['outputs']), 1)

    @patch("requests.Session.post")
    def test_job_create_list(self, post):
        post.return_value = load_response(201, 'fixtures/job_create_live.json')

        resp = self.zen.job.create(live_stream=True)

        self.assertEquals(resp.code, 201)
        self.assertTrue(resp.body['id'] > 0)
        self.assertEquals(len(resp.body['outputs']), 1)

    @patch("requests.Session.get")
    def test_job_details(self, get):
        get.return_value = load_response(200, 'fixtures/job_details.json')

        resp = self.zen.job.details(1234)
        self.assertEquals(resp.code, 200)
        self.assertTrue(resp.body['job']['id'] > 0)
        self.assertEquals(len(resp.body['job']['output_media_files']), 1)

    @patch("requests.Session.get")
    def test_job_progress(self, get):
        get.return_value = load_response(200, 'fixtures/job_progress.json')

        resp = self.zen.job.progress(12345)
        self.assertEquals(resp.code, 200)
        self.assertEquals(resp.body['state'], 'processing')

    @patch("requests.Session.put")
    def test_job_cancel(self, put):
        put.return_value = load_response(204)

        resp = self.zen.job.cancel(5555)
        self.assertEquals(resp.code, 204)
        self.assertEquals(resp.body, None)

    @patch("requests.Session.put")
    def test_job_resubmit(self, put):
        put.return_value = load_response(204)

        resp = self.zen.job.resubmit(5555)
        self.assertEquals(resp.code, 204)
        self.assertEquals(resp.body, None)

    @patch("requests.Session.get")
    def test_job_list(self, get):
        get.return_value = load_response(200, 'fixtures/job_list.json')

        resp = self.zen.job.list()
        self.assertEquals(resp.code, 200)
        self.assertEquals(len(resp.body), 3)

    @patch("requests.Session.get")
    def test_job_list_limit(self, get):
        get.return_value = load_response(200, 'fixtures/job_list_limit.json')

        resp = self.zen.job.list(per_page=1)
        self.assertEquals(resp.code, 200)
        self.assertEquals(len(resp.body), 1)

    @patch("requests.Session.put")
    def test_job_finish(self, put):
        put.return_value = load_response(204)

        resp = self.zen.job.finish(99999)
        self.assertEquals(resp.code, 204)

if __name__ == "__main__":
    unittest.main()

