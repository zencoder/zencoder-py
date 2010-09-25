"""
Main Zencoder module
"""

import os
import json
import httplib2

class ZencoderError(Exception):
    pass

class HTTPBackend(object):
    """
    Abstracts out an HTTP backend, but defaults to httplib2

    @FIXME: Build in support for supplying arbitrary backends
    """
    def __init__(self, as_xml=False):
        """
        Creates an HTTPBackend object, which abstracts out some of the
        library specific HTTP stuff.
        """
        self.base_url = 'https://app.zencoder.com/api/'

        #TODO investigate httplib2 caching and if it is necessary
        self.http = httplib2.Http()
        self.as_xml = as_xml

        if self.as_xml:
            self.headers = {'Content-Type': 'application/xml',
                            'Accepts': 'application/xml'}
        else:
            self.headers = {'Content-Type': 'application/json',
                            'Accepts': 'application/json'}

    def encode(self, data):
        """
        Encodes data as either JSON or XML, so that it can be passed onto
        the Zencoder API
        """
        if not self.as_xml:
            return json.dumps(data)
        else:
            raise NotImplementedError('Encoding as XML is not supported.')

    def decode(self, raw_body):
        """
        Returns the raw_body as json (the default) or XML
        """
        if not self.as_xml:
            return json.loads(raw_body)

    def post(self, url, body=None):
        """
        Execute a HTTP POST request for the given URL
        """
        response, content = self.http.request(url, method="POST",
                                              body=body,
                                              headers=self.headers)

        return self.process(response, content)

    def process(self, http_response, content):
        """
        Returns HTTP backend agnostic Response data
        """
        code = http_response.status
        body = self.decode(content)
        response = Response(code, body, content, http_response)
        return response

class Zencoder(object):
    """ This is the entry point to the Zencoder API """
    def __init__(self, api_key=None, as_xml=False):
        """
        Initializes Zencoder. You must have a valid API_KEY.

        You can pass in the api_key as an argument, or set
        'ZENCODER_API_KEY' as an environment variable, and it will use
        that, if api_key is unspecified.

        Set as_xml=True to get back xml data instead of the default json.
        """
        self.base_url = 'https://app.zencoder.com/api/'
        if not api_key:
            try:
                self.api_key = os.environ['ZENCODER_API_KEY']
            except KeyError:
                raise ZencoderError('ZENCODER_API_KEY not set')
        else:
            self.api_key = api_key

        self.as_xml = as_xml
        self.job = Job(self.api_key, self.as_xml)
        self.account = Account(self.api_key, self.as_xml)
        self.notification = Notification(self.api_key, self.as_xml)
        self.output = Output(self.api_key, self.as_xml)

class Response(object):
    """ Response object """
    def __init__(self, code, body, raw_body, raw_response):
        self.code = code
        self.body = body
        self.raw_body = raw_body
        self.raw_response = raw_response

class Output(object):
    """ Output object """
    pass

class Job(HTTPBackend):
    """
    Contains all the methods that can be performed relating to Jobs with
    the Zencoder API
    """
    def __init__(self, api_key, as_xml=False):
        """
        Initialize a job object
        """
        super(Job, self).__init__()
        self.api_key = api_key
        self.as_xml = as_xml
        self.base_url = self.base_url + 'jobs'

    def create(self, input, outputs=None, options=None):
        """
        Create a job

        """
        data = {"api_key": self.api_key, "input": input}
        if outputs:
            data['outputs'] = outputs
        if options:
            data['options'] = options
        return self.post(self.base_url, body=self.encode(data))

    def list(self, page, per_page):
        """
        List some jobs
        """
        pass

    def details(self, job_id):
        """
        Get some job details
        """
        pass

    def resubmit(self, job_id):
        """
        Resubmits a job
        """
        pass

    def cancel(self, job_id):
        """
        Cancels a job
        """
        pass

    def delete(self, job_id):
        """
        Deletes a job
        """
        pass

class Notification(object):
    """ Notification object """
    pass

class Account(object):
    """ Account object """
    pass

