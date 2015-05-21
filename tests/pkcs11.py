import unittest
import config
from Pkcs11Wrapper import Pkcs11Wrapper

class Pkcs11Test(unittest.TestCase):

    def test_one_session_from_initialisation_to_signature(self):
        pkcs11=Pkcs11Wrapper.getInstance()
        pkcs11.initSession()
        data="17203133959"
        s = pkcs11.sign(data)
        self.assertEquals(config.testSignature,s)
        pkcs11.cleanUp()

    def test_one_session_with_more_signatures(self):
        pkcs11=Pkcs11Wrapper.getInstance()
        pkcs11.initSession()
        data="17203133959"
        s = pkcs11.sign(data)
        self.assertEquals(config.testSignature,s)
        s = pkcs11.sign(data)
        self.assertEquals(config.testSignature,s)
        pkcs11.cleanUp()

    def test_more_sequential_sessions_with_more_signatures(self):
        pkcs11=Pkcs11Wrapper.getInstance()
        pkcs11.initSession()
        data="17203133959"
        s = pkcs11.sign(data)
        self.assertEquals(config.testSignature,s)
        s = pkcs11.sign(data)
        self.assertEquals(config.testSignature,s)
        pkcs11.cleanUp()
        
        pkcs11.initSession()
        data="17203133959"
        s = pkcs11.sign(data)
        self.assertEquals(config.testSignature,s)
        s = pkcs11.sign(data)
        self.assertEquals(config.testSignature,s)
        pkcs11.cleanUp()
