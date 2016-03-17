#encoding: utf-8
import SocketServer
import subprocess
import tempfile
import os
import gettext

gettext.install("PDAnchor")
problemRunningCommand = _("problem running command: {0}")
inputSizeMismatch = _("input size mismatch: {1} bytes instead of {0} bytes")
commandOutputSizeMismatch = _("command output size mismatch: {1} bytes instead of {0} bytes")
anErrorOccured = _("an error occured, try again later")
exitCode = _("exit code: {0}")

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
            self.handleError(problemRunningCommand.format(e))
        if proc.returncode:
            self.handleError(exitCode.format(proc.returncode))

    def receiveData(self):
        data = self.request.recv(self.opts.inputlength)
        if len(data) != self.opts.inputlength:
            self.handleError(
                inputSizeMismatch.format(
                    self.opts.inputlength,
                    len(data)))            
        return data

    def getResponse(self, name):
        f = open(name)
        data = f.read()
        os.unlink(name)
        if len(data) != self.opts.outputlength:
            self.handleError(
                commandOutputSizeMismatch.format(
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
            res = anErrorOccured
        self.sendResult(res)

class CryptoServer(CryptoServerBase,SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
