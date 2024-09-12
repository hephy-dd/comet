import re
from typing import Any, Optional

from comet.driver.generic import Instrument
from comet.driver.generic import InstrumentError

__all__ = ["EnvironBox"]

ERROR_MESSAGES: dict[int, str] = {
    1: "RTC not running",
    2: "RTC read error",
    80: "DAC not found",
    90: "I/O Port Expander parameter error",
    99: "Invalid command",
    100: "General SET command error",
    199: "GET command parameter not found",
    200: "General GET command error",
    999: "Unknown command",
}


def test_bit(value: int, index: int) -> bool:
    return bool((value >> index) & 1)


def parse_error(response: str) -> Optional[InstrumentError]:
    m = re.match(r"^err(\d+)", response.lower())
    if m:
        code = int(m.group(1))
        message = ERROR_MESSAGES.get(code, "")
        return InstrumentError(code, message)
    return None


def parse_pc_data(response: str) -> dict[str, Any]:
    values = response.split(",")
    relay_status = int(values[23])
    return {
        "sensor_count": int(values[0]),
        "box_humidity": float(values[1]),
        "box_temperature": float(values[2]),
        "box_dewpoint": float(values[3]),
        "pid_status": bool(int(values[4])),
        "pid_setpoint": float(values[5]),
        "pid_input": float(values[6]),
        "pid_output": float(values[7]),
        "pid_kp_1": float(values[8]),
        "pid_ki_1": float(values[9]),
        "pid_kd_1": float(values[10]),
        "pid_min": float(values[11]),
        "pid_max": float(values[12]),
        "pid_control_mode": int(values[13]),
        "pid_kp_2": float(values[14]),
        "pid_ki_2": float(values[15]),
        "pid_kd_2": float(values[16]),
        "parameter_set": int(values[17]),
        "parameter_threshold": float(values[18]),
        "hum_flow_dir": int(values[19]),
        "pid_threshold": float(values[20]),
        "vac_valve_current": float(values[21]),
        "vac_valve_count": int(values[22]),
        "power_microscope_ctrl": test_bit(relay_status, 0),
        "power_box_light": test_bit(relay_status, 1),
        "power_probecard_light": test_bit(relay_status, 2),
        "power_laser_sensor": test_bit(relay_status, 3),
        "power_probecard_camera": test_bit(relay_status, 4),
        "power_microscope_camera": test_bit(relay_status, 5),
        "power_microscope_light": test_bit(relay_status, 6),
        "box_light": bool(int(values[24])),
        "box_door": bool(int(values[25])),
        "safety_alert": bool(int(values[26])),
        "stepper_motor_control": bool(int(values[27])),
        "air_flow_sensor": bool(int(values[28])),
        "vac_flow_sensor": bool(int(values[29])),
        "test_led": bool(int(values[30])),
        "discharge_time": float(values[31]),
        "box_lux": float(values[32]),
        "pt100_1": float(values[33]),
        "pt100_2": float(values[34]),
        "pid_sample_time": float(values[35]),
        "pid_prop_mode": int(values[36]),
        "pt100_1_enabled": bool(int(values[37])),
        "pt100_2_enabled": bool(int(values[38])),
    }


