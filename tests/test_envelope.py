from nose.tools import (assert_equal, raises)
from mock import Mock

from s3_encryption.envelope import EncryptionEnvelope
from s3_encryption.exceptions import IncompleteMetadataError

from . import BaseS3EncryptTest


class TestEnvelope(BaseS3EncryptTest):

    def setUp(self):
        self.mock_materials = Mock(description={})
        self.iv_64 = '5GVrEmPudo4GQWYxrIZaKQ=='
        self.iv = self.decode64(self.iv_64)
        self.key_64 = 'RLSBWuEuUy1jpkn+tdgv6Q=='
        self.key = self.decode64(self.key_64)

    def test_encoding(self):
        envelope = EncryptionEnvelope(self.mock_materials)
        envelope.iv = self.iv
        envelope.key = self.key

        assert_equal(envelope['x-amz-matdesc'], '{}')
        assert_equal(envelope.iv, self.iv)
        assert_equal(envelope['x-amz-iv'], self.iv_64)
        assert_equal(envelope.key, self.key)
        assert_equal(envelope['x-amz-key'], self.key_64)

    def test_from_metadata(self):
        meta = {
            'x-amz-matdesc': '{}',
            'x-amz-iv': self.iv_64,
            'x-amz-key': self.key_64
        }
        envelope = EncryptionEnvelope()
        envelope.from_metadata(meta)

        assert_equal(envelope['x-amz-matdesc'], '{}')
        assert_equal(envelope.iv, self.iv)
        assert_equal(envelope['x-amz-iv'], self.iv_64)
        assert_equal(envelope.key, self.key)
        assert_equal(envelope['x-amz-key'], self.key_64)

    @raises(IncompleteMetadataError)
    def test_from_metadata_missing_key(self):
        meta = {
            'x-amz-matdesc': '{}',
            'x-amz-iv': self.iv_64,
        }
        envelope = EncryptionEnvelope()
        envelope.from_metadata(meta)

    @raises(IncompleteMetadataError)
    def test_from_metadata_missing_matdesc(self):
        meta = {
            'x-amz-iv': self.iv_64,
            'x-amz-key': self.key_64
        }
        envelope = EncryptionEnvelope()
        envelope.from_metadata(meta)

    @raises(IncompleteMetadataError)
    def test_from_metadata_missing_iv(self):
        meta = {
            'x-amz-matdesc': '{}',
            'x-amz-key': self.key_64
        }
        envelope = EncryptionEnvelope()
        envelope.from_metadata(meta)

    @raises(IncompleteMetadataError)
    def test_from_metadata_empty(self):
        meta = {}
        envelope = EncryptionEnvelope()
        envelope.from_metadata(meta)
