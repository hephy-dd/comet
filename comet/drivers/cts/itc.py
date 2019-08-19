import datetime

from ...driver import Driver

__all__ = ['ITC']

class ITC(Driver):

    ANALOG_CHANNELS = {
        1: b'A0',
        2: b'A1',
        3: b'A2',
        4: b'A3',
        5: b'A4',
        6: b'A5',
        7: b'A6',
        8: b'A7',
        9: b'A8',
        10: b'A9',
        11: b'A:',
        12: b'A;',
        13: b'A<',
        14: b'A=',
        15: b'A>',
        16: b'A?',
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

    def time(self):
        """Returns current date and time of device as datetime object.
        >>> device.time()
        datetime.datetime(2019, 6, 12, 13, 01, 21)
        """
        self.transport().write_raw(b'T')
        result = self.transport().read_bytes(13).decode()
        return datetime.datetime.strptime(result, 'T%d%m%y%H%M%S')

    def setTime(self, dt):
        """Update device date and time, returns updated data and time as datetime object.
        >>> device.setTime(datetime.now())
        datetime.datetime(2019, 6, 12, 13, 12, 35)
        """
        self.transport.write_raw(dt.strftime('t%d%m%y%H%M%S').encode())
        result = self.transport().read_bytes(13).decode()
        return datetime.datetime.strptime(result, 't%d%m%y%H%M%S')

    def status(self):
        """Returns current status.
        >>> device.status()
        {}
        """
        self.transport().write_raw(b'S')
        result = self.transport().read_bytes(10).decode()
        return result

    def analogChannel(self, index):
        """Returns analog channel reading."""
        code = self.ANALOG_CHANNELS[index]
        self.transport().write_raw(code)
        result = self.transport().read_bytes(14).decode().split(' ')[-1]
        return float(result)

    def errorMessage(self):
        """Returns current error message."""
        self.transport().write_raw(b'F')
        result = self.transport().read_bytes(33).decode()
        return result[1:].strip()
