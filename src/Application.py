#!/usr/bin/python

import sys
import md5
import traceback

from xml.etree.ElementTree import XML

from wsgiref.simple_server import make_server

from Guard import Guard

import config
from Pkcs11Wrapper import Pkcs11Wrapper

excAnswer=getattr(config,'excAnswer',"<exception>{0}</exception>")

class InputValidationException(Exception):
    def __init__(self):
        super().__init__("Invalid input")

class Application:
    def __init__(self):
        self.guard = Guard()
        self.hasher = Pkcs11Wrapper.getInstance()

    def application(self, environ, start_response):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        try:
            personalID = self.getIdFromXml(request_body)
            requestor = self.getIpHash(environ)
            self.guard.check(requestor,personalID)
            digest = self.hasher.hash(personalID)
            reply = "<hash>{0}</hash>".format(digest)
            status = '200 OK'
        except:
            excInfo=sys.exc_info()
            reply = excAnswer.format(excInfo[1],traceback.format_exc())
            status = "406 Not Acceptable"
        response_headers = [('Content-Type', 'text/xml'),
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
        digest = md5.new(ip).hexdigest()
        return digest

    def run(self):
        httpd = make_server('localhost', 8080, self.application)
        while True:
            httpd.handle_request()


if __name__ == '__main__':
    Application().run()

