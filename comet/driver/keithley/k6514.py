from typing import Optional

from comet.driver.generic import Electrometer
from comet.driver.generic import InstrumentError

__all__ = ['K6514']


def parse_error(response: str):
    code, message = [token.strip() for token in response.split(',')][:2]
    return int(code), message.strip('\"')


class K6514(Electrometer):

    def identify(self) -> str:
        return self.query('*IDN?')

    def reset(self) -> None:
        self.write('*RST')
        self.waitcomplete()

    def clear(self) -> None:
        self.write('*CLS')
        self.waitcomplete()

    def next_error(self) -> Optional[InstrumentError]:
        code, message = parse_error(self.query(':SYST:ERR:NEXT?'))
        if code:
            return InstrumentError(code, message)
        return None

    # Zero check

    def get_zero_check(self):
        return bool(int(self.query(":SYST:ZCH?")))

    def set_zero_check(self, enabled: bool):
        value = {False: 'OFF', True: 'ON'}[enabled]
        self.write(f':SYST:ZCH {value}')
        self.waitcomplete()

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)

    def waitcomplete(self) -> None:
        self.query('*OPC?')
