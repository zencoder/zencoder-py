import unittest
from mock import patch

from test_util import TEST_API_KEY, load_response
from zencoder import Zencoder

import datetime

class TestReports(unittest.TestCase):
    def setUp(self):
        self.zen = Zencoder(api_key=TEST_API_KEY)

    @patch("requests.Session.get")
    def test_reports_vod(self, get):
        get.return_value = load_response(200, 'fixtures/report_vod.json')

        resp = self.zen.report.vod()

        self.assertEquals(resp.code, 200)
        self.assertEquals(resp.body['total']['encoded_minutes'], 6)
        self.assertEquals(resp.body['total']['billable_minutes'], 8)

    @patch("requests.Session.get")
    def test_reports_live(self, get):
        get.return_value = load_response(200, 'fixtures/report_live.json')

        resp = self.zen.report.live()

        self.assertEquals(resp.code, 200)
        self.assertEquals(resp.body['total']['stream_hours'], 5)
        self.assertEquals(resp.body['total']['encoded_hours'], 5)
        self.assertEquals(resp.body['statistics']['length'], 5)

    @patch("requests.Session.get")
    def test_reports_all(self, get):
        get.return_value = load_response(200, 'fixtures/report_all.json')

        resp = self.zen.report.all()

        self.assertEquals(resp.code, 200)

        self.assertEquals(resp.body['total']['live']['stream_hours'], 5)
        self.assertEquals(resp.body['total']['live']['encoded_hours'], 5)
        self.assertEquals(resp.body['total']['vod']['encoded_minutes'], 6)
        self.assertEquals(resp.body['total']['vod']['billable_minutes'], 8)
        self.assertEquals(resp.body['statistics']['live']['length'], 2)

    @patch("requests.Session.get")
    def test_reports_all_date_filter(self, get):
        get.return_value = load_response(200, 'fixtures/report_all_date.json')

        start = datetime.date(2013, 5, 13)
        end = datetime.date(2013, 5, 13)
        resp = self.zen.report.all(start_date=start, end_date=end)

        self.assertEquals(resp.code, 200)

        self.assertEquals(resp.body['statistics']['vod'][0]['encoded_minutes'], 5)
        self.assertEquals(resp.body['statistics']['vod'][0]['billable_minutes'], 0)
        self.assertEquals(resp.body['statistics']['live'][0]['stream_hours'], 1)
        self.assertEquals(resp.body['statistics']['live'][0]['total_hours'], 2)

        self.assertEquals(resp.body['total']['vod']['encoded_minutes'], 5)
        self.assertEquals(resp.body['total']['vod']['billable_minutes'], 0)
        self.assertEquals(resp.body['total']['live']['stream_hours'], 1)
        self.assertEquals(resp.body['total']['live']['total_hours'], 2)

if __name__ == "__main__":
    unittest.main()

