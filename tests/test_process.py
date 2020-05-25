import tempfile
import unittest
import os

from comet.process import Process, ProcessManager, ProcessMixin

class ProcessTest(unittest.TestCase):

    def testProcessManager(self):
        p = Process()
        m = ProcessManager()
        self.assertEqual(m.ValueType , type(p))
        m.add("process", p)
        self.assertEqual(m.get("process"), p)

    def testProcessMixin(self):
        class C(ProcessMixin): pass
        p = Process()
        c = C()
        c.processes.add("process", p)
        self.assertEqual(c.processes.get("process"), p)

if __name__ == '__main__':
    unittest.main()
