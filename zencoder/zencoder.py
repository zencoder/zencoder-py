"""
Main Zencoder module
"""

import os
import httplib2
from urllib import urlencode

# Note: I've seen this pattern for dealing with json in different versions of
# python in a lot of modules -- if there's a better way, I'd love to use it.
try:
    # python 2.6 and greater
    import json
except ImportError:
    try:
        # python 2.5
        import simplejson
        json = simplejson
    except ImportError:
        # if we're in django or Google AppEngine land
        # use this as a last resort
        from django.utils import simplejson
        json = simplejson

class ZencoderError(Exception):
    pass

class HTTPBackend(object):
    """
    Abstracts out an HTTP backend, but defaults to httplib2

    @FIXME: Build in support for supplying arbitrary backends
    """
    def __init__(self, api_key, as_xml=False, resource_name=None):
        """
        Creates an HTTPBackend object, which abstracts out some of the
        library specific HTTP stuff.
        """
        self.base_url = 'https://app.zencoder.com/api/'
        if resource_name:
            self.base_url = self.base_url + resource_name

        #TODO investigate httplib2 caching and if it is necessary
        self.http = httplib2.Http()
        self.as_xml = as_xml
        self.api_key = api_key

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
            # only parse json when it exists, else just return None
            if not raw_body or raw_body == ' ':
                return None
            else:
                return json.loads(raw_body)

    def post(self, url, body=None):
        """
        Executes an HTTP POST request for the given URL
        """
        response, content = self.http.request(url, method="POST",
                                              body=body,
                                              headers=self.headers)

        return self.process(response, content)

    def get(self, url, params=None):
        """
        Executes an HTTP GET request for the given URL

        params should be a urllib.urlencoded string
        """
        if params:
            url = '?'.join([url, params])

        response, content = self.http.request(url, method="GET",
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
        self.output = Output(self.api_key, self.as_xml)

class Response(object):
    """ Response object """
    def __init__(self, code, body, raw_body, raw_response):
        self.code = code
        self.body = body
        self.raw_body = raw_body
        self.raw_response = raw_response

class Output(HTTPBackend):
    """ Gets information regarding outputs """
    def __init__(self, api_key, as_xml=False):
        """
        Contains all API methods relating to Outputs.
        """
        super(Output, self).__init__(api_key, as_xml, 'outputs')

    def progress(self, output_id):
        """
        Gets the given output id's progress.
        """
        data = {'api_key': self.api_key}
        return self.get(self.base_url + '/%s/progress' % str(output_id),
                        params=urlencode(data))

class Job(HTTPBackend):
    """
    Contains all API methods relating to transcoding Jobs.
    """
    def __init__(self, api_key, as_xml=False):
        """
        Initialize a job object
        """
        super(Job, self).__init__(api_key, as_xml, 'jobs')

    def create(self, input, outputs=None, options=None):
        """
        Create a job

        @param input: the input url as string
        @param outputs: a list of output dictionaries
        @param options: a dictionary of job options
        """
        data = {"api_key": self.api_key, "input": input}
        if outputs:
            data['outputs'] = outputs

        if options:
            data.update(options)

        return self.post(self.base_url, body=self.encode(data))

    def list(self, page=1, per_page=50):
        """
        List some jobs
        """
        data = {"api_key": self.api_key,
                "page": page,
                "per_page": per_page}
        return self.get(self.base_url, params=urlencode(data))

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

class Account(HTTPBackend):
    """ Account object """
    def __init__(self, api_key=None, as_xml=False):
        """
        Initializes an Account object
        """
        super(Account, self).__init__(api_key, as_xml, 'account')

    def create(self, email, tos=True, options=None):
        """
        Creates an account with Zencoder, no API Key necessary.
        """
        data = {'email': email,
                'terms_of_service': int(tos)}
        if options:
            data.update(options)

        return self.post(self.base_url, body=self.encode(data))

    def details(self):
        """
        Gets your account details.
        """
        data = {'api_key': self.api_key}

        return self.get(self.base_url, params=urlencode(data))

    def integration(self):
        """
        Puts your account into integration mode.
        """
        data = {'api_key': self.api_key}

        return self.get(self.base_url + '/integration',
                        params=urlencode(data))

    def live(self):
        """
        Puts your account into live mode."
        """
        data = {'api_key': self.api_key}

        return self.get(self.base_url + '/live',
                        params=urlencode(data))

