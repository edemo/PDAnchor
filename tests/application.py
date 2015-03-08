#!/usr/bin/python

import unittest
from Application import Application
from StringIO import StringIO

class FakeServer:
    def __init__(self):
        self.status = None
        self.headers = None

    def start_response(self,status,headers):
        self.status = status
        self.headers = headers

class ApplicationTest(unittest.TestCase):

    def test_Application(self):
        environ = {}
        environ['REMOTE_ADDR'] = '192.168.1.2'
        payload = """<id>17203133959</id>"""
        input = StringIO(payload)
        environ['wsgi.input'] = input
        environ['CONTENT_LENGTH'] = "{0}".format(len(payload))
        fakeServer = FakeServer()
        response = Application().application(environ, fakeServer.start_response)
        self.assertEquals(["<hash>7f51e53deaa216e8b22d2708cfb00384</hash>"],response);
        self.assertEquals("200 OK", fakeServer.status)
        print fakeServer.headers
        self.assertEquals(('Content-Length',"{0}".format(len(response[0]))), fakeServer.headers[1])
        self.assertEquals(('Access-Control-Allow-Origin',"*"), fakeServer.headers[2])



if __name__ == '__main__':
        unittest.main()
