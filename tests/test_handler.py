from nose.tools import assert_equal
from mock import Mock
import codecs

from . import BaseS3EncryptTest


class BaseHandlerTest(BaseS3EncryptTest):

    @staticmethod
    def bytes_to_str(data):
        t = type(b''.decode('utf-8'))
        if not isinstance(data, t):
            return data.decode('utf-8')
        return data

    def setUp(self):
        self.iv = self.decode64(codecs.encode("TO5mQgtOzWkTfoX4RE5tsA==", 'utf-8'))
        self.key = self.decode64("uSwsRlIMhY1klVYrgqceqjmQMmARcNl7rEKWW+7HVvA=")
        self.encrypted_key = 'gX+a4JQYj7FP0y5TAAvxTz4e2l0DvOItbXByml/NPtKQcUlsoGHoYR/T0TuYHcNj'

        self.master_key = self.decode64("kM5UVbhE/4rtMZJfsadYEdm2vaKFsmV2f5+URSeUCV4=")

        self.matdesc = '{}'

        self.mock_encryption_materials = Mock(description={})
        self.mock_provider = Mock(encryption_materials=self.mock_encryption_materials)
        self.mock_provider.key_for = lambda x: self.master_key

        self.raw_body = 'secret'
        self.encrypted_body = self.decode64("JIgXCTXpeQerPLiU6dVL4Q==")

        self.base_request_context = {
            'raw_body': self.raw_body
        }

        self.base_response_context = {
            'body': self.encrypted_body
        }

        from s3_encryption import crypto
        crypto.aes_iv = lambda: self.iv
        crypto.aes_key = lambda: self.key


class TestEncryptionHandler(BaseHandlerTest):

    def test_build_request_context(self):
        from s3_encryption.handler import EncryptionHandler
        old_build_env = EncryptionHandler.build_envelope
        EncryptionHandler.build_envelope = lambda x, y: self.matdesc

        handler = EncryptionHandler(self.mock_provider)

        context = handler.build_request_context(self.base_request_context)

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


class TestDecryptionHandler(BaseHandlerTest):

    def test_build_response_context(self):
        from s3_encryption.handler import DecryptionHandler
        old_deconstruct = DecryptionHandler.deconstruct_envelope
        mock_metadata = {
            'x-amz-key': self.encrypted_key,
            'x-amz-iv': self.encode64(self.iv),
            'x-amz-matdesc': self.matdesc
        }

        def decon(x):
            x.envelope.key = self.key
        DecryptionHandler.deconstruct_envelope = decon

        handler = DecryptionHandler(self.mock_provider)
        context = handler.build_response_context(mock_metadata, self.base_response_context)

        DecryptionHandler.deconstruct_envelope = old_deconstruct

        assert_equal(self.bytes_to_str(context['raw_body']), self.raw_body)

    def test_deconstruct_envelope(self):
        from s3_encryption.handler import DecryptionHandler
        handler = DecryptionHandler(self.mock_provider)

        class Envelope(object):
            # EncryptionEnvelope takes care of base64 decoding items when
            # they're returned
            key = self.decode64(self.encrypted_key)
        handler.envelope = Envelope()
        handler.deconstruct_envelope()
        assert_equal(handler.envelope.key, self.key)
