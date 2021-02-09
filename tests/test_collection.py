import unittest

from comet.collection import Collection

class CollectionTest(unittest.TestCase):

    def testCollection(self):
        c = Collection()
        self.assertEqual(c.ValueType, None)
        self.assertEqual(len(c), 0)
        self.assertEqual(list(c.keys()), [])
        self.assertEqual(list(c.values()), [])
        self.assertEqual(list(c.items()), [])
        key, value = "item", 42
        c.add(key, value)
        self.assertRaises(KeyError, c.add, key, value)
        self.assertEqual(len(c), 1)
        self.assertEqual(list(c.keys()), [key])
        self.assertEqual(list(c.values()), [value])
        self.assertEqual(list(c.items()), [(key, value)])
        self.assertEqual(c.get(key), value)
        self.assertRaises(KeyError, c.get, "foo")

if __name__ == '__main__':
    unittest.main()
