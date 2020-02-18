import tempfile
import unittest
import os

from comet.process import Thread, Process, ProcessManager, ProcessMixin

class ProcessTest(unittest.TestCase):

    def testThread(self):
        thread = Thread()
        self.assertEqual(thread.is_running(), True)
        thread.start()
        self.assertEqual(thread.is_running(), True)
        thread.stop()
        self.assertEqual(thread.is_running(), False)

    def testProcess(self):
        p = Process()
        self.assertEqual(p.started, None)
        self.assertEqual(p.finished, None)
        self.assertEqual(p.failed, None)
        p = Process(started=1, finished=2, failed=3)
        self.assertEqual(p.started, 1)
        self.assertEqual(p.finished, 2)
        self.assertEqual(p.failed, 3)

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
