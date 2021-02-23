import unittest
import random

from comet.resource import Resource
from comet.driver import Driver

from comet.driver.keithley import K2410

from .test_driver_k2400 import K2400Test

class K2410Test(K2400Test):

    driver_type = K2410

if __name__ == '__main__':
    unittest.main()
