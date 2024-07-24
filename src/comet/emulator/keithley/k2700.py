import random
import time
from typing import List

from comet.emulator import IEC60488Emulator, message, run
from comet.emulator.utils import Error


class K2700Emulator(IEC60488Emulator):

    IDENTITY: str = "Keithley Inc., Model 2700, 43768438, v1.0 (Emulator)"

    def __init__(self) -> None:
        super().__init__()
        self.sense_voltage_average_tcontrol: str = "MOV"
        self.sense_voltage_average_count: int = 10
        self.sense_voltage_average_state: bool = False
        self.error_queue: List[Error] = []
        self.system_beeper_state: bool = True
        self.trigger_delay_auto: bool = True
        self.trigger_delay: float = 0.001

    @message(r'^\*RST$')
    def set_rst(self):
        self.sense_voltage_average_tcontrol = "MOV"
        self.sense_voltage_average_count = 10
        self.sense_voltage_average_state = False
        self.error_queue.clear()
        self.system_beeper_state = True
        self.trigger_delay_auto = True
        self.trigger_delay = 0.001

    @message(r'^\*CLS$')
    def set_cls(self):
        self.error_queue.clear()

    @message(r'^:?SENS:VOLT:AVER:TCON\?$')
    def get_sense_average_tcontrol(self):
        return self.sense_voltage_average_tcontrol

    @message(r'^:?SENS:VOLT:AVER:TCON\s+(REP|MOV)$')
    def set_sense_average_tcontrol(self, name: str):
        self.sense_voltage_average_tcontrol = name

    @message(r'^:?SENS:VOLT:AVER:COUN[T]?\?$')
    def get_sense_average_count(self):
        return format(self.sense_voltage_average_count, "d")

    @message(r'^:?SENS:VOLT:AVER:COUN[T]?\s+(\d+)$')
    def set_sense_average_count(self, count: str):
        self.sense_voltage_average_count = int(count)

    @message(r'^:?SENS:VOLT:AVER(?::STAT[E]?)?\?$')
    def get_sense_voltage_average_state(self):
        return format(self.sense_voltage_average_state, "d")

    @message(r'^:?SENS:VOLT:AVER(?::STAT[E]?)?\s+(OFF|ON|0|1)$')
    def set_sense_voltage_average_state(self, value):
        self.sense_voltage_average_state = {"0": False, "1": True, "OFF": False, "ON": True}[value]

    @message(r'^:?SYST:ERR\?$')
    def get_system_error(self):
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "no error")
        return f'{error.code}, "{error.message}"'

    @message(r'^:?SYST:BEEP(?::STAT)?\?$')
    def get_beeper_state(self):
        return format(self.system_beeper_state, "d")

    @message(r'^:?SYST:BEEP(?::STAT)? (OFF|ON|0|1)$')
    def set_beeper_state(self, value):
        self.system_beeper_state = {'0': False, '1': True, 'OFF': False, 'ON': True}[value]

    @message(r'^:?INIT(?::IMM)$')
    def set_init(self):
        ...

    @message(r'^:?READ\?$')
    def get_read(self):
        self.get_fetch()

    @message(r'^:?FETC[H]?\?$')
    def get_fetch(self):
        vdc = random.uniform(.00025, .001)
        time.sleep(random.uniform(.5, 1.0))  # rev B10 ;)
        return "{:E},+0.000,+0.000,+0.000,+0.000".format(vdc)

    # Trigger

    @message(r':?TRIG:DEL:AUTO\?')
    def get_trigger_delay_auto(self):
        return format(self.trigger_delay_auto, "d")

    @message(r':?TRIG:DEL:AUTO\s+(OFF|ON|0|1)')
    def set_trigger_delay_auto(self, value):
        self.trigger_delay_auto = {'0': False, '1': True, 'OFF': False, 'ON': True}[value]

    @message(r':?TRIG:DEL\?')
    def get_trigger_delay(self):
        return format(self.trigger_delay, "E")

    @message(r':?TRIG:DEL\s+(.+)')
    def set_trigger_delay(self, value):
        try:
            self.trigger_delay = min(999999.999, max(0.001, float(value)))
        except ValueError:
            self.error_queue.append(Error(-113, "undefined header"))

    @message(r'^(.*)$')
    def unknown_message(self, request):
        self.error_queue.append(Error(101, "malformed command"))


if __name__ == '__main__':
    run(K2700Emulator())
