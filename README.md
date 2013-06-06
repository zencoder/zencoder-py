
Zencoder
--------

[![Build Status](https://travis-ci.org/zencoder/zencoder-py.png?branch=master)](https://travis-ci.org/zencoder/zencoder-py)

A Python module for interacting with the [Zencoder](http://zencoder.com) API.

### Getting Started

Install from PyPI

    $ pip install zencoder

Import zencoder

```python
from zencoder import Zencoder
```

Create an instance of the Zencoder client. This will accept an API key and version. If not API key is set, it will look for a `ZENCODER_API_KEY` environment variable. API version defaults to 'v2'.

    # If you want to specify an API key when creating a client
    client = Zencoder('API_KEY')

    # If you have the environment variable set
    client = Zencoder()

## [Jobs](https://app.zencoder.com/docs/api/jobs)

There's more you can do on jobs than anything else in the API. The following methods are available: `list`, `create`, `details`, `progress`, `resubmit`, `cancel`, `delete`.

Create a [new job](https://app.zencoder.com/docs/api/jobs/create).

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

[List jobs](https://app.zencoder.com/docs/api/jobs/list).

By default the jobs listing is paginated with 50 jobs per page and sorted by ID in descending order. You can pass two parameters to control the paging: `page` and `per_page`.

```python
zen.job.list(per_page=10)
zen.job.list(per_page=10, page=2)
```

Get [details](https://app.zencoder.com/docs/api/jobs/show) about a job.

The number passed to `details` is the ID of a Zencoder job.

```python
zen.job.details(1)
```

Get [progress](https://app.zencoder.com/docs/api/jobs/progress) on a job.

The number passed to `progress` is the ID of a Zencoder job.

```python
zen.job.progress(1)
```

[Resubmit](https://app.zencoder.com/docs/api/jobs/resubmit) a job

The number passed to `resubmit` is the ID of a Zencoder job.

```python
zen.job.resubmit(1)
```

[Cancel](https://app.zencoder.com/docs/api/jobs/cancel) a job

The number passed to `cancel` is the ID of a Zencoder job.

```python
zen.job.cancel(1)
```

### delete

The number passed to `delete` is the ID of a Zencoder job.

```python
zen.job.delete(1)
```

## [Inputs](https://app.zencoder.com/docs/api/inputs)

Get [details](https://app.zencoder.com/docs/api/inputs/show) about an input.

The number passed to `details` is the ID of a Zencoder job.

```python
zen.input.details(1)
```

Get [progress](https://app.zencoder.com/docs/api/inputs/progress) for an input.

The number passed to `progress` is the ID of a Zencoder job.

```python
zen.input.progress(1)
```

## [Outputs](https://app.zencoder.com/docs/api/outputs)

Get [details](https://app.zencoder.com/docs/api/outputs/show) about an output.

The number passed to `details` is the ID of a Zencoder job.

```python
zen.output.details(1)
```

Get [progress](https://app.zencoder.com/docs/api/outputs/progress) for an output.

The number passed to `progress` is the ID of a Zencoder job.

```python
zen.output.progress(1)
```

## [Reports](https://app.zencoder.com/docs/api/reports)

Reports are great for getting usage data for your account. All default to 30 days from yesterday with no [grouping](https://app.zencoder.com/docs/api/encoding/job/grouping), but this can be altered. These will return `422 Unprocessable Entity` if the date format is incorrect or the range is greater than 2 months. 

Get [all usage](https://app.zencoder.com/docs/api/reports/all) (Live + VOD).

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

Get [VOD usage](https://app.zencoder.com/docs/api/reports/vod).

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

Get [Live usage](https://app.zencoder.com/docs/api/reports/live).

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

## [Accounts](https://app.zencoder.com/docs/api/accounts)

Create a [new account](https://app.zencoder.com/docs/api/accounts/create). A unique email address and terms of service are required, but you can also specify a password (and confirmation) along with whether or not you want to subscribe to the Zencoder newsletter. New accounts will be created under the Test (Free) plan.

No API Key is required.

```python
zen.account.create('foo@example.com', tos=1)
zen.account.create('foo@example.com', tos=1,
                   options={'password': 'abcd1234',
                            'affiliate_code': 'foo'})
```

Get [details](https://app.zencoder.com/docs/api/accounts/show) about the current account.

```python
zen.account.details()
```

Turn [integration mode](https://app.zencoder.com/docs/api/accounts/integration) on (all jobs are test jobs).

```python
zen.account.integration()
```

Turn off integration mode, which means your account is live (and you'll be billed for jobs).

```python
zen.account.live()
```
## Tests

The tests use the `mock` library to stub in response data from the API. Run tests individually:

    $ python test/test_jobs.py

Or use `nose`:

    $ nosetests

