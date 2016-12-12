#encoding: utf-8
import unittest
from program import Program
from cryptoservertest import FakeSyslog

class programTest(unittest.TestCase):

    def setUp(self):
        self.fixture = Program(1, 1, "-d 1".split(' '), FakeSyslog())

    def test_default_options_are_set(self):
        fixture = self.fixture
        self.assertEqual('1', fixture.opts.keyid)
        self.assertEqual(None, fixture.opts.verbose)
        self.assertEqual('0000', fixture.opts.pin)
        self.assertEqual('/usr/lib/opensc-pkcs11.so', fixture.opts.module)
        self.assertEqual(None, fixture.opts.environment)
        self.assertEqual('localhost', fixture.opts.host)
        self.assertEqual(256, fixture.opts.inputlength)
        self.assertEqual(256, fixture.opts.outputlength)
        self.assertEqual('SHA512-RSA-PKCS', fixture.opts.mechanism)
        self.assertEqual(9999, fixture.opts.port)

    def test_keyid_can_be_given_with_d(self):
        self.fixture.parseArgs("-d 2222".split(' '))
        self.assertEqual('2222', self.fixture.opts.keyid)

    def test_verbose_can_be_set_with_v(self):
        self.fixture.parseArgs("-d 1 -v".split(' '))
        self.assertEqual(1, self.fixture.opts.verbose)

    def test_verbose_level_is_increased_with_all_v(self):
        self.fixture.parseArgs("-d 1 -vvvv".split(' '))
        self.assertEqual(4, self.fixture.opts.verbose)

    def test_outputlength_is_set_by_o(self):
        self.fixture.parseArgs("-d 1 -o 511".split(' '))
        self.assertEqual(511, self.fixture.opts.outputlength)

