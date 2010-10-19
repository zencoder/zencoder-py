# Zencoder

A Python module for the [Zencoder](http://zencoder.com) API

## Installation
Eventually I'll get around to putting this in the cheeseshop, when that happens you can install with easy_install:
    easy_install zencoder
or with pip:
    pip install zencoder

## Dependencies
zencoder-py depends on [httplib2](http://code.google.com/p/httplib2/), and uses the json module and will depend on some package for xml when I get around to supporting it.

Install httplib2 with pip or easy_install.

## Usage

    from zencoder import Zencoder
    zen = Zencoder('abc123')

    # creates an encoding job with the defaults
    response = zen.job.create('http://input-file/movie.avi')
    print response.code
    print response.body
    print response.body['id']

**Note:** If you set the **ZENCODER\_API\_KEY** environment variable to your api key, you don't have to provide it when initializing Zencoder.

