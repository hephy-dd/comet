import re
from typing import List, Optional, Tuple

from comet.driver.generic import Instrument
from comet.driver.generic import InstrumentError

__all__ = ['ShuntBox']

ERROR_MESSAGES = {
    99: "Unknown command"
}


def parse_error(response: str) -> Optional[InstrumentError]:
    m = re.match(r'^err(\d+)', response.lower())
    if m:
        code = int(m.group(1))
        message = ERROR_MESSAGES.get(code, "")
        return InstrumentError(code, message)
    return None


class ShuntBox(Instrument):

    _error_queue: List[InstrumentError] = []

    def identify(self) -> str:
        return self.query('*IDN?')

    def reset(self) -> None:
        self._error_queue.clear()
        self.write('*RST')

    def clear(self) -> None:
        self._error_queue.clear()
        self.write("*CLS")

    def next_error(self) -> Optional[InstrumentError]:
        if self._error_queue:
            return self._error_queue.pop(0)
        return None

    # Helper

    def query(self, message: str) -> str:
        response = self.resource.query(message).strip()
        error = parse_error(response)
        if error:
            self._error_queue.append(error)
            return ''
        return response

    def write(self, message: str) -> None:
        response = self.query(message)
        error = parse_error(response)
        if error:
            self._error_queue.append(error)

