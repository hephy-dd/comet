import re
import unittest

from comet.emulator.corvus.venus1 import Venus1Emulator


class Venus1Emulator(unittest.TestCase):

    def setUp(self):
        self.emulator = Venus1Emulator()
