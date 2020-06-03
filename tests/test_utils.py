import datetime
import tempfile
import unittest
import os

import comet

class UtiltiesTest(unittest.TestCase):

    def testPaths(self):
        ref = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'comet'))
        self.assertEqual(comet.PACKAGE_PATH, ref)

    def testMakePath(self):
        ref = os.path.join(comet.PACKAGE_PATH, 'spam', 'ham.txt')
        self.assertEqual(comet.make_path('spam', 'ham.txt'), ref)

    def testMakeLabel(self):
        ref = 'V max'
        self.assertEqual(comet.make_label('v_max'), ref)

    def testMakeId(self):
        ref = 'nobody_expects_the_spanish_inquisition'
        self.assertEqual(comet.make_id('Nobody expects the spanish inquisition!'), ref)

    def testMakeIso(self):
        ts = 1423456789.8
        ref = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H-%M-%S')
        self.assertEqual(comet.make_iso(ts), ref)

    def testEscapeString(self):
        self.assertEqual(comet.escape_string('\r\n\t\\r\\n\\t'), '\\r\\n\\t\\\\r\\\\n\\\\t')

    def testUnescapeString(self):
        self.assertEqual(comet.unescape_string('\\\\r\\\\n\\\\t\\r\\n\\t\r\n\t'), '\\r\\n\\t\r\n\t\r\n\t')

    def testReplaceExt(self):
        values = (
            ('module.txt', '.dat', 'module.dat'),
            ('module', '.dat', 'module.dat'),
            ('module.txt', '', 'module'),
            (os.path.join('tmp', 'module.py'), '.ui', os.path.join('tmp', 'module.ui')),
        )
        for filename, ext, ref in values:
            self.assertEqual(comet.replace_ext(filename, ext), ref)

    def testSafeFilename(self):
        self.assertEqual(comet.safe_filename('1.5%+#$test@!.py'), '1.5_+_test_.py')

    def testAutoStep(self):
        self.assertEqual(comet.auto_step(0, 10, 1), 1)
        self.assertEqual(comet.auto_step(0, 10, -1), 1)
        self.assertEqual(comet.auto_step(10, 0, 1), -1)
        self.assertEqual(comet.auto_step(10, 0, -1), -1)
        self.assertEqual(comet.auto_step(-10, 10, -1), 1)
        self.assertEqual(comet.auto_step(-10, 10, 1), 1)
        self.assertEqual(comet.auto_step(10, -10, 1), -1)
        self.assertEqual(comet.auto_step(10, -10, -1), -1)

    def testSwitchDir(self):
        ref = os.path.realpath(os.getcwd())
        tmp = os.path.realpath(tempfile.gettempdir())
        with comet.switch_dir(tmp):
            self.assertEqual(os.path.realpath(os.getcwd()), tmp)
        self.assertEqual(os.path.realpath(os.getcwd()), ref)

if __name__ == '__main__':
    unittest.main()
