from comet.devices import IEC60488

__all__ = ['K2656A']

class K2656A(IEC60488):

    options = {
        'encoding': 'latin1',
        'read_termination': '\r',
    }

    Output = {0: 'OFF', 1: 'ON', 2: 'HIGH_Z'}

    def reset(self):
        self.resource().write('reset(true)')

    def output(self):
        return int(self.resource().query('print(smua.source.output)'))

    def setOutput(self, value):
        value = self.Output.get(value.upper(), 'OFF')
        self.resource().write('smua.source.output = smua.OUTPUT_{}'.format(value))

    def voltage(self):
        return self.resource().query('print(smua.source.levelv)')

    def setVoltage(self, value):
        self.resource().write('smua.source.levelv = {}'.format(value))

    def current(self):
        return self.resource().query('print(smua.source.leveli)')

    def setCurrent(self, value):
        self.resource().write('smua.source.leveli = {}'.format(value))

    def voltageLimit(self):
        return self.resource().query('print(smua.source.limitv)')

    def setVoltageLimit(self, value):
        return self.resource().write('smua.source.limitv = {}'.format(value))

    def currentLimit(self):
        return self.resource().query('print(smua.source.limiti)')

    def setCurrentLimit(self, value):
        return self.resource().write('smua.source.limiti = {}'.format(value))
