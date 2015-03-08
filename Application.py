#!/usr/bin/python

import sys
import md5

from xml.etree.ElementTree import XML

from wsgiref.simple_server import make_server

from Guard import Guard
from Hasher import Hasher

class InputValidationException(Exception):
    def __init__(self):
        super().__init__("Invalid input")

class Application:
    def __init__(self):
        self.guard = Guard()
        self.hasher = Hasher()

    def application(self, environ, start_response):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        try:
            id = self.getIdFromXml(request_body)
            requestor = self.getIpHash(environ)
            self.guard.check(requestor,id)
            hash = self.hasher.hash(id)
            reply = "<hash>{0}</hash>".format(hash)
            status = '200 OK'
        except:
            reply = "<exception>{0}</exception>".format(sys.exc_info()[1])
            status = "406 Not Acceptable"
        response_headers = [('Content-Type', 'text/html'),
            ('Content-Length', str(len(reply))),
            ('Access-Control-Allow-Origin', '*')]
        start_response(status, response_headers)
        return [reply]

    def getIdFromXml(self,body):
        tree = XML(body)
        if 'id' != tree.tag:
            raise InputValidationException()
        return tree.text

    def getIpHash(self,environ):
        ip=environ["REMOTE_ADDR"]
        hash = md5.new(ip).hexdigest()
        return hash

    def run(self):
        httpd = make_server('localhost', 8080, self.application)
        while True:
            httpd.handle_request()


if __name__ == '__main__':
    Application().run()

