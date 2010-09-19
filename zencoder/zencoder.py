"""
Main Zencoder module
"""
import os

class ZencoderError(Exception):
    pass

class Zencoder(object):
    base_url = 'https://app.zencoder.com/api'

    def __init__(self, api_key=None):
        """ Initialize Zencoder """
        if not api_key:
            try:
                self.api_key = os.environ['ZENCODER_API_KEY']
            except KeyError:
                raise ZencoderError('ZENCODER_API_KEY not set')
        else:
            self.api_key = api_key


