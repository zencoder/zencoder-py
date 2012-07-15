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

class ZencoderResponseError(Exception):
    def __init__(self, http_response, content):
        self.http_response = http_response
        self.content = content

class HTTPBackend(object):
    """
    Abstracts out an HTTP backend, but defaults to httplib2

    @FIXME: Build in support for supplying arbitrary backends
    """
    def __init__(self, base_url, api_key, as_xml=False, resource_name=None, timeout=None, test=False, version=None):
        """
        Creates an HTTPBackend object, which abstracts out some of the
        library specific HTTP stuff.
        """
        self.base_url = base_url
        if resource_name:
            self.base_url = self.base_url + resource_name

        self.http = httplib2.Http(timeout=timeout)
        self.as_xml = as_xml
        self.api_key = api_key
        self.test = test
        self.version = version

    def content_length(self, body):
        """
        Returns the content length as an int for the given body data
        """
        return str(len(body)) if body else "0"

    @property
    def headers(self):
        if self.as_xml:
            return {'Content-Type': 'application/xml',
                    'Accepts': 'application/xml'}
        else:
            return {'Content-Type': 'application/json',
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
        else:
            raise NotImplementedError('Decoding as XML is not supported.')

    def delete(self, url, params=None):
        """
        Executes an HTTP DELETE request for the given URL

        params should be a urllib.urlencoded string
        """
        if params:
            url = '?'.join([url, params])

        response, content = self.http.request(url, method="DELETE",
                                              headers=self.headers)
        return self.process(response, content)

    def get(self, url, data=None):
        """
        Executes an HTTP GET request for the given URL

        data should be a dictionary of url parameters
        """
        if data:
            params = urlencode(data)
            url = '?'.join([url, params])

        response, content = self.http.request(url, method="GET",
                                              headers=self.headers)
        return self.process(response, content)

    def post(self, url, body=None):
        """
        Executes an HTTP POST request for the given URL
        """
        headers = self.headers
        headers['Content-Length'] = self.content_length(body)
        response, content = self.http.request(url, method="POST",
                                              body=body,
                                              headers=self.headers)

        return self.process(response, content)

    def put(self, url, data=None, body=None):
        """
        Executes an HTTP PUT request for the given URL
        """
        headers = self.headers
        headers['Content-Length'] = self.content_length(body)

        if data:
            params = urlencode(data)
            url = '?'.join([url, params])

        response, content = self.http.request(url, method="PUT",
                                              body=body,
                                              headers=headers)

        return self.process(response, content)

    def process(self, http_response, content):
        """
        Returns HTTP backend agnostic Response data
        """

        try:
            code = http_response.status
            body = self.decode(content)
            response = Response(code, body, content, http_response)

            return response

        except ValueError:
            raise ZencoderResponseError(http_response, content)

class Zencoder(object):
    """ This is the entry point to the Zencoder API """
    def __init__(self, api_key=None, api_version=None, as_xml=False, timeout=None, test=False):
        """
        Initializes Zencoder. You must have a valid API_KEY.

        You can pass in the api_key as an argument, or set
        `ZENCODER_API_KEY` as an environment variable, and it will use
        that, if api_key is unspecified.

        Set api_version='edge' to get the Zencoder development API. (defaults to 'v2')
        Set as_xml=True to get back xml data instead of the default json.
        """
        if not api_version:
            api_version = 'v2'

        self.base_url = 'https://app.zencoder.com/api/'
        if not api_version == 'edge':
            self.base_url = self.base_url + '%s/' % api_version

        if not api_key:
            try:
                self.api_key = os.environ['ZENCODER_API_KEY']
            except KeyError:
                raise ZencoderError('ZENCODER_API_KEY not set')
        else:
            self.api_key = api_key

        self.test = test
        self.as_xml = as_xml

        args = (self.base_url, self.api_key, self.as_xml)
        kwargs = dict(timeout=timeout, test=self.test, version=api_version)
        self.job = Job(*args, **kwargs)
        self.account = Account(*args, **kwargs)
        self.output = Output(*args, **kwargs)

class Response(object):
    """
    The Response object stores the details of an API request in an XML/JSON
    agnostic way.
    """
    def __init__(self, code, body, raw_body, raw_response):
        self.code = code
        self.body = body
        self.raw_body = raw_body
        self.raw_response = raw_response

class Account(HTTPBackend):
    """ Account object """
    def __init__(self, *args, **kwargs):
        """
        Initializes an Account object
        """
        kwargs['resource_name'] = 'account'
        super(Account, self).__init__(*args, **kwargs)

    def create(self, email, tos=1, options=None):
        """
        Creates an account with Zencoder, no API Key necessary.
        """
        data = {'email': email,
                'terms_of_service': str(tos)}
        if options:
            data.update(options)

        return self.post(self.base_url, body=self.encode(data))

    def details(self):
        """
        Gets your account details.
        """
        data = {'api_key': self.api_key}

        return self.get(self.base_url, data=data)

    def integration(self):
        """
        Puts your account into integration mode.
        """
        data = {'api_key': self.api_key}

        return self.get(self.base_url + '/integration', data=data)

    def live(self):
        """
        Puts your account into live mode.
        """
        data = {'api_key': self.api_key}

        return self.get(self.base_url + '/live', data=data)

class Output(HTTPBackend):
    """ Gets information regarding outputs """
    def __init__(self, *args, **kwargs):
        """
        Contains all API methods relating to Outputs.
        """
        kwargs['resource_name'] = 'outputs'
        super(Output, self).__init__(*args, **kwargs)

    def progress(self, output_id):
        """
        Gets the given output id's progress.
        """
        data = {'api_key': self.api_key}
        return self.get(self.base_url + '/%s/progress' % str(output_id),
                        data=data)

    def details(self, output_id):
        """
        Gets the given output id's details
        """
        data = {'api_key': self.api_key}
        return self.get(self.base_url + '/%s' % str(output_id),
                        data=data)

class Job(HTTPBackend):
    """
    Contains all API methods relating to transcoding Jobs.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a job object
        """
        kwargs['resource_name'] = 'jobs'
        super(Job, self).__init__(*args, **kwargs)

    def create(self, input, outputs=None, options=None):
        """
        Creates a job

        @param input: the input url as string
        @param outputs: a list of output dictionaries
        @param options: a dictionary of job options
        """
        as_test = int(self.test)

        data = {"api_key": self.api_key, "input": input, "test": as_test}
        if outputs:
            data['outputs'] = outputs

        if options:
            data.update(options)

        return self.post(self.base_url, body=self.encode(data))

    def list(self, page=1, per_page=50):
        """
        Lists some jobs.

        @param page: <int> the page of results to return
        @param per_page: <int> the number of results per page
        """
        data = {"api_key": self.api_key,
                "page": page,
                "per_page": per_page}
        return self.get(self.base_url, data=data)

    def details(self, job_id):
        """
        Gets details for the given job
        """
        data = {'api_key': self.api_key}
        return self.get(self.base_url + '/%s' % str(job_id), data=data)

    def progress(self, job_id):
        data = {'api_key': self.api_key}
        return self.get(self.base_url + '/%s/progress' % str(job_id), data=data)

    def resubmit(self, job_id):
        """
        Resubmits the given `job_id`
        """
        data = {'api_key': self.api_key}
        url = self.base_url + '/%s/resubmit' % str(job_id)
        return self.put(url, data=data)

    def cancel(self, job_id):
        """
        Cancels the given `job_id`
        """
        if self.version == 'v1':
            verb = self.get
        else:
            verb = self.put

        data = {'api_key': self.api_key}
        url = self.base_url + '/%s/cancel' % str(job_id)
        return verb(url, data=data)

    def delete(self, job_id):
        """
        Deletes the given `job_id`

        WARNING: This method is aliased to `Job.cancel` -- it is deprecated in
                 API version 2 and greater.
        """
        return self.cancel(job_id)

