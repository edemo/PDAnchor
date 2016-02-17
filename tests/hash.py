#!/usr/bin/python

import unittest
from config import testHash
from Pkcs11Wrapper import Pkcs11Wrapper
import time

class HashTest(unittest.TestCase):
    def test_Hash(self):
        hasher=Pkcs11Wrapper()
        self.assertEquals(testHash,hasher.hash("17203133959testname"))

    def test_double_init(self):
        hasher=Pkcs11Wrapper()
        self.assertEquals(testHash,hasher.hash("17203133959testname"))
        self.assertEquals(testHash,hasher.hash("17203133959testname"))
        
    def test_time_hash(self):
        hasher = Pkcs11Wrapper()
        now = time.time()
        times = []
        for j in range(10):  # @UnusedVariable
            now = time.time()
            for i in range(10):  # @UnusedVariable
                self.assertEqual(hasher.hash("17203133959testname"),testHash)
            elapsed = time.time() - now
            times.append(elapsed)
            print "one round elapsed: {0}".format(elapsed)
        
if __name__ == '__main__':
        unittest.main()

