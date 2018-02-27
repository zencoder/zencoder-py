
Zencoder
--------

[![Build Status](https://travis-ci.org/zencoder/zencoder-py.svg?branch=master)](https://travis-ci.org/zencoder/zencoder-py)

A Python module for interacting with the [Zencoder](http://zencoder.com) API.

### Getting Started

Install from PyPI

    $ pip install zencoder

Import zencoder

```python
from zencoder import Zencoder
```

Create an instance of the Zencoder client. This will accept an API key and version. If not API key is set, it will look for a `ZENCODER_API_KEY` environment variable. API version defaults to 'v2'.

```python
# If you want to specify an API key when creating a client
client = Zencoder('API_KEY')

# If you have the environment variable set
client = Zencoder()
```

## [Jobs](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Jobs)

Create a [new job](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Jobs-Create_a_Job).

```python
client.job.create('s3://bucket/key.mp4')
client.job.create('s3://bucket/key.mp4',
               outputs=[{'label': 'vp8 for the web',
                         'url': 's3://bucket/key_output.webm'}])
```

This returns a `zencoder.Response` object. The body includes a Job ID, and one or more Output IDs (one for every output file created).

```python
response = client.job.create('s3://bucket/key.mp4')
response.code           # 201
response.body['id']     # 12345
```

[List jobs](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Jobs-List_Jobs).

By default the jobs listing is paginated with 50 jobs per page and sorted by ID in descending order. You can pass two parameters to control the paging: `page` and `per_page`.

```python
client.job.list(per_page=10)
client.job.list(per_page=10, page=2)
```

Get [details](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Jobs-Get_Job_Details) about a job.

The number passed to `details` is the ID of a Zencoder job.

```python
client.job.details(1)
```

Get [progress](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Jobs-Job_Progress) on a job.

The number passed to `progress` is the ID of a Zencoder job.

```python
client.job.progress(1)
```

[Resubmit](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Jobs-Resubmit_a_Job) a job

The number passed to `resubmit` is the ID of a Zencoder job.

```python
client.job.resubmit(1)
```

[Cancel](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Jobs-Cancel_a_Job) a job

The number passed to `cancel` is the ID of a Zencoder job.

```python
client.job.cancel(1)
```

## [Inputs](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Inputs)

Get [details](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Inputs-Get_Input_Details) about an input.

The number passed to `details` is the ID of a Zencoder input.

```python
client.input.details(1)
```

Get [progress](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Inputs-Update_Input_Progress) for an input.

The number passed to `progress` is the ID of a Zencoder input.

```python
client.input.progress(1)
```
## [Outputs](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Outputs)

Get [details](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Outputs-Get_Output_Details) about an output.

The number passed to `details` is the ID of a Zencoder output.

```python
client.output.details(1)
```

Get [progress](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Outputs-Update_Output_Progress) for an output.

The number passed to `progress` is the ID of a Zencoder output.

```python
client.output.progress(1)
```

## [Reports](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Reports)

Reports are great for getting usage data for your account. All default to 30 days from yesterday with no [grouping](https://support.brightcove.com/zencoder-encoding-settings-job#grouping), but this can be altered. These will return `422 Unprocessable Entity` if the date format is incorrect or the range is greater than 2 months. 

Get [all usage](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Reports-Get_Usage_for_VOD___Live) (Live + VOD).

```python
import datetime
client.report.all()
client.report.all(grouping="foo")
client.report.all(start_date=datetime.date(2011, 10, 30),
                end_date=datetime.date(2011, 11, 24))
client.report.all(start_date=datetime.date(2011, 10, 30),
                end_date=datetime.date(2011, 11, 24),
                grouping="foo")
```

Get [VOD usage](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Reports-Get_Usage_for_VOD).

```python
import datetime
client.report.vod()
client.report.vod(grouping="foo")
client.report.vod(start_date=datetime.date(2011, 10, 30),
               end_date=datetime.date(2011, 11, 24))
client.report.vod(start_date=datetime.date(2011, 10, 30),
               end_date=datetime.date(2011, 11, 24),
               grouping="foo")
```

Get [Live usage](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Reports-Get_Usage_for_Live).

```python
import datetime
client.report.live()
client.report.live(grouping="foo")
client.report.live(start_date=datetime.date(2011, 10, 30),
                end_date=datetime.date(2011, 11, 24))
client.report.live(start_date=datetime.date(2011, 10, 30),
                end_date=datetime.date(2011, 11, 24),
                grouping="foo")
```

## [Accounts](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Accounts)

Create a [new account](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Accounts-Create_an_Account). A unique email address and terms of service are required, but you can also specify a password (and confirmation) along with whether or not you want to subscribe to the Zencoder newsletter. New accounts will be created under the Test (Free) plan.

No API Key is required.

```python
client.account.create('foo@example.com', tos=1)
client.account.create('foo@example.com', tos=1,
                   options={'password': 'abcd1234',
                            'password_confirmation': 'abcd1234',
                            'affiliate_code': 'foo'})
```

Get [details](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Accounts-Get_Account_Details) about the current account.

```python
client.account.details()
```

Turn [integration mode](https://brightcovelearning.github.io/Brightcove-API-References/zencoder-api/v2/doc/index.html#api-Accounts-Turn_On_Integration_Mode) on (all jobs are test jobs).

```python
client.account.integration()
```

Turn off integration mode, which means your account is live (and you'll be billed for jobs).

```python
client.account.live()
```

## Tests

The tests use the `mock` library to stub in response data from the API. Run tests individually:

    $ python test/test_jobs.py

Or use `nose`:

    $ nosetests

