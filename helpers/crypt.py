# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256
from base64 import b64encode, b64decode


class Crypt(object):
    key = 'd\'4[2rK8Q4@y3&}W2--4rYw348='

    def __init__(self, data):
        self.block_size = 16
        self.data = data
        self.key = sha256(Crypt.key.encode()).digest()[:32]
        self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr(
            self.block_size - len(s) % self.block_size)
        self.un_pad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self):
        plain_text = self.pad(self.data)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_OFB, iv)
        return b64encode(iv + cipher.encrypt(plain_text.encode())).decode()

    def decrypt(self):
        cipher_text = b64decode(self.data.encode())
        iv = cipher_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_OFB, iv)
        return self.un_pad(cipher.decrypt(cipher_text[self.block_size:])).decode()
