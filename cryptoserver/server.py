import SocketServer
import subprocess
import tempfile
import os
import syslog

    
def main(opts):
    SocketServer.TCPServer.allow_reuse_address = True
    CryptoServer.opts = opts
    server = SocketServer.TCPServer((opts.host, opts.port), CryptoServer)
    server.serve_forever()

class CryptoServer(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024) #ASSUMPTION: we will always get all the input in one packet.
        temp=tempfile.NamedTemporaryFile()
        name = temp.name
        temp.close()
        cmd = ["pkcs11-tool",
               "--module",
               self.opts.module,
               "-l",
               "-p",
               self.opts.pin,
               "-d",
               self.opts.keyid,
               "-m",
               self.opts.mechanism,
               "-s",
               "-o",
               name
            ]
        if self.opts.verbose:
            syslog.syslog(str(cmd))
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        proc.stdin.write(data)
        (out,err) = proc.communicate()
        syslog.syslog(out)
        syslog.syslog(err)
        f = open(name)
        res = f.read()
        os.unlink(name)
        self.request.sendall(res)
