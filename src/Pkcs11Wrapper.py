import PyKCS11
import config
import threading
from Crypto.Hash.SHA512 import SHA512Hash

class ConCurrencyException(Exception):
    pass


class Pkcs11Wrapper(object):
    singleton = None
    lock = threading.Lock()
    def __init__(self, key = None):
        if key != "initializing":
            raise ValueError("this is singleton")
        self.p11lib = PyKCS11.PyKCS11Lib()
        self.p11lib.load(config.pkcs11lib)


    @classmethod
    def getInstance(cls):
        if cls.singleton == None:
            cls.singleton = cls(key="initializing")
        return cls.singleton
        
    def initSession(self):
        if not self.lock.acquire(False):
            raise ConCurrencyException
        self.session = self.p11lib.openSession(config.tokenSlot)
        try:
            self.session.login(config.PIN)
        except PyKCS11.PyKCS11Error:
            pass
        self.key = self.session.findObjects()[config.tokenObjectIndex]
        self.mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA256_RSA_PKCS, None) # @UndefinedVariable

    def sign(self, data):
        signature = self.session.sign(self.key, data, self.mechanism)
        s = ""
        for byte in signature:
            s += "{0:02x}".format(byte)
        return s
    
    def cleanUp(self):
        self.session.closeSession()
        self.lock.release()
        

    def _hash(self, data):
        data = SHA512Hash(data).digest()
        data = self.sign(data)
        data = SHA512Hash(data).hexdigest()
        return data

    def hash(self, data):
        self.initSession()
        data = self._hash(data)
        self.cleanUp()
        return data
