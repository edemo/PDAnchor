#encoding: utf-8
import socketserver
import subprocess
import tempfile
import os
import time
import traceback
from enforce import runtime_validation
from typing import List, Tuple
from socket import socket

problemRunningCommand = "problem running command: {0}"
inputSizeMismatch = "input size mismatch: {1} bytes instead of {0} bytes"
commandOutputSizeMismatch = "command output size mismatch: {1} bytes instead of {0} bytes"
anErrorOccured = b"an error occured, try again later"
exitCode = "exit code: {0}"

class CryptoServerBase(object):

    def getTempName(self):
        temp = tempfile.NamedTemporaryFile()
        name = temp.name
        temp.close()
        return name

    @runtime_validation
    def compileCommandLine(self, name: str):
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

    def compileWakeupCommandLine(self):
        pass
        cmd = ["pkcs11-tool", "--module", 
            self.opts.module, 
            "-O"]
        if self.opts.verbose:
            self.syslog.syslog(str(cmd))
        return cmd

    @runtime_validation
    def handleError(self, errMsg: str):
        self.syslog.syslog(errMsg)
        raise RuntimeError(errMsg)

    @runtime_validation
    def runCommand(self, data: bytes, cmd: List[str]):
        try:
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.stdin.write(data)
            out, err = proc.communicate()
            self.logRun(str(out), str(err))
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

    @runtime_validation
    def getResponse(self, name: str):
        f = open(name,"rb")
        data = f.read()
        os.unlink(name)
        if len(data) != self.opts.outputlength:
            f.close()
            self.handleError(
                commandOutputSizeMismatch.format(
                    self.opts.outputlength,
                    len(data)))
        f.close()
        return data

    @runtime_validation
    def logRun(self, out: str, err: str):
        self.syslog.syslog(str(out))
        self.syslog.syslog(str(err))

    @runtime_validation
    def sendResult(self, res: bytes):
        self.request.sendall(res)


    def wakeUpToken(self):
        preCmd = self.compileWakeupCommandLine()
        try:
            self.runCommand(b"", preCmd)
        except:
            time.sleep(3)
            self.runCommand(b"", preCmd)

    def handle(self):
        try:
            data = self.receiveData()
            self.wakeUpToken()
            name = self.getTempName()
            cmd = self.compileCommandLine(name)
            self.runCommand(data, cmd)
            res = self.getResponse(name)
        except Exception:
            self.syslog.syslog(traceback.format_exc())
            res = anErrorOccured
        self.sendResult(res)

    
class CryptoServer(CryptoServerBase,socketserver.BaseRequestHandler):
    @runtime_validation
    def __init__(self, request: socket, client_address: tuple, server):
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
