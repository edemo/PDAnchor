#!/usr/bin/python

import unittest
from config import testSignature
from Pkcs11Wrapper import Pkcs11Wrapper

class HashTest(unittest.TestCase):
    def test_Hash(self):
        hasher=Pkcs11Wrapper()
        self.assertEquals(testSignature,hasher.hash("17203133959"))

    def test_double_init(self):
        hasher=Pkcs11Wrapper()
        self.assertEquals(testSignature,hasher.hash("17203133959"))
        self.assertEquals(testSignature,hasher.hash("17203133959"))
        
if __name__ == '__main__':
        unittest.main()

