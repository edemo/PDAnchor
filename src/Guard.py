#!/usr/bin/python
#coding=UTF-8

from time import time
import config
import re

HUNDRED_YEARS = 1000000
LAST_DAY_OF_1996 = 961231

class IncorrectIdException(Exception):
    def __init__(self, why):
        msg = "Ez nem személyi szám: {0}".format(why)
        super(Exception,self).__init__(msg)

class IncorrectNameException(Exception):
    def __init__(self, why):
        msg = "Ez nem anyja neve: {0}".format(why)
        super(Exception,self).__init__(msg)

class TooFrequentguestException(Exception):
    def __init__(self):
        super(Exception,self).__init__("Várj még egy percet")

class Guard():
    conns = {}

    def check(self, caller, req):
        self.checkName(req.mothername)
        self.checkID(req.id)
        self.checkCaller(caller)
        return True

    def checkName(self, motherName):
        if re.compile(r"[^abcdefghijklmnopqrstuvwxyz]").search(motherName):
            raise IncorrectNameException("nem csupa kisbetu")
        if len(motherName) > 50:
            raise IncorrectNameException("túl hosszú")

    def checkCaller(self, caller):
        now = time()
        if self.conns.has_key(caller):
            if ( self.conns[caller] > now - getattr(config,"minimum_time",60) ):
                raise TooFrequentguestException()
        self.conns[caller] = now

    def checkIdLen(self, userID):
        if len(userID) != 11:
            raise IncorrectIdException("nem 11 karakter")

    def isYoungSumma(self, userID):
        birthday = int(userID[1:7])
        firstNumber = int(userID[0])
        if firstNumber == 3 or firstNumber == 4:
            birthday = birthday + HUNDRED_YEARS
        if birthday <= LAST_DAY_OF_1996:
            return False
        return True

    def computeOldSumma(self, userID):
        summa = 0
        pos = 1
        for i in userID[:-1]:
            summa += int(i) * pos
            pos += 1
        return summa

    def checkAllDomain(self, userID):
        for i in userID:
            self.checkDomain(i)

    def computeYoungSumma(self, userID):
        youngsumma = 0
        pos = 1
        for i in userID[:-1]:
            youngsumma += int(i) * (11 - pos)
            pos += 1
        return youngsumma

    def computeChecksum(self, userID):
        if self.isYoungSumma(userID):
            return self.computeYoungSumma(userID)
        return self.computeOldSumma(userID)

    def inputCheck(self, userID):
        self.checkIdLen(userID)
        self.checkAllDomain(userID)

    def checkID(self,userID):
        self.inputCheck(userID)
        lastCh=userID[-1]
        controlsum = self.computeChecksum(userID)
        if (controlsum % 11) != int(lastCh):
                raise IncorrectIdException("nem stimmel az összeg: {0}".format(controlsum % 11))

    def checkDomain(self, ch):
            if not ( ch in "1234567890"):
                raise IncorrectIdException("nem számokból áll")
