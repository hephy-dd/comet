""" Driver for ECR AC3 thermal chuck"""

from typing import Tuple


class AC3:
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

    def get_error_status(self) -> int:
        """Get error status code."""
        response = self._query("RE")
        # Format: Eyyy where yyy is error code
        return int(response[1:])
