# encoding: utf-8
from optparse import OptionParser
import sys
import traceback
import SocketServer
import os
import syslog
from server import CryptoServer

class Program(object):
    def __init__(self, version, updated, argv, syslog):
        self.syslog=syslog
        self.startLogging()
        self.program_version = version
        self.program_build_date = "%s" % updated
        self.setupDescription()
        self.setupParser()
        self.parseArgs(argv)
        self.setupEnvironment()


    def mainLoop(self):
        try:
            self.main()
        except:
            self.handleException()

    def main(self):
        SocketServer.TCPServer.allow_reuse_address = True
        CryptoServer.opts = self.opts
        CryptoServer.syslog = self.syslog
        server = SocketServer.TCPServer((self.opts.host, self.opts.port), CryptoServer)
        self.syslog.syslog("listening at {0} {1}".format(self.opts.host, self.opts.port))
        server.serve_forever()

    def handleException(self):
        excString = traceback.format_exc()
        self.syslog.syslog(excString)

    def setupDescription(self):
        self.program_name = os.path.basename(sys.argv[0]) # @UnusedVariable
        self.program_version_string = '%%prog %s (%s)' % (self.program_version, self.program_build_date)
        self.program_longdesc = '''''' # optional - give further explanation about what the program does
        self.program_license = u"Copyright 2016 Magosányi Árpád Licensed under GNU GPL v3"

    def setupParser(self):
        parser = OptionParser(
            version=self.program_version_string,
            epilog=self.program_longdesc,
            description=self.program_license)
        parser.add_option("-d", "--id", dest="keyid", type="string",
                    help="key id (mandatory!)")
        parser.add_option("-m", "--module", dest="module", type="string",
                    help="pkcs11 module path")
        parser.add_option("-p", "--pin", dest="pin", type="string",
                    help="pin [default: %default]")
        parser.add_option("-M", "--mechanism", dest="mechanism",
                    help="HNAC/sign mechanism to use [default: %default]", type="string")
        parser.add_option("-H", "--host", dest="host", type="string",
                    help="host [default: %default]")
        parser.add_option("-P", "--port", dest="port", type="int",
                    help="port [default: %default]")
        parser.add_option("-v", "--verbose", dest="verbose", action="count",
                    help="verbose to syslog. WARNING: logs PIN! [default: %default]")
        parser.add_option("-i", "--inputlenght", dest="inputlength", type="int",
                    help="length of input strings [default: %default]")
        parser.add_option("-o", "--outputlength", dest="outputlength", type="int",
                    help="length of output strings [default: %default]")
        parser.add_option("-e", "--environment", dest="environment", type="string",
                    help="append var=value to environment [default: %default]")
        parser.set_defaults(
                module="/usr/lib/opensc-pkcs11.so",
                pin=u"0000",
                mechanism="SHA512-RSA-PKCS",
                host=u"localhost",
                port=9999,
                inputlength=256,
                outputlength=256,
                environment=None)
        self.parser = parser

    def parseArgs(self, argv):
        opts, args = self.parser.parse_args(argv)  # @UnusedVariable
        if not opts.keyid:
            print self.parser.format_help()
            sys.exit(1)
        self.opts = opts

    def setupEnvironment(self):
        if self.opts.environment:
            name, value = self.opts.environment.split("=", 2)
            os.environ[name] = value

    def startLogging(self):
        self.syslog.openlog("cryptoserver", logoption=syslog.LOG_PID)
        self.syslog.syslog("cryptoserver started")

    def logFinish(self):
        return self.syslog.syslog("cryptoserver stopped at {0} {1}".format(self.opts.host, self.opts.port))
