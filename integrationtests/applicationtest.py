#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
from application import FakeServer
from Application import Application
import config
from StringIO import StringIO

class ApplicationTest(unittest.TestCase):

    def test_Application(self):
        environ = {}
        environ['REMOTE_ADDR'] = '192.168.1.2'
        payload = """<request><id>17203133959</id><mothername>testname</mothername></request>"""
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
