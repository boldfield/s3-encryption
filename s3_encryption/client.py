import boto3
from s3_encryption import crypto
from s3_encryption.handler import EncryptionHandler, DecryptionHandler
from s3_encryption.exceptions import ArgumentError
from s3_encryption.key_provider import DefaultKeyProvider


class S3EncryptionClient(object):

    def __init__(self, encryption_key=None, **kwargs):
        self.client = kwargs.get('client', None)
        if self.client is None:
            self.client = boto3.client('s3', region_name=kwargs.get('region_name', None))

        self.key_provider = self.extract_key_provider(encryption_key=encryption_key, **kwargs)
        self.envelope_location = self.extract_location(**kwargs)
        self.instruction_file_suffix = self.extract_suffix(**kwargs)

    def put_object(self, Bucket=None, Key=None, Body=None, ACL=None):
        context = {
            'raw_body': Body,
            'cipher': crypto.aes_cipher(mode='CBC')
        }
        handler = EncryptionHandler(self.key_provider)
        context = handler.build_request_context(context)
        kwargs = {
           'Bucket': Bucket,
           'Key': Key,
           'Body': context['body'],
           'Metadata': context['envelope']
        }
        if ACL is not None:
            kwargs['ACL'] = ACL
        self.client.put_object(**kwargs)

    def get_object(self, Bucket=None, Key=None):
        resp = self.client.get_object(Bucket=Bucket, Key=Key)
        context = {'body': resp['Body'].read()}
        handler = DecryptionHandler(self.key_provider)
        context = handler.build_response_context(resp['Metadata'], context)
        return context['raw_body']

    def extract_key_provider(self, **kwargs):
        if 'encryption_key' not in kwargs:
            msg = 's3_encryption currently only supports '\
                  'encryption with client provided keys.'
            raise ArgumentError(msg)
        return DefaultKeyProvider(kwargs['encryption_key'], **kwargs)

    def extract_location(self, **kwargs):
        location = kwargs.get('envelope_location', 'metadata')
        if location not in ['instruction_file', 'metadata']:
            msg = 'envelope_location must be one of: metadata, instruction_file'
            raise ArgumentError(msg)
        return location

    def extract_suffix(self, **kwargs):
        return kwargs.get('instruction_file_suffix', '.instruction')
