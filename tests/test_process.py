import tempfile
import unittest
import os

from qutie.application import CoreApplication

from comet.process import Process, ProcessManager, ProcessMixin

class ProcessTest(unittest.TestCase):

    def testProcess(self):
        app = CoreApplication()
        def run(process):
            process.set('value', True)
            process.emit('event')
        p = Process(target=run)
        p.started = lambda: p.set('started', True)
        p.finished = lambda: p.set('finished', True)
        p.failed = lambda e, tb: p.set('failed', e)
        p.event = lambda: p.set('event', True)
        p.start()
        app.qt.processEvents()
        p.stop()
        p.join()
        self.assertEqual(p.get('value'), True)
        self.assertEqual(p.get('started'), True)
        self.assertEqual(p.get('finished'), True)
        self.assertEqual(p.get('failed'), None)
        self.assertEqual(p.get('event'), True)

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
