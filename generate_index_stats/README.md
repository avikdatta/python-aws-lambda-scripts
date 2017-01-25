# A python script for data stats generation using AWS lambda
A script for generation of samples stats using a [index file](http://ftp.ebi.ac.uk/pub/databases/blueprint/releases/current_release/homo_sapiens/20160816.data.index). Scripts in this repo are based on this [AWS lambda tutorial](http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html).

## Steps for creating AWS lambda function

### Upload codes to AWS S3
* Download this repository using git clone or download option from Github.
* Create a zip containing the python scripts
   <pre><code>
    zip -9 index_stats_scripts.zip python-aws-lambda-scripts/generate_index_stats/*.py
   </code></pre>
* Create a bucket for codes in S3
  <pre><code>
  aws s3 mb s3://myBucketForCode
  </code></pre>
* Upload the scripts to S3
  <pre><code>
  aws s3 cp index_stats_scripts.zip s3://myBucketForCode/
  </code></pre>
  
### Create lambda function
  <pre><code>
  aws lambda create-function \
  --region us-east-1 \
  --function-name index-stats \
  --code S3Bucket=myBucketForCode,S3Key=index_stats_scripts.zip \
  --role arn:aws:iam::xxxxxxxxx:role/lambda-s3-execution \
  --handler get_stats.lambda_handler \
  --runtime python2.7 \
  --profile aws_admin \
  --timeout 3 \
  --memory-size 128
  </code></pre>

### Create input/output buckets
Create S3 buckets for input and output files
<pre><code>
# Input bucket
aws s3 mb s3://myInputFiles

# Output bucket
aws s3 mb s3://myInputFiles-report
</code></pre>

### Create event in S3 input bucket and add access permission policy
Create an event in theS3 input file bucket following the above mentioned [AWS tutorial](http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-configure-event-source.html).

### Create a Test event
Add a test for the lambda function.
  <pre><code>
  {
  "Records": [
    {
      "eventVersion": "2.0",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "s3": {
        "configurationId": "testConfigRule",
        "object": {
          "eTag": "0123456789abcdef0123456789abcdef",
          "key": "i_300.index",
          "sequencer": "0A1B2C3D4E5F678901",
          "size": 128
        },
        "bucket": {
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "name": "ftp_index_files",
          "arn": "arn:aws:s3:::ftp_index_files"
        },
        "s3SchemaVersion": "1.0"
      },
      "responseElements": {
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
        "x-amz-request-id": "EXAMPLE123456789"
      },
      "awsRegion": "us-east-1",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "eventSource": "aws:s3"
    }
   ]
 }
 </code></pre>
 
 ### Upload file in input bucket and check the output bucket
 <pre><code>
 # Upload input file
 aws s3 cp input.index s3://myInputFiles
 
 # Download output files
 aws s3 cp s3://myInputFiles-report/input.index.json
 </code></pre>
 
 
