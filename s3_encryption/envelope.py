import json
import base64
import codecs

from s3_encryption.exceptions import IncompleteMetadataError


class EncryptionEnvelope(dict):

    def __init__(self, materials=None):
        if materials is not None:
            self['x-amz-matdesc'] = json.dumps(materials.description)

    @property
    def key(self):
        _key = self.get('x-amz-key', None)
        if _key is not None:
            _key = self.decode64(_key)
        return _key

    @property
    def iv(self):
        _iv = self.get('x-amz-iv', None)
        if _iv is not None:
            _iv = self.decode64(_iv)
        return _iv

    @key.setter
    def key(self, key):
        self['x-amz-key'] = self.encode64(key)

    @iv.setter
    def iv(self, iv):
        self['x-amz-iv'] = self.encode64(iv)

    def json(self):
        return json.dumps(self)

    def from_metadata(self, metadata):
        self['x-amz-key'] = metadata.get('x-amz-key')
        self['x-amz-iv'] = metadata.get('x-amz-iv')
        self['x-amz-matdesc'] = metadata.get('x-amz-matdesc')
        if not (self['x-amz-key'] and self['x-amz-iv'] and self['x-amz-matdesc']):
            raise IncompleteMetadataError('All metadata keys are required for decryption (x-amz-key, x-amz-iv, x-amz-matdesc).')

    @classmethod
    def encode64(self, data):
        try:
            byte_data = bytes(data, 'utf-8')
        except TypeError:
            byte_data = bytes(data)
        return codecs.decode(base64.b64encode(byte_data), 'utf-8')

    @classmethod
    def decode64(self, data):
        try:
            byte_data = bytes(data, 'utf-8')
        except TypeError:
            byte_data = bytes(data)
        return base64.b64decode(byte_data)
