"""
Main Zencoder module
"""

class Zencoder(object):
    base_url = 'https://app.zencoder.com/api'
    def __init__(self, api_key):
        """ Initialize Zencoder """
        self.api_key = api_key

