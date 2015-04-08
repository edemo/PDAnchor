#!/usr/bin/python
#coding=UTF-8

from time import time

class IncorrectIdException(Exception):
    def __init__(self, why):
        msg = "Ez nem személyi szám: {0}".format(why)
        super(Exception,self).__init__(msg)

class TooFrequentguestException(Exception):
    def __init__(self):
        super(Exception,self).__init__("Várj még egy percet")

class Guard():
    conns = {}

    def check(self, caller, userID):
        self.checkID(userID)
        self.checkCaller(caller)
        return True

    def checkCaller(self, caller):
        now = time()
        if self.conns.has_key(caller):
            if ( self.conns[caller] > now - 60 ):
                raise TooFrequentguestException()
        self.conns[caller] = now

    def checkID(self,userID):
        sum = 0
        pos = 1
        if len(userID) != 11:
            raise IncorrectIdException("nem 11 karakter")
        for i in userID[:-1]:
            self.checkDomain(i)
            sum += int(i)*pos
            pos += 1
        lastCh=userID[-1]
        self.checkDomain(lastCh)
        if (sum % 11) != int(lastCh):
                raise IncorrectIdException("nem stimmel az összeg: {0}".format(sum % 11))

    def checkDomain(self, ch):
            if not ( ch in "1234567890"):
                   raise IncorrectIdException("nem számokból áll")
