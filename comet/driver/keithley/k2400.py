from typing import Dict, List, Tuple

from comet.driver import lock, Driver, Property
from comet.driver import IEC60488
from comet.driver.iec60488 import opc_wait, opc_poll

__all__ = ['K2400']

class Format(Driver):

    ELEMENT_VOLTAGE = 'VOLTAGE'
    ELEMENT_CURRENT = 'CURRENT'
    ELEMENT_RESISTANCE = 'RESISTANCE'
    ELEMENT_TIME = 'TIME'

    @property
    def elements(self):
        tr = {
            'VOLT': self.ELEMENT_VOLTAGE,
            'CURR': self.ELEMENT_CURRENT,
            'RES': self.ELEMENT_RESISTANCE,
            'TIME': self.ELEMENT_TIME
        }
        values = self.resource.query(':FORM:ELEM?').split(',')
        return list(map(lambda key: tr[key.strip()], values))

    @elements.setter
    @opc_wait
    def elements(self, value):
        tr = {
            self.ELEMENT_VOLTAGE: 'VOLT',
            self.ELEMENT_CURRENT: 'CURR',
            self.ELEMENT_RESISTANCE: 'RES',
            self.ELEMENT_TIME: 'TIME'
        }
        value = ','.join(map(lambda key: tr[key], value))
        self.resource.write(f':FORM:ELEM {value}')

class Route(Driver):

    @property
    def terminals(self):
        value = int(float(self.resource.query(':ROUT:TERM?')))
        return {'FRON': 'FRONT', 'REAR': 'REAR', 0: 'FRONT', 1: 'REAR'}[value]

    @terminals.setter
    @opc_wait
    def terminals(self, value):
        value = {'FRONT': 'FRON', 'REAR': 'REAR', 0: 'FRON', 1: 'REAR'}[value]
        self.resource.write(f':ROUT:TERM {value}')

class System(Driver):

    RSENSE_ON = 'ON'
    RSENSE_OFF = 'OFF'

    class Beeper(Driver):

        @Property(values={False: 0, True: 1})
        def status(self) -> int:
            result = self.resource.query(':SYST:BEEP:STAT?')
            return int(result)

        @status.setter
        @opc_wait
        def status(self, value: int):
            self.resource.write(f':SYST:BEEP:STAT {value:d}')

    def __init__(self, resource):
        super().__init__(resource)
        self.beeper = self.Beeper(resource)

    @property
    def error(self) -> Tuple[int, str]:
        """Returns current instrument error.
        >>> system.error
        (0, "No error")
        """
        result = self.resource.query(':SYST:ERR?').split(',')
        return int(result[0]), result[1].strip().strip('"')

    @Property(values={RSENSE_OFF: 0, RSENSE_ON: 1})
    def rsense(self) -> int:
        return int(self.resource.query(':SYST:RSEN?'))

    @rsense.setter
    @opc_wait
    def rsense(self, value: int):
        self.resource.write(f':SYST:RSEN {value:d}')

