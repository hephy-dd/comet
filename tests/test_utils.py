import tempfile
import unittest
import os

from comet import utils

class UtiltiesTest(unittest.TestCase):

    def testPaths(self):
        ref = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'comet'))
        self.assertEqual(utils.PACKAGE_PATH, ref)

    def testMakePath(self):
        ref = os.path.join(utils.PACKAGE_PATH, 'spam', 'ham.txt')
        self.assertEqual(utils.make_path('spam', 'ham.txt'), ref)

    def testMakeLabel(self):
        ref = 'V max'
        self.assertEqual(utils.make_label('v_max'), ref)

    def testMakeId(self):
        ref = 'nobody_expects_the_spanish_inquisition'
        self.assertEqual(utils.make_id('Nobody expects the spanish inquisition!'), ref)

    def testReplaceExt(self):
        values = (
            ('module.txt', '.dat', 'module.dat'),
            ('module', '.dat', 'module.dat'),
            ('module.txt', '', 'module'),
            (os.path.join('tmp', 'module.py'), '.ui', os.path.join('tmp', 'module.ui')),
        )
        for filename, ext, ref in values:
            self.assertEqual(utils.replace_ext(filename, ext), ref)

    def testSwitchDir(self):
        ref = os.getcwd()
        tmp = tempfile.gettempdir()
        with utils.switch_dir(tmp):
            self.assertEqual(os.getcwd(), tmp)
        self.assertEqual(os.getcwd(), ref)

if __name__ == '__main__':
    unittest.main()
