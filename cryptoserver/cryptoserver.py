#!/usr/bin/env python3
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
from program import Program
import syslog


__all__ = []
__version__ = 0.1
__date__ = '2016-02-17'
__updated__ = '2016-02-17'

TESTRUN = 0

def main(argv=None, syslog=syslog):

    if argv is None:
        argv = sys.argv[1:]
        program = Program(__version__, __updated__, argv, syslog)
        program.mainLoop()
    program.logFinish()

if __name__ == "__main__":
    if TESTRUN:
        import doctest
        doctest.testmod()
    sys.exit(main())
