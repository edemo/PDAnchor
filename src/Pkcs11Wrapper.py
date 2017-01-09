import config
from Crypto.Hash.SHA512 import SHA512Hash
import socket
import traceback
import syslog
from Exceptions import IncorrectLengthException
from enforce.decorators import runtime_validation

class Pkcs11Wrapper(object):
    @runtime_validation
    def sign(self, data: bytes):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((config.cryptoserver_host,config.cryptoserver_port))  # @UndefinedVariable
            sock.sendall(data.zfill(config.inputlength))
            response = sock.recv(config.outputlength)
            if len(response) != config.outputlength:
                raise IncorrectLengthException(config.outputlength, response)
        except:
            syslog.syslog(traceback.format_exc())
            raise
        finally:
            sock.close()
        s=""
        for byte in response:
            s += "{0:02x}".format(byte)
        return s

    @runtime_validation
    def hash(self, data: bytes):
        data = SHA512Hash(data).digest()
        data = self.sign(data).encode()
        data = SHA512Hash(data).hexdigest()
        return data
