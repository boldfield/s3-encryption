from Crypto import Random
from Crypto.Cipher import AES as pyAES
import codecs


class AES(object):

    def __init__(self):
        self.key = None
        self._mode = None
        self.iv = None

    @staticmethod
    def str_to_bytes(data):
        t = type(b''.decode('utf-8'))
        if isinstance(data, t):
            return codecs.encode(data, 'utf-8')
        return data

    def encrypt(self, data):
        if self.iv is None:
            cipher = pyAES.new(self.key, self.mode)
        else:
            cipher = pyAES.new(self.key, self.mode, self.iv)
        return cipher.encrypt(pad_data(AES.str_to_bytes(data)))

    def decrypt(self, data):
        if self.iv is None:
            cipher = pyAES.new(self.key, self.mode)
        else:
            cipher = pyAES.new(self.key, self.mode, self.iv)
        return unpad_data(cipher.decrypt(AES.str_to_bytes(data)))

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        m = 'MODE_{}'.format(mode.upper()) if not mode.startswith('MODE') else mode
        self._mode = getattr(pyAES, m)


def aes_cipher(key=None, iv=None, mode=None):
    aes = AES()
    aes.iv = iv if iv else None
    aes.mode = mode if mode else None
    aes.key = key if key else None
    return aes


def aes_encrypt(key, data, mode='ECB', iv=None):
    aes = AES()
    aes.mode = mode
    aes.iv = iv
    aes.key = key
    return aes.encrypt(data)


def aes_decrypt(key, data, mode='ECB', iv=None):
    aes = AES()
    aes.mode = mode
    aes.iv = iv
    aes.key = key
    return aes.decrypt(data)


def aes_iv():
    return Random.new().read(pyAES.block_size)


def aes_key():
    return Random.new().read(pyAES.block_size)


pad_data = lambda s: s + (pyAES.block_size - len(s) % pyAES.block_size) * AES.str_to_bytes(chr(pyAES.block_size - len(s) % pyAES.block_size))
unpad_data = lambda s: s[0:-ord(s[len(s)-1:])]
