from s3_encryption import crypto
from s3_encryption.envelope import EncryptionEnvelope


class EncryptionHandler(object):

    def __init__(self, provider):
        self.provider = provider

    def build_request_context(self, context):
        cipher = context.get('cipher', None) or crypto.aes_cipher(mode='CBC')
        cipher.iv = crypto.aes_iv()
        cipher.key = crypto.aes_key()
        context['body'] = cipher.encrypt(context['raw_body'])
        context['envelope'] = self.build_envelope(cipher)
        return context

    def build_envelope(self, cipher):
        self.envelope = EncryptionEnvelope(self.provider.encryption_materials)
        self.envelope.iv = cipher.iv
        key = self.provider.key_for(self.provider.encryption_materials)
        self.envelope.key = crypto.aes_encrypt(key, cipher.key)
        return self.envelope


class DecryptionHandler(object):

    def __init__(self, provider):
        self.provider = provider

    def build_response_context(self, obj_metadata, context):
        self.envelope = EncryptionEnvelope()
        self.envelope.from_metadata(obj_metadata)
        self.deconstruct_envelope()
        cipher = crypto.aes_cipher(mode='CBC')
        cipher.iv = self.envelope.iv
        cipher.key = self.envelope.key
        context['cipher'] = cipher
        context['raw_body'] = cipher.decrypt(context['body'])
        return context

    def deconstruct_envelope(self):
        key = self.provider.key_for(self.provider.encryption_materials)
        self.envelope.key = crypto.aes_decrypt(key, self.envelope.key)
