"""
Main Zencoder module
"""
import os

class ZencoderError(Exception):
    pass

class Zencoder(object):
    """ Main class for pushing jobs to zencoder """
    def __init__(self, api_key=None):
        """ Initialize Zencoder """
        self.base_url = 'https://app.zencoder.com/api'
        if not api_key:
            try:
                self.api_key = os.environ['ZENCODER_API_KEY']
            except KeyError:
                raise ZencoderError('ZENCODER_API_KEY not set')
        else:
            self.api_key = api_key


