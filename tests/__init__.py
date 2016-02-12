import base64
import codecs
import unittest


def setup_package(self):
    pass


def teardown_package(self):
    pass


class BaseS3EncryptTest(unittest.TestCase):

    def decode64(self, data):
        try:
            byte_data = bytes(data, 'utf-8')
        except TypeError:
            byte_data = bytes(data)
        return base64.b64decode(byte_data)

    def encode64(self, data):
        try:
            byte_data = bytes(data, 'utf-8')
        except TypeError:
            byte_data = bytes(data)
        return codecs.decode(base64.b64encode(byte_data), 'utf-8')
