import unittest
from nose.tools import assert_equal
from mock import Mock, MagicMock, patch


from . import BaseS3EncryptTest


class TestEncryptionHandler(BaseS3EncryptTest):
    def setUp(self):
        self.iv = self.decode64("TO5mQgtOzWkTfoX4RE5tsA==")
        self.key = self.decode64("uSwsRlIMhY1klVYrgqceqjmQMmARcNl7rEKWW+7HVvA=")
        self.encrypted_key = 'gX+a4JQYj7FP0y5TAAvxTz4e2l0DvOItbXByml/NPtKQcUlsoGHoYR/T0TuYHcNj'

        self.master_key = self.decode64("kM5UVbhE/4rtMZJfsadYEdm2vaKFsmV2f5+URSeUCV4=")
        self.encrypted_body = self.decode64("JIgXCTXpeQerPLiU6dVL4Q==")

        self.matdesc = '{}'

        self.mock_encryption_materials = Mock(description={})
        self.mock_provider = Mock(encryption_materials=self.mock_encryption_materials)
        self.mock_provider.key_for = lambda x: self.master_key

        self.base_context = {
            'raw_body': 'secret'
        }

        from s3_encryption import crypto
        crypto.aes_iv = lambda: self.iv
        crypto.aes_key = lambda: self.key

    def test_build_request_context(self):
        from s3_encryption.handler import EncryptionHandler
        old_build_env = EncryptionHandler.build_envelope
        EncryptionHandler.build_envelope = lambda x, y: self.matdesc

        handler = EncryptionHandler(self.mock_provider)

        context = handler.build_request_context(self.base_context)

        EncryptionHandler.build_envelope = old_build_env

        assert_equal(context['body'], self.encrypted_body)
        assert_equal(context['envelope'], self.matdesc)

    def test_build_envelope(self):
        from s3_encryption.handler import EncryptionHandler
        from s3_encryption import crypto
        cipher = crypto.aes_cipher(mode='CBC')
        cipher.iv = crypto.aes_iv()
        cipher.key = crypto.aes_key()

        handler = EncryptionHandler(self.mock_provider)
        envelope = handler.build_envelope(cipher)

        assert_equal(envelope['x-amz-key'], self.encrypted_key)
        assert_equal(envelope['x-amz-iv'], self.encode64(self.iv))
        assert_equal(envelope['x-amz-matdesc'], self.matdesc)
