#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
from application import FakeServer
from Application import Application
import config
from io import BytesIO

class ApplicationTest(unittest.TestCase):

    def test_Application(self):
        environ = {}
        environ['REMOTE_ADDR'] = '192.168.1.2'
        payload = b"""<request><id>17203133959</id><mothername>testname</mothername></request>"""
        wsgiInput = BytesIO(payload)
        environ['wsgi.input'] = wsgiInput
        environ['CONTENT_LENGTH'] = "{0}".format(len(payload))
        fakeServer = FakeServer()
        response = Application().application(environ, fakeServer.start_response)
        self.assertEqual(
            ["<hash>{0}</hash>".format(config.testHash).encode()],
            response);
        self.assertEqual("200 OK", fakeServer.status)
        self.assertEqual(('Content-Length',"{0}".format(len(response[0]))), fakeServer.headers[1])
        self.assertEqual(('Access-Control-Allow-Origin',"*"), fakeServer.headers[2])
        self.assertEqual(('Content-Type',"text/xml"), fakeServer.headers[0])
