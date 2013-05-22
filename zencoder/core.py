import os
import requests
from datetime import datetime

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

__version__ = '0.6.3'

class ZencoderError(Exception):
    pass

class ZencoderResponseError(Exception):
    def __init__(self, http_response, content):
        self.http_response = http_response
        self.content = content

class HTTPBackend(object):
    """ Abstracts out an HTTP backend. Required argument are `base_url` and 
    `api_key`. """
    def __init__(self,
                 base_url,
                 api_key,
                 resource_name=None,
                 timeout=None,
                 test=False,
                 version=None):

        self.base_url = base_url

        if resource_name:
            self.base_url = self.base_url + resource_name

        self.http = requests.Session()

        self.api_key = api_key
        self.test = test
        self.version = version

        # sets request headers for the entire session
        self.http.headers.update(self.headers)

    @property
    def headers(self):
        """ Returns default headers, by setting the Content-Type, Accepts,
        User-Agent and API Key headers."""

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Zencoder-Api-Key': self.api_key,
            'User-Agent': 'zencoder-py v{0}'.format(__version__)
        }

        return headers

    def delete(self, url, params=None):
        """
        Executes an HTTP DELETE request for the given URL

        params should be a dictionary
        """
        response = self.http.delete(url, params=params)
        return self.process(response)

    def get(self, url, data=None):
        """
        Executes an HTTP GET request for the given URL

        data should be a dictionary of url parameters
        """
        response = self.http.get(url, headers=self.headers, params=data)
        return self.process(response)

    def post(self, url, body=None):
        """
        Executes an HTTP POST request for the given URL
        """
        response = self.http.post(url, data=body, headers=self.headers)

        return self.process(response)

    def put(self, url, data=None, body=None):
        """
        Executes an HTTP PUT request for the given URL
        """
        response = self.http.put(url, params=data, data=body, headers=self.headers)

        return self.process(response)

    def process(self, response):
        """ Returns HTTP backend agnostic Response data. """

        try:
            code = response.status_code

            # 204 - No Content
            if code == 204:
                body = None
            # add an error message to 402 errors
            elif code == 402:
                body = {
                    "message": "Payment Required",
                    "status": "error"
                }
            else:
                body = response.json()

            return Response(code, body, response.content, response)
        except ValueError:
            raise ZencoderResponseError(response, response.content)

