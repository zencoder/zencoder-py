# Zencoder
[![Build Status](https://secure.travis-ci.org/schworer/zencoder-py.png)](http://travis-ci.org/schworer/zencoder-py)

A Python module for the [Zencoder](http://zencoder.com) API.

## Installation
Install from PyPI using `easy_install` or `pip`.

    pip install zencoder

## Dependencies
`zencoder-py` depends on [requests](http://python-requests.org), and uses the `json` or `simplejson` module.

## Usage

    from zencoder import Zencoder
    zen = Zencoder('abc123') # enter your api key

    # creates an encoding job with the defaults
    job = zen.job.create('http://input-file/movie.avi')
    print job.code
    print job.body
    print job.body['id']

    # get the transcode progress of the first output
    progress = zen.output.progress(job.body['outputs'][0]['id'])
    print progress.body


    # configure your outputs with dictionaries
    iphone = {
                 'label': 'iPhone',
                 'url': 's3://output-bucket/output-file-1.mp4',
                 'width': 480,
                 'height': 320
             }
    web = {
              'label': 'web',
              'url': 's3://output-bucket/output-file.vp8',
              'video_codec':, 'vp8'
          }
    # the outputs kwarg requires an iterable
    outputs = (iphone, web)
    another_job = zen.job.create(input_url, outputs=outputs)

**Note:** If you set the `ZENCODER_API_KEY` environment variable to your api key, you don't have to provide it when initializing Zencoder.

## Specifying the API Version
Set the version of the Zencoder API you want to use as the `api_version` keyword to the `Zencoder` object (defaults to `v2`):

```python
# set to version 1: https://app.zencoder.com/api/v1/
zen = Zencoder(api_version='v1')

# set to the edge version: https://app.zencoder.com/api/
zen = Zencoder(api_version='edge')
```
## Documentation
Docs are in progress, and hosted at Read the Docs: http://zencoder.rtfd.org

## Contributors
 * [Senko Rasic](http://github.com/senko)
 * [Josh Kennedy](http://github.com/kennedyj)
 * [Issac Kelly](http://github.com/issackelly)


