#!/usr/bin/python

import syslog
from Application import Application

app = Application()

def application(environ, start_response):
	syslog.syslog("app start")
	return app.application(environ, start_response)
