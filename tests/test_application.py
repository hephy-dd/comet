import unittest

from comet.application import Application

class ApplicationTest(unittest.TestCase):

    def test_application(self):
        app = Application(name="comet")
        self.assertEqual(app.name, "comet")
        self.assertEqual(app.title, "")
        self.assertEqual(app.version, "")
        app.title = "Sample"
        self.assertEqual(app.title, "Sample")
        app.version = "1.2.3"
        self.assertEqual(app.version, "1.2.3")
        app.name = "test"
        self.assertEqual(app.qt.applicationName(), "test")

if __name__ == '__main__':
    unittest.main()
