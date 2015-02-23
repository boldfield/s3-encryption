import json
import base64


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
        self['x-amz-key'] = self.encode64(key).encode('utf-8')

    @iv.setter
    def iv(self, iv):
        self['x-amz-iv'] = self.encode64(iv).encode('utf-8')

    def json(self):
        return json.dumps(self)

    def from_metadata(self, metadata):
        self['x-amz-key'] = metadata.get('x-amz-key', None)
        self['x-amz-iv'] = metadata.get('x-amz-iv', None)
        self['x-amz-matdesc'] = metadata.get('x-amz-matdesc', None)

    @classmethod
    def encode64(self, data):
        return base64.b64encode(data)

    @classmethod
    def decode64(self, data):
        return base64.b64decode(data)
