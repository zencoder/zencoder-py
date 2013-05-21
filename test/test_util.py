from collections import namedtuple
import json
import os

TEST_API_KEY = 'abcd123'

MockResponse = namedtuple("Response", "status_code, json, content")

CUR_DIR = os.path.split(__file__)[0]

def load_response(code, fixture=None):
    if fixture:
        with open(os.path.join(CUR_DIR, fixture), 'r') as f:
            content = f.read()
    else:
        content = None

    return MockResponse(code, lambda: json.loads(content), content)

