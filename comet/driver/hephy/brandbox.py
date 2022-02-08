import re
from typing import List, Optional, Tuple

from comet.driver.generic import SwitchingMatrix
from comet.driver.generic import InstrumentError
from comet.utils import combine_matrix

__all__ = ['BrandBox']

ERROR_MESSAGES = {
    99: "Invalid command"
}


def split_channels(channels: str) -> List[str]:
    return [channel.strip() for channel in channels.split(',') if channel.strip()]


def join_channels(channels: List[str]) -> str:
    return ','.join([format(channel).strip() for channel in channels])


def parse_error(response: str) -> Optional[InstrumentError]:
    m = re.match(r'^err(\d+)', response.lower())
    if m:
        code = int(m.group(1))
        message = ERROR_MESSAGES.get(code, "")
        return InstrumentError(code, message)
    return None


class BrandBox(SwitchingMatrix):

    CHANNELS = combine_matrix('ABC', '12')

    _error_queue: List[InstrumentError] = []

    def identify(self) -> str:
        return self.query('*IDN?')

    def reset(self) -> None:
        self._error_queue.clear()
        self.write('*RST')

    def clear(self) -> None:
        self._error_queue.clear()
        self.write('*CLS')

    def next_error(self) -> Optional[InstrumentError]:
        if self._error_queue:
            return self._error_queue.pop(0)
        return None

    def closed_channels(self) -> List[str]:
        channels = self.query(':CLOS:STAT?')
        return split_channels(channels)

    def close_channels(self, channels: List[str]) -> None:
        channel_list = join_channels(sorted(channels))
        self.write(f':CLOS {channel_list}')

    def open_channels(self, channels: List[str]) -> None:
        channel_list = join_channels(sorted(channels))
        self.write(f':OPEN {channel_list}')

    def open_all_channels(self) -> None:
        channel_list = join_channels(self.CHANNELS)
        self.write(f':OPEN {channel_list}')

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
