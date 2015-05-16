#!/usr/bin/python

import unittest
from Guard import Guard, IncorrectIdException, TooFrequentguestException

class GuardTest(unittest.TestCase):

    def setUp(self):
        self.guard=Guard()

    def test_Guard_checks_id_len(self):
        with self.assertRaises(IncorrectIdException):
            self.guard.check("aaa","1720313399")

    def test_Guard_checks_id_sum(self):
        with self.assertRaises(IncorrectIdException):
            self.guard.check("aab","17203133958")

    def test_Guard_checks_id_chars(self):
        with self.assertRaises(IncorrectIdException):
            self.guard.check("aac","A7203133958")

    def test_Guard_check(self):
        self.guard.check("aaa","17203133959")
        with self.assertRaises(TooFrequentguestException):
            self.guard.check("aaa","17203133959")

    def test_young_people_id(self):
        self.guard.check("bbb","19903146758")

    def test_very_young_people_id(self):
        self.guard.check("ccc","40412044075")

if __name__ == '__main__':
        unittest.main()

