s3-encryption is a thin wrapper around the `boto3` S3 client.  It facilitates client-side encryption which is compatable to
that which is provided by the Ruby aws-sdk-resources.

Functionality is currently limited to that demonstrated below:

```python

import boto3
from s3_encryption.client import S3EncryptionClient

REGION = 'us-west-2'
BUCKET = 'testing.stuff.bucket'
s3_key = 'testing.txt'

s3e = S3EncryptionClient(encryption_key=plaintext_key, region_name=REGION)
s3e.put_object(Body='this is a test', Bucket=BUCKET, Key='testing.txt')
s3e.client.put_object(Body=encoded_key, Bucket='pubkey.domains.socrata.com', Key=s3_key + '.key')
```

```python

REGION = 'us-west-2'
BUCKET = 'testing.stuff.bucket'
s3_key = 'testing.txt'

s3 = boto3.client('s3', region_name=REGION)
encoded_key = s3.get_object(Bucket=BUCKET, Key=s3_key + '.key')

plaintext_key = decode_encryption_key(enc_key['Body'].read())

s3e = S3EncryptionClient(encryption_key=plaintext_key, region_name=REGION)
print s3e.get_object(Bucket=BUCKET, Key=s3_key)
>> 'this is a test'
```


```ruby

REGION = 'us-west-2'
BUCKET = 'testing.stuff.bucket'
s3_key = 'testing.txt'

s3c = Aws::S3::Client.new
res = s3c.get_object(:bucket => BUCKET, :key => s3_key + '.key')
enc_key = res[:body].read

plaintext_key = decode_encryption_key(enc_key)

s3ec = Aws::S3::Encryption::Client.new(:encryption_key => plaintext_key)
res = s3ec.get_object(:bucket => bucket, :key => s3_key)
body = res[:body].read
puts body
>> 'this is a test'
```
