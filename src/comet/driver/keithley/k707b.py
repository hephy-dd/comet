from typing import List, Optional

from comet.driver.generic import InstrumentError
from comet.driver.generic.switching_matrix import SwitchingMatrix
from comet.utils import combine_matrix

__all__ = ['K707B']


def split_channels(channels: str) -> List[str]:
    return [channel.strip() for channel in channels.split(';') if channel.strip()]


def join_channels(channels: List[str]) -> str:
    return ','.join([format(channel).strip() for channel in channels])


class K707B(SwitchingMatrix):

    CHANNELS = combine_matrix('1234', 'ABCDEFG', combine_matrix('0', '123456789') + combine_matrix('1', '12'))

    def identify(self) -> str:
        return self.query('*IDN?')

    def reset(self) -> None:
        self.write('*RST')

    def clear(self) -> None:
        self.write('*CLS')

    # Beeper

    @property
    def beeper(self) -> bool:
        return bool(float(self.tsp_print('beeper.enable')))

    @beeper.setter
    def beeper(self, value: bool) -> None:
        self.tsp_assign('beeper.enable', format(value, 'd'))

    # Error queue

    def next_error(self) -> Optional[InstrumentError]:
        code, message = self.tsp_print('errorqueue.next()').split('\t')[:2]
        if int(code):
            return InstrumentError(int(code), message.strip('\"\' '))
        return None

    # Switching matrix

    @property
    def closed_channels(self) -> List[str]:
        channels = self.tsp_print('channel.getclose("allslots")')
        if channels == 'nil':
            return []
        return sorted(split_channels(channels))

    def close_channels(self, channels: List[str]) -> None:
        channel_list = join_channels(channels)
        self.write(f'channel.close("{channel_list}")')

    def open_channels(self, channels: List[str]) -> None:
        channel_list = join_channels(channels)
        self.write(f'channel.open("{channel_list}")')

    def open_all_channels(self) -> None:
        self.write('channel.open("allslots")')

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)
        self.query('*OPC?')

    def tsp_print(self, expression: str) -> str:
        return self.query(f'print({expression})')

    def tsp_assign(self, expression: str, value: str) -> None:
        self.write(f'{expression} = {value}')
