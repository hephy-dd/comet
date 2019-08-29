import time
import unittest

from comet.settings import Settings

class VolatileSettings(Settings):

    default_filename = 'settings-test-volatile.json'

class VolatileSettingsTest(unittest.TestCase):

    organization = 'HEPHY'
    application = 'comet'
    persistent = False
    Context = VolatileSettings

    @classmethod
    def setUpClass(cls):
        cls.settings = cls.Context(cls.organization, cls.application, cls.persistent)

    @classmethod
    def tearDownClass(cls):
        cls.settings.clear()

    def testSettingsAttrs(self):
        self.assertEqual(self.settings.organization, self.organization)
        self.assertEqual(self.settings.application, self.application)
        self.assertEqual(self.settings.persistent, self.persistent)

    def testSettings(self):
        with self.settings as settings:
            self.assertEqual(settings, {})
            settings['operators'] = ['Monty', 'John']
        with self.settings as settings:
            self.assertEqual(settings, {'operators': ['Monty', 'John']})

class PersistentSettings(Settings):

    default_filename = 'settings-test-persistent.json'

class PersistentSettingsTest(VolatileSettingsTest):

    persistent = True
    Context = PersistentSettings

if __name__ == '__main__':
    unittest.main()
