#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
from Guard import Guard, IncorrectIdException, TooFrequentguestException, IncorrectNameException
from Application import record

class GuardTest(unittest.TestCase):

    def setUp(self):
        self.guard=Guard()

    def test_Guard_checks_id_len(self):
        with self.assertRaises(IncorrectIdException):
            self.guard.check("aaa",record("1720313399","testname"))

    def test_Guard_checks_id_sum(self):
        with self.assertRaises(IncorrectIdException):
            self.guard.check("aab",record("17203133958","testname"))

    def test_Guard_checks_id_chars(self):
        with self.assertRaises(IncorrectIdException):
            self.guard.check("aac",record("A7203133958","testname"))

    def test_Guard_check(self):
        self.guard.check("aaa",record("17203133959","testname"))
        with self.assertRaises(TooFrequentguestException):
            self.guard.check("aaa",record("17203133959","testname"))

    def test_young_people_id(self):
        self.guard.check("bbb",record("19903146758","testname"))

    def test_very_young_people_id(self):
        self.guard.check("ccc",record("40412044075","testname"))
        
    def test_mothername_should_not_contain_space(self):
        with self.assertRaises(IncorrectNameException):
            self.guard.checkName("contains space")

    def test_mothername_should_not_contain_anything_beyond_lower_ascii(self):
            for s in u""" ,?~!"#$%^&*()_+{}:|"<>?öüóőúéáűA\t\n""":
                name = u"contains%ssomething" % (s, )
                with self.assertRaises(IncorrectNameException):
                    self.guard.checkName(name)

    def test_mothername_should_not_be_too_long(self):
        with self.assertRaises(IncorrectNameException):
            self.guard.checkName("c"*51)

if __name__ == '__main__':
        unittest.main()

