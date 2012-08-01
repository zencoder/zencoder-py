Usage
=====

Here is some basic usage information::

    import zencoder
    zen = zencoder.Zencoder()
    zen.jobs.list()

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

