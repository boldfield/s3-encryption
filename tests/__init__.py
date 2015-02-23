import base64
import unittest


def setup_package(self):
    pass


def teardown_package(self):
    pass


class BaseS3EncryptTest(unittest.TestCase):

    def decode64(self, data):
        return base64.b64decode(data)

    def encode64(self, data):
        return base64.b64encode(data)
