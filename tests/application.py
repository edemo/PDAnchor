#!/usr/bin/python

import unittest
from Application import Application
from StringIO import StringIO
import config

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
        wsgiInput = StringIO(payload)
        environ['wsgi.input'] = wsgiInput
        environ['CONTENT_LENGTH'] = "{0}".format(len(payload))
        fakeServer = FakeServer()
        response = Application().application(environ, fakeServer.start_response)
        self.assertEquals(
            ["<hash>{0}</hash>".format(config.testHash)],
            response);
        self.assertEquals("200 OK", fakeServer.status)
        self.assertEquals(('Content-Length',"{0}".format(len(response[0]))), fakeServer.headers[1])
        self.assertEquals(('Access-Control-Allow-Origin',"*"), fakeServer.headers[2])
        self.assertEquals(('Content-Type',"text/xml"), fakeServer.headers[0])

    def test_origin_header_in_bad_request(self):
        environ = {}
        environ['REMOTE_ADDR'] = '192.168.1.2'
        payload = """<id>1720313395</id>"""
        wsgiInput = StringIO(payload)
        environ['wsgi.input'] = wsgiInput
        environ['CONTENT_LENGTH'] = "{0}".format(len(payload))
        fakeServer = FakeServer()
        response = Application().application(environ, fakeServer.start_response)
        self.assertEquals("406 Not Acceptable", fakeServer.status)
        self.assertEquals(('Content-Length',"{0}".format(len(response[0]))), fakeServer.headers[1])
        self.assertEquals(('Access-Control-Allow-Origin',"*"), fakeServer.headers[2])
        self.assertEquals(('Content-Type',"text/xml"), fakeServer.headers[0])



if __name__ == '__main__':
        unittest.main()
