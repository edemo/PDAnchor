#!/usr/bin/python

import unittest
from Hasher import Hasher

class HashTest(unittest.TestCase):
    def test_Hash(self):
        hasher=Hasher()
        self.assertEquals("7f51e53deaa216e8b22d2708cfb00384",hasher.hash("17203133959"))

if __name__ == '__main__':
        unittest.main()

