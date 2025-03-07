"""Driver for ECR AC3 thermal chuck"""

from comet.driver.generic import Instrument, InstrumentError
from typing import Tuple, Optional


__all__ = ["AC3"]


class AC3(Instrument):
    """AC3 Fusion TS010S temperature controller interface."""

    # Operating mode constants
    MODE_NORMAL: int = 1
    MODE_STANDBY: int = 2
    MODE_DEFROST: int = 3
    MODE_PURGE: int = 4

    STATUS_TEMPERATURE_REACHED: int = 0
    STATUS_HEATING: int = 1
    STATUS_COOLING: int = 2
    STATUS_ERROR: int = 8

    ERROR_MESSAGES = {
        1: "OVERTEMP: The Chuck temperature has passed the maximum temperature limit by more than 2°C.",
        3: "CHUCKCABLE: Analog-digital-converter error",
        4: "CHUCKCABLE: The Chuck's sensor cable or the Chuck sensor is defective.",
        5: "CHUCKVOLTx or CHUCKCURRx: Either one of the Chuck's voltage sensors or the Chuck's current sensors is defective.",
        7: "BASE SENSOR: The base sensor cable is broken or the base sensor is defective.",
        8: "EXTCHILL: External Chiller communication error.",
        16: "DEWPWARN: The dew point is too close to the Chuck temperature. Chuck temperature waits for better dewpoint.",
        17: "DEWPALARM: Severe dew point deterioration. Auto Chuck Defrost in progress.",
        18: "DEWPSENS: Dew point sensor not connected or defective.",
        40: "ADC FROZEN: Analog-digital-converter error. Power has been switched off.",
        61: "OVERCURR HC1: The protective circuit has detected too much current to the Chuck heater No. 1. The Controller SP115P will shut off the Chuck power supply. (Dead end error)",
        62: "PWR DEFECT HC1: Power Supply defect. The protective circuit measures no voltage and current.",
        63: "UNDERCURR HC1: The protective circuit has detected too low current in Channel 1. The Circuit can measure voltage, but no current.",
        70: "INTTEMP: The internal temperature is outside its limits!",
        72: "THERMO CUT: Thermal Cut-Out. Chuck temperature has passed the maximum temperature limit and the safeguard has switched off the chuck power. (Dead end error)",
        81: "OVERCURR CH2: The protective circuit has detected too much current to the Chuck heater No 2 (Only for 300mm Chuck). The Controller SP115P will shut off the Chuck power supply. (Dead end error)",
        82: "PWR DEFECT CH2: Power Supply defect. The protective circuit measures no voltage and current.",
        83: "UNDERCURR CH2: The protective circuit has detected too low current to the Chuck heater No 2 (Only for 300mm Chuck).",
        89: "NOCHILLER: The air temperature coming from the Chiller does not go cold",
        97: "AIRPRESS LOW: Air pressure at air input is too low.",
        200: "PROB LOCK: Prober lock switch signaled an error.",
        201: "CHUCKTEMP: Chuck temperature differs. Power has been switched off.",
        202: "PT1000J: The PT1000J cable is defective.",
        203: "PT100M: The PT1000 cable is defective.",
    }

    def identify(self) -> str:
        self._query("RI")  # verify connection
        return "ERS AC3 Thermal Chuck"

    def reset(self) -> None: ...  # not supported

    def clear(self) -> None: ...  # not supported

    def next_error(self) -> Optional[InstrumentError]:
        code = int(self._query("RE")[1:])

        if code:
            return InstrumentError(code, self.ERROR_MESSAGES.get(code, "unknown error"))
        return None

    def __init__(self, resource):
        self._resource = resource

    def _query(self, message: str) -> str:
        """Send query and validate response.

        Args:
            message: Command string to send

        Returns:
            Response string from device

        Raises:
            RuntimeError: If device returns error
        """
        response = self._resource.query(message)
        if response.strip() == "?":
            raise RuntimeError(f"Command failed: {message}")
        return response.strip()

    @property
    def temperature(self) -> float:
        """Get current chuck temperature in °C."""
        response = self._query("RC")
        # Format: Csxxxx where s is sign and xxxx is temperature in 1/10°C
        value = float(response[1:]) / 10
        return value

    @property
    def target_temperature(self) -> float:
        """Get temperature setpoint in °C."""
        response = self._query("RT")
        # Format: Tvxxxx where v is sign and xxxx is temperature in 1/10°C
        value = float(response[1:]) / 10
        return value

    @target_temperature.setter
    def target_temperature(self, value: float) -> None:
        """Set temperature setpoint in °C."""

        if value > 300 or value < -70:
            raise ValueError("Temperature {} is out of range -70 to 300C".format(value))

        # Convert to 1/10°C with sign
        temp = int(value * 10)
        # write sign explicitly
        sign = "+" if temp >= 0 else "-"
        temp_str = f"{sign}{abs(temp):04d}"

        self._query(f"ST{temp_str}")

    @property
    def operating_mode(self) -> int:
        """Get current operating mode."""
        response = self._query("RO")
        # Format: Oy where y is mode number
        return int(response[1])

    @operating_mode.setter
    def operating_mode(self, mode: int) -> None:
        if mode not in range(1, 5):
            raise ValueError("Invalid mode: {}".format(mode))
        """Set operating mode."""
        self._query(f"SO{mode}")

    @property
    def dewpoint(self) -> float:
        """Get measured dewpoint in °C."""
        response = self._query("RF")
        # Format: Fsxxxx where s is sign and xxxx is dewpoint in 1/10°C
        value = float(response[1:]) / 10
        return value

    @property
    def dewpoint_control(self) -> bool:
        """Get dewpoint control status."""
        response = self._query("RD")
        # Format: Dy where y is 0 (off) or 1 (on)
        return bool(int(response[1]))

    @dewpoint_control.setter
    def dewpoint_control(self, state: bool) -> None:
        """Set dewpoint control state."""
        self._query(f"SD{int(state)}")

    @property
    def hold_mode(self) -> bool:
        """Get hold mode status."""
        response = self._query("RH")

        # y = 00: «Hold Mode» not active
        # y = 10: «Hold Mode» set but not yet reached
        # yy = 11: : «Hold Mode» set and reached

        return bool(int(response[1]))

    @hold_mode.setter
    def hold_mode(self, state: bool) -> None:
        """Set hold mode state."""
        self._query(f"SH{int(state)}")

    def get_control_status(self) -> int:
        """Get control status."""
        response = self._query("RI")

        return int(response[1])
