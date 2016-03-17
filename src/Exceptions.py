#encoding: utf-8
from Messages import notPersonalId, noMotherName, invalidInput, waitAMinute,\
    outputLengthMismatch

class AnchorException(Exception):
    def __init__(self, why):
        msg = why
        super(Exception,self).__init__(msg)
    
class InputValidationException(AnchorException):
    def __init__(self):
        super(Exception,self).__init__(invalidInput)

class IncorrectIdException(AnchorException):
    def __init__(self, why):
        msg = notPersonalId.format(why)
        super(Exception,self).__init__(msg)

class IncorrectNameException(AnchorException):
    def __init__(self, why):
        msg = noMotherName.format(why)
        super(Exception,self).__init__(msg)

class TooFrequentguestException(AnchorException):
    def __init__(self):
        super(Exception,self).__init__(waitAMinute)

class IncorrectLengthException(AnchorException):
    def __init__(self, outputLength, response):
        msg = outputLengthMismatch.format(outputLength, len(response))
        super(Exception,self).__init__(msg)