class Source(Driver):

    class Function(Driver):

        MODE_CURRENT = 'CURRENT'
        MODE_VOLTAGE = 'VOLTAGE'
        MODE_MEMORY = 'MEMORY'

        @Property(values={MODE_CURRENT: 'CURR', MODE_VOLTAGE: 'VOLT', MODE_MEMORY: 'MEM'})
        def mode(self) -> str:
            return self.resource.query(':SOUR:FUNC:MODE?')

        @mode.setter
        @opc_wait
        def mode(self, value: str):
            self.resource.write(f':SOUR:FUNC:MODE {value}')

    class Voltage(Driver):

        class Range(Driver):

            @property
            def auto(self) -> bool:
                return bool(int(self.resource.query(':SOUR:VOLT:RANG:AUTO?')))

            @auto.setter
            @opc_wait
            def auto(self, value: bool):
                self.resource.write(f':SOUR:VOLT:RANG:AUTO {value:d}')

            @property
            def level(self) -> float:
                return float(self.resource.query(':SOUR:VOLT:RANG?'))

            @level.setter
            @opc_wait
            def level(self, value: float):
                self.resource.write(f':SOUR:VOLT:RANG {value:E}')

        class Protection(Driver):

            @property
            def level(self) -> float:
                """Returns over voltage limit."""
                return float(self.resource.query(':SOUR:VOLT:PROT:LEV?'))

            @level.setter
            @opc_wait
            def level(self, value: float):
                """Set over voltage limit for V-Source."""
                self.resource.write(f':SOUR:VOLT:PROT:LEV {value:E}')

        def __init__(self, resource):
            super().__init__(resource)
            self.range = self.Range(resource)
            self.protection = self.Protection(resource)

        @property
        def level(self) -> float:
            return float(self.resource.query(':SOUR:VOLT:LEV?'))

        @level.setter
        @opc_wait
        def level(self, value: float):
            self.resource.write(f':SOUR:VOLT:LEV {value:E}')

    class Current(Driver):

        class Range(Driver):

            @property
            def auto(self) -> bool:
                return bool(int(self.resource.query(':SOUR:CURR:RANG:AUTO?')))

            @auto.setter
            @opc_wait
            def auto(self, value: bool):
                self.resource.write(f':SOUR:CURR:RANG:AUTO {value:d}')

            @property
            def level(self) -> float:
                return float(self.resource.query(':SOUR:CURR:RANG?'))

            @level.setter
            @opc_wait
            def level(self, value: float):
                self.resource.write(f':SOUR:CURR:RANG {value:E}')

        def __init__(self, resource):
            super().__init__(resource)
            self.range = self.Range(resource)

        @property
        def level(self) -> float:
            return float(self.resource.query(':SOUR:CURR:LEV?'))

        @level.setter
        @opc_wait
        def level(self, value: float):
            self.resource.write(f':SOUR:CURR:LEV {value:E}')

    def __init__(self, resource):
        super().__init__(resource)
        self.function = self.Function(resource)
        self.voltage = self.Voltage(resource)
        self.current = self.Current(resource)

    @opc_wait
    def clear(self):
        """Turn output source off when in idle."""
        self.resource.write(':SOUR:CLE')

