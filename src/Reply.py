class Reply(object):
    def __init__(self,status,message):
        self.status = status
        self.message = message

    def addResponseHeaders(self):
        response_headers = [('Content-Type', 'text/xml'), ('Content-Length', str(len(self.message))), 
            ('Access-Control-Allow-Origin', '*')]
        return response_headers

    def webReply(self, start_response):
        response_headers = self.addResponseHeaders()
        start_response(self.status, response_headers)
        return [self.message]
