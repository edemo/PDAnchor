#!/usr/bin/env python
# encoding: utf-8
'''
cryptoserver -- the cryptographic server of anchor

cryptoserver is a small server which listens on a port, and returns the SHA512-RSA-PKCS mac of the input


@author:     magwas

@copyright:  2016 Magosanyi Arpad. All rights reserved.

@license:    GNU GPL v3

@contact:    mag@magwas.rulez.org
@deffield    updated: Updated
'''

import sys
import os

from optparse import OptionParser
import syslog
import server
import traceback

__all__ = []
__version__ = 0.1
__date__ = '2016-02-17'
__updated__ = '2016-02-17'

TESTRUN = 0

def main(argv=None):

    program_name = os.path.basename(sys.argv[0])
    program_version = __version__
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = u"Copyright 2016 Magosányi Árpád                                             \
                Licensed under GNU GPL v3"

    if argv is None:
        argv = sys.argv[1:]
    try:
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
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
        parser.add_option("-e", "--environment", dest="environment", type="string",
                          help="append var=value to environment [default: %default]")

        parser.set_defaults(module="/usr/lib/opensc-pkcs11.so", pin=u"0000", mechanism="SHA512-RSA-PKCS", host=u"localhost", port=9999, environment=None)

        # process options
        (opts, args) = parser.parse_args(argv)
        if not opts.keyid:
            print parser.format_help()
            sys.exit(1)
        
        if opts.environment:
            (name,value) = opts.environment.split("=",2)
            print (name,value)
            os.environ[name]=value
        syslog.openlog("cryptoserver", logoption=syslog.LOG_PID)
        syslog.syslog(str.format("cryptoserver started at {0} {1}",opts.host,opts.port))
        server.main(opts)

    except Exception:
        excString = traceback.format_exc()
        syslog.syslog(excString)
        print excString
        return 2
    syslog.syslog(str.format("cryptoserver stopped at {0} {1}",opts.host,opts.port))


if __name__ == "__main__":
    if TESTRUN:
        import doctest
        doctest.testmod()
    sys.exit(main())
