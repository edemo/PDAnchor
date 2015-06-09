#!/usr/bin/python
#coding=UTF-8

from time import time

HUNDRED_YEARS = 1000000
LAST_DAY_OF_1996 = 961231

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


    def checkIdLen(self, userID):
        if len(userID) != 11:
            raise IncorrectIdException("nem 11 karakter")

    def chooseSumma(self, userID, summa, youngsumma):
        birthday = int(userID[1:7])
        firstNumber = int(userID[0])
        if firstNumber == 3 or firstNumber == 4:
            birthday = birthday + HUNDRED_YEARS
        if birthday <= LAST_DAY_OF_1996:
            controlsum = summa
        else:
            controlsum = youngsumma
        return controlsum

    def computeSums(self, userID):
        summa = 0
        youngsumma = 0
        pos = 1
        for i in userID[:-1]:
            self.checkDomain(i)
            summa += int(i) * pos
            youngsumma += int(i) * (11 - pos)
            pos += 1
        return summa, youngsumma

    def computeChecksum(self, userID):
        summa, youngsumma = self.computeSums(userID)
        controlsum = self.chooseSumma(userID, summa, youngsumma)
        return controlsum

    def checkID(self,userID):
        self.checkIdLen(userID)
        lastCh=userID[-1]
        self.checkDomain(lastCh)
        controlsum = self.computeChecksum(userID)
        if (controlsum % 11) != int(lastCh):
                raise IncorrectIdException("nem stimmel az összeg: {0}".format(controlsum % 11))

    def checkDomain(self, ch):
            if not ( ch in "1234567890"):
                raise IncorrectIdException("nem számokból áll")
