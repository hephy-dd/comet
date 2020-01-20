import tempfile
import unittest
import os

from comet.application import Application

class ApplicationTest(unittest.TestCase):

    def testApplication(self):
        a = Application(name="comet")
        self.assertEqual(a.name, "comet")
        self.assertEqual(a.title, "")
        self.assertEqual(a.version, "")
        a.title = "Sample"
        self.assertEqual(a.title, "Sample")
        a.version = "1.2.3"
        self.assertEqual(a.version, "1.2.3")
        a.name = "test"
        self.assertEqual(a.qt.applicationName(), "test")

if __name__ == '__main__':
    unittest.main()
