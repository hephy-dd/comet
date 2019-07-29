from lantz.core import Action, Feat, DictFeat, ureg
from lantz.core.messagebased import MessageBasedDriver
from lantz.core.errors import InstrumentError

class ITC(MessageBasedDriver):
    """Lantz driver for interfacing with ITS devices from CTS."""

    analog_channel_codes = {
        1: 'A0', 2: 'A1', 3: 'A2', 4: 'A3',
        5: 'A4', 6: 'A5', 7: 'A6', 8: 'A7',
        9: 'A8', 10: 'A9', 11: 'A:', 12: 'A;',
        13: 'A<', 14: 'A=', 15: 'A>', 16: 'A?',
    }
    """Mapping analog channel numbers to channel IDs."""

    warning_messages = {
        '\x01': "Wassernachfüllen",
        '\x02': "Temp. Toleranzband Oben",
        '\x03': "Temp. Toleranzband Unten",
        '\x04': "Feuchte Toleranzband Oben",
        '\x05': "Feuchte Toleranzband Unten",
        '\x06': "Wasserbad Abschlaemmen",
    }

    error_messages = {
        '\x31': "Temperatur Grenze Min 08-B1",
        '\x32': "Temperatur Grenze Max 08-B1",
        '\x33': "Temp. Begrenzer Pruefr. 01-F1.1",
        '\x34': "TK Vent. Pruefr. 02-F2.1",
        '\x35': "Pruefgutschutz Max 09-A1",
        '\x37': "Ueberdruck Kuehlung 03-B40",
        '\x38': "Feuchtegrenze Min 08-B2",
        '\x39': "Feuchtegrenze Max 08-B2",
        '\x3a': "Feuchtesensor 08-B2",
        '\x3b': "Wassermangel Feuchte 07-B80",
        '\x3c': "TK Ventilator Verfl. 03-F5.1",
        '\x3d': "Siededrucksensor 03-B60",
        '\x3f': "Pt100 Abluft 08-B1.1",
        '\x40': "Pt100 Zuluft 08-B1.2",
        '\x41': "Pt100 Wasserbad 07-B4",
        '\x42': "Schwimmer Wasservorrat 07-B81",
        '\x43': "Pt100 Beweglich 08-B15",
        '\x47': "Pt100 Sauggas K 03-B13",
        '\x4b': "Sauggastemp. K 03-B13",
        '\x53': "Absaugung Kuehlung 03-B43",
        '\x5b': "Schwimmer Wasserbad 07-B80",
        '\x5c': "Pt100 Saugdampf K 03-B12",
        '\x5e': "Siededrucksensor K 03-B43",
        '\x62': "Leistungsschalter Einspeisung 00-Q1",
    }

    def write_bytes(self, message):
        if not isinstance(message, bytes):
            message = message.encode()
        return self.resource.write_raw(message)

    def read_bytes(self, count):
        return self.resource.read_bytes(count).decode()

    def query_bytes(self, message, count):
        self.write_bytes(message)
        return self.read_bytes(count)

    @Feat()
    def time(self):
        """Returns current date and time of device as datetime object.
        >>> device.time
        datetime.datetime(2019, 6, 12, 13, 01, 21)
        """
        result = self.query_bytes('T', 13)
        return datetime.datetime.strptime(result, 'T%d%m%y%H%M%S')

    @time.setter
    def time(self, dt):
        """Update device date and time, returns updated data and time as datetime object.
        >>> device.time = datetime.now()
        datetime.datetime(2019, 6, 12, 13, 12, 35)
        """
        result = self.query_bytes(dt.strftime('t%d%m%y%H%M%S'), 13)
        return datetime.datetime.strptime(result, 't%d%m%y%H%M%S')

    @DictFeat(keys=analog_channel_codes.keys())
    def analog_channel(self, key):
        """Read analog channel, returns tuple containing actual value and target value.
        >>> device.analog_channel[1]
        (42.1, 45.0)
        """
        result = self.query_bytes(key, 14)
        _, actual, target = result.split()
        return float(actual), float(target)

    @analog_channel.setter
    def analog_channel(self, key, value):
        """Set target value for analog channel.
        >>> device.analog_channel[1] = 42.0
        """
        result = self.query_bytes('a{}_{:05.1f}'.format(key, value), 1)
        if result != 'a':
            raise InstrumentError("Invalid channel: '{}'".format(key))

    @Feat()
    def status(self):
        """Returns device status as dictionary.
        >>> device.status
        {'running': False, 'warning': None, 'error': None, '', }
        """
        result = self.query_bytes('S', 10)
        running = bool(int(result[1]))
        is_error = bool(int(result[2]))
        channel_states = {channel: bool(int(state)) for channel, state in enumerate(result[3:9])}
        error_nr = result[9]
        warning = self.warning_messages[error_nr] if is_error and error_nr in self.warning_messages else None
        error = self.error_messages[error_nr] if is_error and error_nr in self.error_messages else None
        return {
            'running': running,
            'warning': warning,
            'error': error,
            'digital_channels': channel_states,
        }

    @DictFeat(values={False: 0, True: 1}, keys=list(range(1, 7)))
    def digital_channel(self, key):
        result = self.query_bytes('S', 10)
        channel_states = {channel + 1: int(state) for channel, state in enumerate(result[3:9])}
        return channel_states[key]

    @digital_channel.setter
    def digital_channel(self, key, value):
        result = self.query_bytes('s{}_{}'.format(key, value), 4)
        return result

    @Feat()
    def program(self):
        """Returns number of running program or None if no program is running.
        >>> device.program
        3
        """
        result = self.query_bytes('P', 4)
        value = int(result[1:])
        return value if value else None

    @Action()
    def start_program(self, key):
        """Starts a program. Returns program number or None for no program.
        >>> device.start_program(42)
        42
        """
        self.write_bytes('P{:03d}'.format(key))

    @Action()
    def stop_program(self):
        """Stops a running program. Returns program number or None for no program.
        >>> device.stop_program()
        """
        self.write_bytes('P{:03d}'.format(key))

    # TODO

    @Feat()
    def error_message(self):
        """Returns current error message."""
        result = self.query_bytes('F', 33)
        return result[1:].strip()

    # TODO

    @Feat(limits=(0, 2))
    def keyboard_lock(self):
        result = self.query_bytes('L', 2)
        return int(result[1:])

    @keyboard_lock.setter
    def keyboard_lock(self, value):
        self.query_bytes('l{}'.format(value), 2)
