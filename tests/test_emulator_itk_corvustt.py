import re
import unittest

from comet.emulator.itk.corvustt import CorvusTTEmulator


class CorvusTTEmulatorTest(unittest.TestCase):

    def setUp(self):
        self.emulator = CorvusTTEmulator()
