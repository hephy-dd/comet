import datetime
import tempfile
import unittest
import os

import comet

class UtiltiesTest(unittest.TestCase):

    def test_paths(self):
        ref = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'comet'))
        self.assertEqual(comet.PACKAGE_PATH, ref)

    def test_make_path(self):
        ref = os.path.join(comet.PACKAGE_PATH, 'spam', 'ham.txt')
        self.assertEqual(comet.make_path('spam', 'ham.txt'), ref)

    def test_make_label(self):
        ref = 'V max'
        self.assertEqual(comet.make_label('v_max'), ref)

    def test_make_id(self):
        ref = 'nobody_expects_the_spanish_inquisition'
        self.assertEqual(comet.make_id('Nobody expects the spanish inquisition!'), ref)

    def test_make_iso(self):
        ts = 1423456789.8
        ref = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H-%M-%S')
        self.assertEqual(comet.make_iso(ts), ref)

    def test_escape_string(self):
        self.assertEqual(comet.escape_string('\r\n\t\\r\\n\\t'), '\\r\\n\\t\\\\r\\\\n\\\\t')

    def test_unescape_string(self):
        self.assertEqual(comet.unescape_string('\\\\r\\\\n\\\\t\\r\\n\\t\r\n\t'), '\\r\\n\\t\r\n\t\r\n\t')

    def test_replace_ext(self):
        values = (
            ('module.txt', '.dat', 'module.dat'),
            ('module', '.dat', 'module.dat'),
            ('module.txt', '', 'module'),
            (os.path.join('tmp', 'module.py'), '.ui', os.path.join('tmp', 'module.ui')),
        )
        for filename, ext, ref in values:
            self.assertEqual(comet.replace_ext(filename, ext), ref)

    def test_safe_filename(self):
        self.assertEqual(comet.safe_filename('1.5%+#$test@!.py'), '1.5_+_test_.py')

    def test_auto_step(self):
        self.assertEqual(comet.auto_step(0, 10, 1), 1)
        self.assertEqual(comet.auto_step(0, 10, -1), 1)
        self.assertEqual(comet.auto_step(10, 0, 1), -1)
        self.assertEqual(comet.auto_step(10, 0, -1), -1)
        self.assertEqual(comet.auto_step(-10, 10, -1), 1)
        self.assertEqual(comet.auto_step(-10, 10, 1), 1)
        self.assertEqual(comet.auto_step(10, -10, 1), -1)
        self.assertEqual(comet.auto_step(10, -10, -1), -1)

    def test_switch_dir(self):
        ref = os.path.realpath(os.getcwd())
        tmp = os.path.realpath(tempfile.gettempdir())
        with comet.switch_dir(tmp):
            self.assertEqual(os.path.realpath(os.getcwd()), tmp)
        self.assertEqual(os.path.realpath(os.getcwd()), ref)

if __name__ == '__main__':
    unittest.main()
