"""
Main Zencoder module
"""

import os
import json
import httplib2

class ZencoderError(Exception):
    pass

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

        # no caching set up
        self.http = httplib2.Http()

        self.as_xml = as_xml

    def get_jobs(self):
        url = self.base_url + 'jobs'
        url = '%s?api_key=%s' % (url, self.api_key)
        #data = urllib.urlencode({'api_key': self.api_key})

        request = urllib2.Request(url)

        response = urllib2.urlopen(request).read()
        if not self.as_xml:
            response = json.loads(response)

        return [Job(x) for x in response]

    def create_job(self, input):
        """ creates a zencoder job """
        url = self.base_url + 'jobs'
        data = json.dumps({"api_key":self.api_key, "input": input})

        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        req = self.http.request(url, method="POST", body=data,
                              headers=headers)

        return json.loads(req[-1])

class Response(object):
    """ Response object """
    pass

class Output(object):
    """ Output object """
    pass

class Job(object):
    """ Job object """
    def __init__(self, api_key):
        """
        Initialize a job object
        """
        pass

    def create(self, input, outputs=None, options=None):
        """
        Create a job
        """
        pass

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

