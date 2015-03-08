#!/usr/bin/python
#coding=UTF-8

import sqlite3
from time import time

class IncorrectIdException(Exception):
    def __init__(self, why):
        msg = "Ez nem személyi szám: {0}".format(why)
        super(Exception,self).__init__(msg)

class TooFrequentguestException(Exception):
    def __init__(self):
        super(Exception,self).__init__("Várj még egy percet")

class Guard():
    conn = None

    def __init__(self):
        self.getConn()

    @classmethod
    def getConn(klass):
        if klass.conn == None:
            klass.conn=sqlite3.connect('/var/run/PDAnchor/guard.db')
            now = time()
            klass.conn.execute("delete from log")
        return klass.conn
    def check(self, caller, userID):
        self.checkID(userID)
        self.checkCaller(caller)
        return True

    def checkCaller(self, caller):
        now = time()
        c=self.conn.cursor()
        c.execute("select count(*) from log where id = ? and ts > ?",(caller, now - 60))
        r = c.fetchone()
        if r[0]  != 0:
            c.close()
            raise TooFrequentguestException()
        c.execute("insert into log values (?,?)",(caller,now))
        c.close()

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
