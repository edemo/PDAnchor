#!/usr/bin/python

from tempfile import NamedTemporaryFile
from subprocess import Popen, STDOUT, PIPE
import hashlib
import config
import os

hashcmd = getattr(config,'hashcmd',"/usr/bin/pkcs15-crypt -s -p 0000 -i {0} --pkcs1 -o {1}")

class NoSmartCardException(Exception):
    pass

class Hasher():
    def __init__(self):
        self.inputFileName=self.createTempFile()
        self.outputFileName=self.createTempFile()

    def createTempFile(self):
        f=NamedTemporaryFile(delete=False)
        fileName=f.name
        f.close()
        return fileName
        
    def hash( self, inputString ):
        with open(self.inputFileName,"w") as inputFile:
            inputFile.write(inputString)
        self.callSmartCard()
        with open(self.outputFileName,"r") as outputFile:
            returned=outputFile.read()
        os.remove(self.outputFileName)
        os.remove(self.inputFileName)
        return hashlib.sha512(returned).hexdigest()

    def callSmartCard(self):
        cmd = hashcmd.format(self.inputFileName, self.outputFileName)
        proc = Popen(cmd.split(" "),stdout=PIPE, stderr=STDOUT)
        (stdout,dummy) = proc.communicate()
        if ( 0 != proc.returncode):
            raise NoSmartCardException(stdout)

