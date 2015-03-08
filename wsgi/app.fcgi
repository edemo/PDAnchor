#!/usr/bin/python

from Application import Application

app = Application()

def application(environ, start_response):
	return app.application(environ, start_response)
