#!/usr/bin/python

import unittest
from config import testSignature
from Pkcs11Wrapper import Pkcs11Wrapper
import time

class HashTest(unittest.TestCase):
    def test_Hash(self):
        hasher=Pkcs11Wrapper.getInstance()
        self.assertEquals(testSignature,hasher.hash("17203133959"))

    def test_double_init(self):
        hasher=Pkcs11Wrapper.getInstance()
        self.assertEquals(testSignature,hasher.hash("17203133959"))
        self.assertEquals(testSignature,hasher.hash("17203133959"))
        
    def test_time_hash(self):
        hasher = Pkcs11Wrapper.getInstance()
        now = time.time()
        hasher.initSession()
        print "initialisation elapsed: {0}".format(time.time()-now)
        times = []
        for j in range(10):  # @UnusedVariable
            now = time.time()
            for i in range(10):  # @UnusedVariable
                hasher._hash("17203133959")
            elapsed = time.time() - now
            times.append(elapsed)
            print "one round elapsed: {0}".format(elapsed)
        print times
        hasher.cleanUp()
            
        
if __name__ == '__main__':
        unittest.main()

