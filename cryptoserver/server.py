import SocketServer
import subprocess
import tempfile
import os

class CryptoServerBase(object):

    def getTempName(self):
        temp = tempfile.NamedTemporaryFile()
        name = temp.name
        temp.close()
        return name

    def compileCommandLine(self, name):
        cmd = ["pkcs11-tool", "--module", 
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
            name]
        if self.opts.verbose:
            self.syslog.syslog(str(cmd))
        return cmd


    def handleError(self, errMsg):
        self.syslog.syslog(errMsg)
        raise RuntimeError(errMsg)

    def runCommand(self, data, cmd):
        try:
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.stdin.write(data)
            out, err = proc.communicate()
            self.logRun(out, err)
        except Exception as e:
            self.handleError("problem running command: {0}".format(e))
        if proc.returncode:
            self.handleError("exit code: {0}".format(proc.returncode))

    def receiveData(self):
        data = self.request.recv(self.opts.inputlength)
        if len(data) != self.opts.inputlength:
            self.handleError(
                "input is not {0} bytes ({1} bytes)".format(
                    self.opts.inputlength,
                    len(data)))            
        return data

    def getResponse(self, name):
        f = open(name)
        data = f.read()
        os.unlink(name)
        if len(data) != self.opts.outputlength:
            self.handleError(
                "command output is not {0} bytes ({1} bytes)".format(
                    self.opts.outputlength,
                    len(data)))            
        return data

    def logRun(self, out, err):
        self.syslog.syslog(out)
        self.syslog.syslog(err)

    def sendResult(self, res):
        self.request.sendall(res)

    def handle(self):
        try:
            data = self.receiveData()
            name = self.getTempName()
            cmd = self.compileCommandLine(name)
            self.runCommand(data, cmd)
            res = self.getResponse(name)
        except Exception:
            res = "an error occured, try again later"
        self.sendResult(res)

class CryptoServer(CryptoServerBase,SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
