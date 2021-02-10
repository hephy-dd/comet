import datetime
import logging
import time

from comet.driver import Driver
from comet.driver import lock

from comet.driver.iec60488 import IEC60488
from comet.driver.iec60488 import opc_wait

__all__ = ['K2657A']

class K2657A(IEC60488):
    """Keithley Models 2657A High Power System SourceMeter."""

    class Beeper(Driver):

        @property
        def enable(self):
            return bool(float(self.resource.query('print(beeper.enable)')))

        @enable.setter
        @opc_wait
        def enable(self, value):
            self.resource.write(f'beeper.enable = {value:d}')

    class ErrorQueue(Driver):

        @property
        def count(self):
            return bool(float(self.resource.query('print(errorqueue.count)')))

        def next(self):
            return self.resource.query('print(errorqueue.next())').split('\t')

        @opc_wait
        def clear(self):
            self.resource.write('errorqueue.clear()')

    class Measure(Driver):

        def __init__(self, resource):
            super().__init__(resource)
            self.filter = self.Filter(resource)

        class Filter(Driver):

            @property
            def count(self):
                return int(self.resource.query('print(errorqueue.count)'))

            @count.setter
            @opc_wait
            def count(self, value):
                if 1 <= value <= 100:
                    self.resource.write(f'smua.measure.filter.count = {value:d}')
                raise ValueError("filter count out of range")

            @property
            def enable(self):
                return bool(int(self.resource.query('print(smua.measure.filter.enable)')))

            @enable.setter
            @opc_wait
            def enable(self, value):
                self.resource.write(f'smua.measure.filter.enable = {value:d}')

            @property
            def type(self):
                value = int(float(self.resource.query('print(smua.measure.filter.type)')))
                return {0: 'MOVING', 1: 'REPEAT', 2: 'MEDIAN'}[value]

            @type.setter
            @opc_wait
            def type(self, value):
                value = {'MOVING': 0, 'REPEAT': 1, 'MEDIAN': 2}[value]
                self.resource.write(f'smua.measure.filter.type = {value:d}')

        @property
        def nplc(self):
            return float(self.resource.query('print(smua.measure.nplc)'))

        @nplc.setter
        @opc_wait
        def nplc(self, value):
            if 0.001 <= value <=25.0:
                self.resource.write(f'smua.measure.nplc = {value:E}')
            raise ValueError("nplc out of range")

        def i(self):
            return float(self.resource.query('print(smua.measure.i())'))

        def v(self):
            return float(self.resource.query('print(smua.measure.v())'))

        def r(self):
            return float(self.resource.query('print(smua.measure.r())'))

        def p(self):
            return float(self.resource.query('print(smua.measure.p())'))

        def iv(self):
            results = self.resource.query('print(smua.measure.iv())').split(',')
            return float(results[0]), float(results[1])

    class Source(Driver):

        @property
        def compliance(self):
            return {'false': False, 'true': True}[self.resource.query('print(smua.source.compliance)')]

        OUTPUT_DCAMPS = 'DCAMPS'
        OUTPUT_DCVOLTS = 'DCVOLTS'

        @property
        def func(self):
            value = int(float(self.resource.query('print(smua.source.func)')))
            return {
                0: self.OUTPUT_DCAMPS,
                1: self.OUTPUT_DCVOLTS
            }[value]

        @func.setter
        @opc_wait
        def func(self, value):
            value = {
                self.OUTPUT_DCAMPS: 0,
                self.OUTPUT_DCVOLTS: 1
            }[value]
            self.resource.write(f'smua.source.func = {value:d}')

        @property
        def highc(self):
            return bool(float(self.resource.query('print(smua.source.highc)')))

        @highc.setter
        @opc_wait
        def highc(self, value):
            self.resource.write(f'smua.source.highc = {value:d}')

        @property
        def leveli(self):
            return float(self.resource.query('print(smua.source.leveli)'))

        @leveli.setter
        @opc_wait
        def leveli(self, value):
            self.resource.write(f'smua.source.leveli = {value:E}')

        @property
        def limiti(self):
            return float(self.resource.query('print(smua.source.limiti)'))

        @limiti.setter
        @opc_wait
        def limiti(self, value):
            self.resource.write(f'smua.source.limiti = {value:E}')

        @property
        def levelv(self):
            return float(self.resource.query('print(smua.source.levelv)'))

        @levelv.setter
        @opc_wait
        def levelv(self, value):
            self.resource.write(f'smua.source.levelv = {value:E}')

        @property
        def limitv(self):
            return float(self.resource.query('print(smua.source.limitv)'))

        @limitv.setter
        @opc_wait
        def limitv(self, value):
            self.resource.write(f'smua.source.limitv = {value:E}')

        OUTPUT_OFF = 'OFF'
        OUTPUT_ON = 'ON'
        OUTPUT_HIGH_Z = 'HIGH_Z'

        @property
        def output(self):
            value = int(float(self.resource.query('print(smua.source.output)')))
            return {
                0: self.OUTPUT_OFF,
                1: self.OUTPUT_ON,
                2: self.OUTPUT_HIGH_Z
            }[value]

        @output.setter
        @opc_wait
        def output(self, value):
            value = {
                self.OUTPUT_OFF: 0,
                self.OUTPUT_ON: 1,
                self.OUTPUT_HIGH_Z: 2
            }[value]
            self.resource.write(f'smua.source.output = {value:d}')

    def __init__(self, resource):
        super().__init__(resource)
        self.beeper = self.Beeper(resource)
        self.errorqueue = self.ErrorQueue(resource)
        self.measure = self.Measure(resource)
        self.source = self.Source(resource)

    SENSE_LOCAL = 'LOCAL'
    SENSE_REMOTE = 'REMOTE'
    SENSE_CALA = 'CALA'

    @property
    def sense(self):
        value = int(float(self.resource.query('print(smua.sense)')))
        return {
            0: self.SENSE_LOCAL,
            1: self.SENSE_REMOTE,
            2: self.SENSE_CALA
        }[value]

    @sense.setter
    @opc_wait
    def sense(self, value):
        value = {
            self.SENSE_LOCAL: 0,
            self.SENSE_REMOTE: 1,
            self.SENSE_CALA: 2
        }[value]
        self.resource.write(f'smua.sense = {value:d}')
