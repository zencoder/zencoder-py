# Zencoder
[![Build Status](https://travis-ci.org/zencoder/zencoder-py.png?branch=master)](https://travis-ci.org/zencoder/zencoder-py)

A Python module for the [Zencoder](http://zencoder.com) API.

## Installation
Install from PyPI using `pip`.

    pip install zencoder

## Dependencies
`zencoder-py` depends on [requests](http://python-requests.org), and uses the `json` or `simplejson` module.

## Usage

### Create an instance of `Zencoder`

    from zencoder import Zencoder
    zen = Zencoder('abc123') # enter your api key

### Submit a job

    # creates an encoding job with the defaults
    job = zen.job.create('http://input-file/movie.avi')
    print job.code
    print job.body
    print job.body['id']

### Return output progress

    # get the transcode progress of the first output
    progress = zen.output.progress(job.body['outputs'][0]['id'])
    print progress.body

### Create a new job with multiple outputs

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

### ZENCODER_API_KEY Environment Variable

```python
import os
os.environ['ZENCODER_API_KEY'] = 'abcd1234'
zen = Zencoder()
```

If you set `ZENCODER_API_KEY` to your API Key, you don't have to provide it when initializing Zencoder.

## Specifying the API Version
Set the version of the Zencoder API you want to use as the `api_version` keyword to the `Zencoder` object (defaults to `v2`):

```python
# set to version 1: https://app.zencoder.com/api/v1/
zen = Zencoder(api_version='v1')

# set to the edge version: https://app.zencoder.com/api/
zen = Zencoder(api_version='edge')
```

## Jobs

There's more you can do on jobs than anything else in the API. The following methods are available: `list`, `create`, `details`, `progress`, `resubmit`, `cancel`, `delete`.

### create

```python
zen.job.create('s3://bucket/key.mp4')
zen.job.create('s3://bucket/key.mp4',
               outputs=[{'label': 'vp8 for the web',
                         'url': 's3://bucket/key_output.webm'}])
```

This returns a `zencoder.Response` object. The body includes a Job ID, and one or more Output IDs (one for every output file created).

```python
response = zen.job.create('s3://bucket/key.mp4')
response.code           # 201
response.body['id']     # 12345
```

### list

By default the jobs listing is paginated with 50 jobs per page and sorted by ID in descending order. You can pass two parameters to control the paging: `page` and `per_page`.

```python
zen.job.list(per_page=10)
zen.job.list(per_page=10, page=2)
```

### details

The number passed to `details` is the ID of a Zencoder job.

```python
zen.job.details(1)
```

### progress

The number passed to `progress` is the ID of a Zencoder job.

```python
zen.job.progress(1)
```

### resubmit

The number passed to `resubmit` is the ID of a Zencoder job.

```python
zen.job.resubmit(1)
```

### cancel

The number passed to `cancel` is the ID of a Zencoder job.

```python
zen.job.cancel(1)
```

### delete

The number passed to `delete` is the ID of a Zencoder job.

```python
zen.job.delete(1)
```

## Inputs

### details

The number passed to `details` is the ID of a Zencoder job.

```python
zen.input.details(1)
```

### progress

The number passed to `progress` is the ID of a Zencoder job.

```python
zen.input.progress(1)
```

## Outputs

### details

The number passed to `details` is the ID of a Zencoder job.

```python
zen.output.details(1)
```

### progress

The number passed to `progress` is the ID of a Zencoder job.

```python
zen.output.progress(1)
```

## Accounts

### create

No API Key is required.

```python
zen.account.create('foo@example.com', tos=1)
zen.account.create('foo@example.com', tos=1,
                   options={'password': 'abcd1234',
                            'affiliate_code': 'foo'})
```

### details

```python
zen.account.details()
```

### integration

This will put your account into integration mode (site-wide).

```python
zen.account.integration()
```

### live

This will put your account into live mode (site-wide).

```python
zen.account.live()
```

## Reports

### minutes

This will list the minutes used for your account within a certain, configurable range.

```python
import datetime
zen.report.minutes()
zen.report.minutes(grouping="foo")
zen.report.minutes(start_date=datetime.date(2011, 10, 30),
                   end_date=datetime.date(2011, 11, 24))
zen.report.minutes(start_date=datetime.date(2011, 10, 30),
                   end_date=datetime.date(2011, 11, 24),
                   grouping="foo")
```

### vod

This will list the VOD minutes used for your account.

```python
import datetime
zen.report.vod()
zen.report.vod(grouping="foo")
zen.report.vod(start_date=datetime.date(2011, 10, 30),
               end_date=datetime.date(2011, 11, 24))
zen.report.vod(start_date=datetime.date(2011, 10, 30),
               end_date=datetime.date(2011, 11, 24),
               grouping="foo")
```

### live

This will list the Live transcoding minutes used for your account.

```python
import datetime
zen.report.live()
zen.report.live(grouping="foo")
zen.report.live(start_date=datetime.date(2011, 10, 30),
                end_date=datetime.date(2011, 11, 24))
zen.report.live(start_date=datetime.date(2011, 10, 30),
                end_date=datetime.date(2011, 11, 24),
                grouping="foo")
```

### all

This will list all of the transcoding minutes used for your account.

```python
import datetime
zen.report.all()
zen.report.all(grouping="foo")
zen.report.all(start_date=datetime.date(2011, 10, 30),
                end_date=datetime.date(2011, 11, 24))
zen.report.all(start_date=datetime.date(2011, 10, 30),
                end_date=datetime.date(2011, 11, 24),
                grouping="foo")
```

## Documentation
Docs are in progress, and hosted at Read the Docs: http://zencoder.rtfd.org

## Contributors
 * [Senko Rasic](http://github.com/senko)
 * [Josh Kennedy](http://github.com/kennedyj)
 * [Issac Kelly](http://github.com/issackelly)


