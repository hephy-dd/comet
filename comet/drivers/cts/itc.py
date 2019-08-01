import datetime

from slave.driver import Command, Driver
from slave.types import Boolean, Float, Integer, Mapping, Set

__all__ = ['ITC']

class ITC(Driver):

    ANALOG_CHANNELS = {
        1: '0',
        2: '1',
        3: '2',
        4: '3',
        5: '4',
        6: '5',
        7: '6',
        8: '7',
        9: '8',
        10: '9',
        11: ':',
        12: ';',
        13: '<',
        14: '=',
        15: '>',
        16: '?',
    }
    """Mapping analog channel index to channel code."""

    WARNING_MESSAGES = {
        '\x01': "Wassernachfüllen",
        '\x02': "Temp. Toleranzband Oben",
        '\x03': "Temp. Toleranzband Unten",
        '\x04': "Feuchte Toleranzband Oben",
        '\x05': "Feuchte Toleranzband Unten",
        '\x06': "Wasserbad Abschlaemmen",
    }
    """Warning messages."""

    ERROR_MESSAGES = {
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
    """Error messages."""

    def __init__(self, transport, protocol=None):
        super().__init__(transport, protocol)

    @property
    def time(self):
        """Returns current date and time of device as datetime object.
        >>> device.time
        datetime.datetime(2019, 6, 12, 13, 01, 21)
        """
        self._transport.write_raw(b'T')
        result = self._transport.read_bytes(13).decode()
        return datetime.datetime.strptime(result, 'T%d%m%y%H%M%S')

    @time.setter
    def time(self, dt):
        """Update device date and time, returns updated data and time as datetime object.
        >>> device.time = datetime.now()
        datetime.datetime(2019, 6, 12, 13, 12, 35)
        """
        self._transport.write_raw(dt.strftime('t%d%m%y%H%M%S').encode())
        result = self._transport.read_bytes(13)
        return datetime.datetime.strptime(result, 't%d%m%y%H%M%S')

    @property
    def error_message(self):
        """Returns current error message."""
        self._transport.write_raw(b'F')
        result = self.read_bytes(33).decode()
        return result[1:].strip()