class Sense(Driver):

    class Average(Driver):

        TCONTROL_MOVING = 'MOVING'
        TCONTROL_REPEAT = 'REPEAT'

        @property
        def tcontrol(self) -> str:
            key = int(float(self.resource.query(':SENS:AVER:TCON?')))
            return {
                0: self.TCONTROL_MOVING,
                1: self.TCONTROL_REPEAT
            }.get(key)

        @tcontrol.setter
        @opc_wait
        def tcontrol(self, value: str):
            value = {
                self.TCONTROL_MOVING: 'MOV',
                self.TCONTROL_REPEAT: 'REP'
            }[value]
            self.resource.write(f':SENS:AVER:TCON {value:s}')

        @Property(minimum=1, maximum=100)
        def count(self) -> int:
            return int(float(self.resource.query(':SENS:AVER:COUN?')))

        @count.setter
        @opc_wait
        def count(self, value: int):
            self.resource.write(f':SENS:AVER:COUN {value:d}')

        @Property(values={False: 0, True: 1})
        def state(self) -> int:
            return int(float(self.resource.query(':SENS:AVER:STAT?')))

        @state.setter
        @opc_wait
        def state(self, value: int):
            self.resource.write(f':SENS:AVER:STAT {value:d}')

    class Current(Driver):

        class Protection(Driver):

            @property
            def level(self) -> float:
                """Returns current compliance limit."""
                return float(self.resource.query(':SENS:CURR:PROT:LEV?'))

            @level.setter
            @opc_wait
            def level(self, value: float):
                """Set current compliance limit for V-Source."""
                self.resource.write(f':SENS:CURR:PROT:LEV {value:E}')

            @property
            def tripped(self) -> bool:
                """Returns True if in current compliance."""
                return bool(int(self.resource.query(':SENS:CURR:PROT:TRIP?')))

            @property
            def rsyncronize(self) -> bool:
                """Returns True if range syncronization enabled."""
                return bool(int(self.resource.query(':SENS:CURR:PROT:RSYN?')))

            @rsyncronize.setter
            @opc_wait
            def rsyncronize(self, value: bool):
                """Enable or disable measure and compliance range syncronization."""
                self.resource.write(f':SENS:CURR:PROT:RSYN {value:d}')

        class Range(Driver):

            @property
            def auto(self) -> bool:
                return bool(int(self.resource.query(':SENS:CURR:RANG:AUTO?')))

            @auto.setter
            @opc_wait
            def auto(self, value: bool):
                self.resource.write(f':SENS:CURR:RANG:AUTO {value:d}')

        def __init__(self, resource):
            super().__init__(resource)
            self.protection = self.Protection(resource)
            self.range = self.Range(resource)

    class Voltage(Driver):

        class Protection(Driver):

            @property
            def level(self) -> float:
                """Returns voltage compliance limit."""
                return float(self.resource.query(':SENS:VOLT:PROT:LEV?'))

            @level.setter
            @opc_wait
            def level(self, value: float):
                """Set voltage compliance limit for V-Source."""
                self.resource.write(f':SENS:VOLT:PROT:LEV {value:E}')

            @property
            def tripped(self) -> bool:
                """Returns True if in voltage compliance."""
                return bool(int(self.resource.query(':SENS:VOLT:PROT:TRIP?')))

            @property
            def rsyncronize(self) -> bool:
                """Returns True if range syncronization enabled."""
                return bool(int(self.resource.query(':SENS:VOLT:PROT:RSYN?')))

            @rsyncronize.setter
            def rsyncronize(self, value: bool):
                """Enable or disable measure and compliance range syncronization."""
                self.resource.write(f':SENS:VOLT:PROT:RSYN {value:d}')

        def __init__(self, resource):
            super().__init__(resource)
            self.protection = self.Protection(resource)

    def __init__(self, resource):
        super().__init__(resource)
        self.average = self.Average(resource)
        self.current = self.Current(resource)
        self.voltage = self.Voltage(resource)

class PowerMixin:

    @Property(values={False: 0, True: 1})
    def output(self) -> bool:
        """Returns True if output enabled.
        >>> instr.output
        True
        """
        return int(self.resource.query(':OUTP:STAT?'))

    @output.setter
    @opc_wait
    def output(self, value: int):
        """Enable or disable output.
        >>> instr.output = True
        """
        self.resource.write(f':OUTP:STAT {value:d}')

class MeasureMixin:

    @opc_poll
    def init(self):
        """Initiate a measurement.
        >>> instr.init()
        """
        self.resource.write(':INIT')

    def fetch(self) -> List[float]:
        """Returns the latest available reading as list.
        >>> instr.fetch()
        [-4.32962079e-05, 0.0, 0.0, ...]
        """
        result = self.resource.query(':FETC?')
        return list(map(float, result.split(',')))

    def read(self) -> List[Dict[str, float]]:
        """High level command to perform a singleshot measurement. It resets the
        trigger model, initiates it, and fetches a new reading.
        >>> instr.read()
        [-4.32962079e-05, 0.0, 0.0, ...]
        """
        result = self.resource.query(':READ?')
        return list(map(float, result.split(',')))

class K2400(IEC60488, MeasureMixin, PowerMixin):
    """Keithley Series 2400 Source Meter Unit."""

    def __init__(self, resource, **kwargs):
        super().__init__(resource, **kwargs)
        self.format = Format(resource)
        self.route = Route(resource)
        self.system = System(resource)
        self.source = Source(resource)
        self.sense = Sense(resource)
