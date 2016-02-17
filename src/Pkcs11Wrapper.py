import config
from Crypto.Hash.SHA512 import SHA512Hash
import socket
import traceback
import syslog


class Pkcs11Wrapper(object):
    def sign(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((config.cryptoserver_host,config.cryptoserver_port))  # @UndefinedVariable
            sock.sendall(data)
            response = sock.recv(1024)
        except:
            syslog.syslog(traceback.format_exc())
            raise
        finally:
            sock.close()
        s=""
        for byte in response:
            s += "{0:02x}".format(ord(byte))
        return s

    def hash(self, data):
        data = SHA512Hash(data).digest()
        data = self.sign(data)
        data = SHA512Hash(data).hexdigest()
        return data
