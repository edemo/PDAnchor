#!/usr/bin/python

import sys
import traceback

from xml.etree.ElementTree import XML

from wsgiref.simple_server import make_server

from Guard import Guard

import config
from Pkcs11Wrapper import Pkcs11Wrapper
from Reply import Reply
from syslog import syslog
from Exceptions import InputValidationException
from Messages import applicationInit, okStatus, notAcceptableStatus
from Crypto.Hash import SHA512

class record(object):
    def __init__(self,identity=None,name=None):
        self.id=identity
        self.mothername=name

excAnswer=getattr(config,'excAnswer',"<exception>{0}</exception>")

class Application:
    def __init__(self):
        syslog(applicationInit)
        self.guard = Guard()
        self.hasher = Pkcs11Wrapper()

    def computeReply(self, environ, request_body):
        ret = self.getRequestFromXml(request_body)
        requestor = self.getIpHash(environ)
        self.guard.check(requestor, ret)
        digest = self.hasher.hash((ret.id+ret.mothername).encode())
        message = "<hash>{0}</hash>".format(digest).encode()
        status = okStatus
        return Reply(status, message)

    def createErrorReply(self):
        syslog(traceback.format_exc())
        excInfo = sys.exc_info()
        message = excAnswer.format(excInfo[1], traceback.format_exc())
        status = notAcceptableStatus
        return Reply(status, message)

    def getRequestSize(self, environ):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        return request_body_size

    def application(self, environ, start_response):
        request_body_size = self.getRequestSize(environ)
        request_body = environ['wsgi.input'].read(request_body_size)
        try:
            reply = self.computeReply(environ, request_body)
        except:
            reply = self.createErrorReply()
        return reply.webReply(start_response)

    def getRequestFromXml(self,body):
        tree = XML(body)
        if 'request' != tree.tag:
            raise InputValidationException()
        r = record()
        for tag in tree.getchildren():
            if tag.tag in ['id','mothername']:
                setattr(r,tag.tag,tag.text)
        if None is getattr(r,'id',None):
            raise InputValidationException()            
        if None is getattr(r,'mothername',None):
            raise InputValidationException()            
        return r

    def getIpHash(self,environ):
        ip=environ["REMOTE_ADDR"]
        digest = SHA512.SHA512Hash(ip.encode()).hexdigest()
        return digest

    def run(self):
        httpd = make_server('localhost', 8080, self.application)
        while True:
            httpd.handle_request()

if __name__ == '__main__':
    Application().run()