class EnvironBox(Instrument):
    _error_queue: list[InstrumentError] = []

    def identify(self) -> str:
        return self.query("*IDN?")

    def reset(self) -> None:
        self._error_queue.clear()
        # self.write("*RST")

    def clear(self) -> None:
        self._error_queue.clear()
        # self.write("*CLS")

    # Error queue

    def next_error(self) -> Optional[InstrumentError]:
        if self._error_queue:
            return self._error_queue.pop(0)
        return None

    DISCARGE_OFF: bool = False
    DISCARGE_ON: bool = True

    def set_discharge(self, state: bool) -> None:
        value = {self.DISCARGE_OFF: "OFF", self.DISCARGE_ON: "ON"}[state]
        self.write(f"SET:DISCHARGE {value}")

    PID_CONTROL_OFF: bool = False
    PID_CONTROL_ON: bool = True

    def get_pid_control(self) -> bool:
        return bool(int(self.query("GET:CTRL ?")))

    def set_pid_control(self, state: bool) -> None:
        value = {self.PID_CONTROL_OFF: "OFF", self.PID_CONTROL_ON: "ON"}[state]
        self.write(f"SET:CTRL {value}")

    PID_CONTROL_MODE_HUM: str = "HUM"
    PID_CONTROL_MODE_DEW: str = "DEW"

    def get_pid_control_mode(self) -> str:
        value = self.get_data()["pid_control_mode"]
        return {1: self.PID_CONTROL_MODE_HUM, 2: self.PID_CONTROL_MODE_DEW}[value]

    def set_pid_control_mode(self, mode: str) -> None:
        value = {self.PID_CONTROL_MODE_HUM: "HUM", self.PID_CONTROL_MODE_DEW: "DEW"}[mode]
        self.write(f"SET:CTRL_MODE {value}")

    PID_DOOR_STOP_OFF: bool = False
    PID_DOOR_STOP_ON: bool = True

    def get_pid_door_stop(self) -> bool:
        value = self.query("GET:PID_DOOR_STOP ?")
        return {"1": self.PID_DOOR_STOP_OFF, "2": self.PID_DOOR_STOP_ON}[value]  # [1=OFF,2=ON]

    def set_pid_door_stop(self, state: bool) -> None:
        value = {self.PID_DOOR_STOP_OFF: "OFF", self.PID_DOOR_STOP_ON: "ON"}[state]
        self.write(f"SET:PID_DOOR_STOP {value}")

    def get_box_humidity(self) -> float:
        return float(self.query("GET:HUM ?"))

    def get_box_temperature(self) -> float:
        return float(self.query("GET:TEMP ?"))

    def get_box_lux(self) -> float:
        return float(self.query("GET:LUX ?"))

    BOX_DOOR_CLOSED: bool = False
    BOX_DOOR_OPEN: bool = True

    def get_box_door_state(self) -> bool:
        return bool(float(self.query("GET:DOOR ?")))

    def get_chuck_temperature(self) -> float:
        return float(self.query("GET:PT100_1 ?"))

    def get_chuck_block_temperature(self) -> float:
        return float(self.query("GET:PT100_2 ?"))

    BOX_LIGHT_OFF: bool = False
    BOX_LIGHT_ON: bool = True

    def get_box_light(self) -> bool:
        value = self.query("GET:LIGHT ?")
        return {"0": self.BOX_LIGHT_OFF, "1": self.BOX_LIGHT_ON}[value]

    def set_box_light(self, state: bool) -> None:
        value = {self.BOX_LIGHT_OFF: "OFF", self.BOX_LIGHT_ON: "ON"}[state]
        self.write(f"SET:BOX_LIGHT {value}")

    MICROSCOPE_LIGHT_OFF: bool = False
    MICROSCOPE_LIGHT_ON: bool = True

    def get_microscope_light(self) -> bool:
        value = self.get_data()["power_microscope_light"]
        return {False: self.BOX_LIGHT_OFF, True: self.BOX_LIGHT_ON}[value]

    def set_microscope_light(self, state: bool) -> None:
        value = {self.BOX_LIGHT_OFF: "OFF", self.BOX_LIGHT_ON: "ON"}[state]
        self.write(f"SET:MICROSCOPE_LIGHT {value}")

    PROBECARD_LIGHT_OFF: bool = False
    PROBECARD_LIGHT_ON: bool = True

    def get_probecard_light(self) -> bool:
        value = self.get_data()["power_probecard_light"]
        return {False: self.BOX_LIGHT_OFF, True: self.BOX_LIGHT_ON}[value]

    def set_probecard_light(self, state: bool) -> None:
        value = {self.BOX_LIGHT_OFF: "OFF", self.BOX_LIGHT_ON: "ON"}[state]
        self.write(f"SET:PROBCARD_LIGHT {value}")

    TEST_LED_OFF: bool = False
    TEST_LED_ON: bool = True

    def get_test_led(self) -> bool:
        """Get state of test LED."""
        value = self.query("GET:TEST_LED ?")
        return {"0": self.TEST_LED_OFF, "1": self.TEST_LED_ON}[value]

    def set_test_led(self, state: bool) -> None:
        """Set test LED state."""
        value = {self.TEST_LED_OFF: "OFF", self.TEST_LED_ON: "ON"}[state]
        self.write(f"SET:TEST_LED {value}")

    DOOR_AUTO_LIGHT_OFF: bool = False
    DOOR_AUTO_LIGHT_ON: bool = True

    def get_door_auto_light(self) -> bool:
        """Get state of door automatic light switch."""
        value = self.query("GET:DOOR_AUTO_LIGHT ?")
        return {"1": self.DOOR_AUTO_LIGHT_OFF, "2": self.DOOR_AUTO_LIGHT_ON}[value]  # [1=OFF,2=ON]

    def set_door_auto_light(self, state: bool) -> None:
        """Set door automatic light switch state."""
        value = {self.DOOR_AUTO_LIGHT_OFF: "OFF", self.DOOR_AUTO_LIGHT_ON: "ON"}[state]
        self.write(f"SET:DOOR_AUTO_LIGHT {value}")

    def get_data(self) -> dict[str, Any]:
        """Return dictionary of PC_DATA."""
        return parse_pc_data(self.query("GET:PC_DATA ?"))

    def get_uptime(self) -> float:
        """Return Arduino uptime in seconds."""
        value = self.query("GET:UPTIME ?")
        days, hours, minutes, seconds = map(int, value.split(","))
        total_seconds = (days * 24 * 60 * 60) + (hours * 60 * 60) + (minutes * 60) + seconds
        return float(total_seconds)

    # Helper

    def query(self, message: str) -> str:
        response = self.resource.query(message).strip()
        error = parse_error(response)
        if error:
            self._error_queue.append(error)
            return ""
        return response

    def write(self, message: str) -> None:
        response = self.query(message)
        error = parse_error(response)
        if error:
            self._error_queue.append(error)
