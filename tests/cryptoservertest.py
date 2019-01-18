#encoding: utf-8
import unittest
from server import CryptoServerBase
import time
from enforce.decorators import runtime_validation

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

class FakeSyslog(object):
    def __init__(self):
        self.logged = []
    def syslog(self, msg):
        self.logged.append(msg)
    def openlog(self,*args, **kwargs):
        self.logged.append("openlog:{0} {1}".format(args, kwargs))

class FakeRequest(object):
    @runtime_validation
    def __init__(self,msg: bytes):
        self.msg = msg
    @runtime_validation
    def recv(self, length: int):
        return self.msg
    
    @runtime_validation
    def sendall(self, msg: bytes):
        self.sent=msg

class CryproServerTest(unittest.TestCase):

    def setUp(self):
        self.fixture = CryptoServerBase()
        self.fixture.syslog = FakeSyslog()

        self.fixture.opts = Bunch(
            module="/usr/lib/softhsm/libsofthsm2.so",
            pin="0000",
            keyid="d34db33f",
            mechanism="SHA512-RSA-PKCS",
            verbose=False,
            inputlength=512,
            outputlength=256,
            )
        self.fixture.request = FakeRequest(b"a"*512)

    def prepareFakeOutput(self, length):
        name = self.fixture.getTempName()
        f = open(name, "w")
        f.write("a" * length)
        f.close()
        return name

    def test_getTempName_returns_a_filename_which_can_be_created(self):
        name = self.fixture.getTempName()
        theFile = open(name, "w")
        self.assertTrue(hasattr(theFile, "read"))
        theFile.close()

    def test_commandLine_is_compiled_properly(self):
        commandLine = self.fixture.compileCommandLine("theName")
        self.assertEqual([
                'pkcs11-tool',
                '--module', '/usr/lib/softhsm/libsofthsm2.so',
                '-l',
                '-p', '0000',
                '-d', 'd34db33f',
                '-m', 'SHA512-RSA-PKCS',
                '-s',
                '-o', 'theName'
            ], commandLine)

    def test_wakeupCommandline_is_compiled_properly(self):
        commandLine = self.fixture.compileWakeupCommandLine()
        self.assertEqual([
                'pkcs11-tool',
                '--module', '/usr/lib/softhsm/libsofthsm2.so',
                '-O'
            ], commandLine)

    def test_runCommand_throws_exception_if_command_fails(self):
        with self.assertRaises(RuntimeError):
            self.fixture.runCommand(b"", ["/bin/false"])
            
    def test_runCommand_logs_stdout(self):
        self.fixture.runCommand(b"hello world", ["cat"])
        self.assertEqual(["b'hello world'","b''"],self.fixture.syslog.logged)

    def test_runCommand_logs_stderr(self):
        self.fixture.runCommand(b"hello world", ["dd", "of=/dev/null"])
        self.assertTrue(
            self.fixture.syslog.logged[-1].startswith(
                "b'0+1 records in\\n0+1 records out\\n11 bytes"))

    def test_runCommand_logs_catches_errors(self):
        with self.assertRaises(RuntimeError):
            self.fixture.runCommand(b"hello world", ["ajj"])
        self.assertEqual("problem running command: [Errno 2] No such file or directory: 'ajj': 'ajj'",self.fixture.syslog.logged[-1])

    def test_input_length_is_checked(self):
        self.fixture.request = FakeRequest(b"a"*511)
        with self.assertRaises(RuntimeError):
            self.fixture.receiveData()
        self.assertEqual(['input size mismatch: 511 bytes instead of 512 bytes'],self.fixture.syslog.logged)

    def test_good_input_length_is_accepted(self):
        result = self.fixture.receiveData()
        self.assertEqual(b"a"*512,result)

    def test_output_length_is_checked(self):
        name = self.prepareFakeOutput(511)
        with self.assertRaises(RuntimeError):
            self.fixture.getResponse(name)
        self.assertEqual(['command output size mismatch: 511 bytes instead of 256 bytes'],self.fixture.syslog.logged)

    def test_good_output_length_is_accepted(self):
        name = self.prepareFakeOutput(256)
        result = self.fixture.getResponse(name)
        self.assertEqual(b"a"*256,result)

    def test_handle_plays_it_all(self):
        self.fixture.handle()
        self.assertEqual(b'"\xdb$Y<{Yxe~\xb7(\x14\xd5V*\x91\xef\xeek\x9b\xc5\x9d\xcc\x04<G\x1cu\x08s\t\x9c\x05Rt\xf4\x15\xf6\x8bi\x9cW\x0c[\xaa#\xfa\xc3\xf7\x04\x19\x8c{F\x83\x9d\x14\xa2w\tla*\x8bJ\x17\xd2\x04 \xfd\x07\xe8\x1b\xed\xfd\x9dY\x96\xa1`6\'+\xc5,\x9b\x02\x1bZ\xad\xd5\x0b\xca4\xecdcL\xa0Y\x0b\xabz ?\x0e\xf1\xef\xa1\xd3Q\xcd\xa7\x1eg%\xe2B\xd8].\x14\x1c\';\xc6\xd3\x07\xd0\r\x14\xc2\xdd[\xeb}\xeb\x8f\x97Hp|\x0e\xaf\xf6\xa2\x05\x0c8 \x034\xa6\xe8\x106NHD\xa9\x8f\xb8i~@h\xc3\xefT\x7f\x05\x1d\xd4W\x92\x92\xfb\xd34\xe8\x984\xe4\xbf\xed3\x82\xf2y(\x0fo\xb3Q\xb9\xa9\xb8NR\xa3\x94(e\xcf\xa3\x18\x06\x93\xba\xf2\xba\xda\xed$\xda\xb0\xb3\x95#\xf3\xbdZ\xf2\xc1\x13\xae\xf77\xd2\xd8\xa3\x0f`\x94u\x8a\xf0\xd3\xe4!s\xa0\xc9\x9d#\xed\xb8\xdf\xd8S\x82\x8c\x0c\x0bb',
                         self.fixture.request.sent)

    def test_handle_logs_it_all(self):
        self.fixture.opts.verbose=1
        self.fixture.handle()
        self.assertEqual(6, len(self.fixture.syslog.logged))
        self.assertEqual("['pkcs11-tool', '--module', '/usr/lib/softhsm/libsofthsm2.so', '-O']",self.fixture.syslog.logged[0])
        self.assertEqual("b''",self.fixture.syslog.logged[1])
        self.assertIn('Using slot 0 with a present token ', str(self.fixture.syslog.logged[2]))
        self.assertTrue(self.fixture.syslog.logged[3].startswith(
            "['pkcs11-tool', '--module', '/usr/lib/softhsm/libsofthsm2.so', '-l', '-p', '0000', '-d', 'd34db33f', '-m', 'SHA512-RSA-PKCS', '-s', '-o',"))
        self.assertIn('Using signature algorithm SHA512-RSA-PKCS',self.fixture.syslog.logged[5])
        self.assertIn('Using slot 0 with a present token ',self.fixture.syslog.logged[5])

    def test_wake_up_tries_twice__raises_error_and_takes_time_if_fails(self):
        self.fixture.opts.module = 'badModule'
        t = time.time()
        with self.assertRaises(RuntimeError):
            self.fixture.wakeUpToken()
        now = time.time()
        self.assertGreaterEqual(now, t + 3)
        self.assertEqual(6, len(self.fixture.syslog.logged))
        self.assertEqual(self.fixture.syslog.logged[0], self.fixture.syslog.logged[3])
        self.assertEqual(self.fixture.syslog.logged[1], self.fixture.syslog.logged[4])
        self.assertEqual(self.fixture.syslog.logged[2], self.fixture.syslog.logged[5])

    def test_problems_result_in_error_message(self):
        self.fixture.request = FakeRequest(b"a"*511)
        self.fixture.handle()
        self.assertEqual(b"an error occured, try again later", self.fixture.request.sent)

    def test_problems_are_logged(self):
        self.fixture.request = FakeRequest(b"a"*511)
        self.fixture.handle()
        self.assertTrue('input size mismatch: 511 bytes instead of 512 bytes' in self.fixture.syslog.logged[-1])
