import os
import unittest

from comet.emulator.tcpsocket import split_messages

class TCPSocketTest(unittest.TestCase):

    def test_split_messages(self):
        messages = [
            ('', []),
            ('\r\n\r\n', []),
            ('\n', []),
            ('\nfoo\n', ['foo']),
            ('foo\r\nbar\r\n\r\n', ['foo', 'bar']),
            ('foo\nbar\n\n', ['foo', 'bar']),
        ]
        for token, reference in messages:
            result = list(split_messages(token, '\n'))
            self.assertEqual(result, reference)
