from __future__ import print_function
from FtpIndex import FtpIndex
import json
import boto3
import uuid

s3_boto=boto3.resource('s3')

def lambda_handler(event, context):
  '''
  AWS lambda function
  '''

  for record in event['Records']:
    bucket=record['s3']['bucket']['name']
    key=record['s3']['object']['key']

    # Set upload and download path
    download_path='/tmp/{}{}'.format(uuid.uuid4(), key)
    upload_path='/tmp/stats-{}.json'.format(key)
    
    # Download input file
    s3_boto.meta.client.download_file(bucket, key, download_path)

    # Read index data
    index_data=FtpIndex(download_path)
    index_stats=index_data.get_all_stats()

    # write json report
    with open(upload_path, 'w') as out_json:
      out_json.write(json.dumps(index_stats, indent=2))   

    # Upload report to bucket with suffix '-report'
    s3_boto.meta.client.upload_file(upload_path, '{}-report'.format(bucket), '{}.json'.format(key))
