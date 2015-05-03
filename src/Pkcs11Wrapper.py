import PyKCS11
import config
class Pkcs11Wrapper(object):
    def __init__(self):
        self.p11lib = PyKCS11.PyKCS11Lib()
        self.p11lib.load("/usr/lib/opensc-pkcs11.so")


    def initSession(self):
        self.session = self.p11lib.openSession(config.tokenSlot)
        self.session.login(config.PIN)
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
        
    def hash(self, data):
        self.initSession()
        return self.sign(data)