class Zencoder(object):
    """ This is the entry point to the Zencoder API """
    def __init__(self, api_key=None, api_version=None, timeout=None, test=False):
        """
        Initializes Zencoder. You must have a valid `api_key`.

        You can pass in the api_key as an argument, or set
        `ZENCODER_API_KEY` as an environment variable, and it will use
        that, if `api_key` is unspecified.

        Set api_version='edge' to get the Zencoder development API. (defaults to 'v2')
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

        args = (self.base_url, self.api_key)
        kwargs = dict(timeout=timeout, test=self.test, version=api_version)
        self.job = Job(*args, **kwargs)
        self.account = Account(*args, **kwargs)
        self.output = Output(*args, **kwargs)
        self.input = Input(*args, **kwargs)
        self.report = None
        if api_version == 'v2':
            self.report = Report(*args, **kwargs)

class Response(object):
    """ The Response object stores the details of an API request. """
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

        return self.post(self.base_url, body=json.dumps(data))

    def details(self):
        """
        Gets your account details.
        """

        return self.get(self.base_url)

    def integration(self):
        """
        Puts your account into integration mode.
        """

        return self.put(self.base_url + '/integration')

    def live(self):
        """
        Puts your account into live mode.
        """
        return self.put(self.base_url + '/live')

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
        return self.get(self.base_url + '/%s/progress' % str(output_id))

    def details(self, output_id):
        """
        Gets the given output id's details
        """
        return self.get(self.base_url + '/%s' % str(output_id))

class Input(HTTPBackend):
    """ Returns information regarding inputs """
    def __init__(self, *args, **kwargs):
        """
        Contains all API methods relating to Inputs.
        """
        kwargs['resource_name'] = 'inputs'
        super(Input, self).__init__(*args, **kwargs)

    def progress(self, input_id):
        """
        Gets the given input id's progress.
        """
        return self.get(self.base_url + '/%s/progress' % str(input_id))

    def details(self, input_id):
        """
        Gets the given input id's details
        """
        return self.get(self.base_url + '/%s' % str(input))

class Job(HTTPBackend):
    """ Contains all API methods relating to transcoding Jobs. """
    def __init__(self, *args, **kwargs):
        """ Initializes a job object. """
        kwargs['resource_name'] = 'jobs'
        super(Job, self).__init__(*args, **kwargs)

    def create(self, input=None, live_stream=False, outputs=None, options=None):
        """
        Creates a transcoding job.

        @param input: the input url as string
        @param live_stream: starts a Live Stream job (input must be None)
        @param outputs: a list of output dictionaries
        @param options: a dictionary of job options
        """
        data = {"input": input, "test": self.test}
        if outputs:
            data['outputs'] = outputs

        if options:
            data.update(options)

        if live_stream:
            data['live_stream'] = live_stream

        return self.post(self.base_url, body=json.dumps(data))

    def list(self, page=1, per_page=50):
        """
        Lists some jobs.

        @param page: <int> the page of results to return
        @param per_page: <int> the number of results per page
        """
        data = {"page": page,
                "per_page": per_page}
        return self.get(self.base_url, data=data)

    def details(self, job_id):
        """
        Gets details for the given job
        """
        return self.get(self.base_url + '/%s' % str(job_id))

    def progress(self, job_id):
        return self.get(self.base_url + '/%s/progress' % str(job_id))

    def resubmit(self, job_id):
        """
        Resubmits the given `job_id`
        """
        url = self.base_url + '/%s/resubmit' % str(job_id)
        return self.put(url)

    def cancel(self, job_id):
        """
        Cancels the given `job_id`
        """
        if self.version == 'v1':
            verb = self.get
        else:
            verb = self.put

        url = self.base_url + '/%s/cancel' % str(job_id)
        return verb(url)

    def delete(self, job_id):
        """
        Deletes the given `job_id`

        WARNING: This method is aliased to `Job.cancel` -- it is deprecated in
                 API version 2 and greater.
        """
        return self.cancel(job_id)

    def finish(self, job_id):
        """ Finishes the live stream for `job_id`. """
        return self.put(self.base_url + '/%s/finish' % str(job_id))

class Report(HTTPBackend):
    def __init__(self, *args, **kwargs):
        """
        Contains all API methods relating to Reports.
        """
        kwargs['resource_name'] = 'reports'
        super(Report, self).__init__(*args, **kwargs)

    def __format(self, start_date=None, end_date=None, grouping=None):
        data = {'api_key': self.api_key}

        date_format = '%Y-%m-%d'
        if start_date:
            data['from'] = start_date.strftime(date_format)

        if end_date:
            data['to'] = end_date.strftime(date_format)

        if grouping:
            data['grouping'] = grouping

        return data

    def minutes(self, start_date=None, end_date=None, grouping=None):
        """
        Gets a detailed Report of encoded minutes and billable minutes for a 
        date range.

        **Warning**: `start_date` and `end_date` must be `datetime.date` objects.

        Example:
            import datetime
            start = datetime.date(2012, 12, 31)
            end = datetime.today()
            data = z.report.minutes(start, end)

        @param start_date: Start date of report (If not submitted,
            API defaults to 30 days ago)
        @param end_date: End date of report (If not submitted, API defaults to
            yesterday)
        @param grouping: Minute usage for only one report grouping
        """

        data = self.__format(start_date, end_date)

        url = self.base_url + '/minutes'
        return self.get(url, data=data)

    def vod(self, start_date=None, end_date=None, grouping=None):
        """ Gets a report of VOD Usage """
        data = self.__format(start_date, end_date, grouping)

        url = self.base_url + '/vod'
        return self.get(url, data=data)

    def live(self, start_date=None, end_date=None, grouping=None):
        """ Gets a report of Live Usage """
        data = self.__format(start_date, end_date, grouping)

        url = self.base_url + '/live'
        return self.get(url, data=data)

    def all(self, start_date=None, end_date=None, grouping=None):
        """ Gets a report of both VOD and Live Usage """
        data = self.__format(start_date, end_date, grouping)

        url = self.base_url + '/all'
        return self.get(url, data=data)

