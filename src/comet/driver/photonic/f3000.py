from comet.driver import Driver

__all__ = ["F3000"]


class F3000Driver(Driver):
    """Photonic LED light source base class"""

    def __init__(self, resource):
        self.resource = resource
        self.resource.write_termination = "\r"
        self.resource.read_termination = "\r"


class F3000(F3000Driver):
    """Class for controlling Photonics F3000 LED light sources"""

    @property
    def brightness(self) -> int:
        """Returns current brightness of light source
            (0-100 percent)

        Returns:
            int . Brightness of light source in percent
        """

        self.resource.write("B?")
        response = self.resource.read()

        return int(response.replace("B", ""))

    @brightness.setter
    def brightness(self, brightness: int):
        """Set brightness of light source in percent

        Args:
            brightness (int): Brightness to set in percent
        """
        brightness = max(0, min(100, brightness))

        self.resource.write(f"B{brightness}")
        self.resource.read()

    @property
    def light_enabled(self) -> bool:
        """Get current state of shutter (light source)

        Returns:
            str: State of light source (1 on, 0 off)
        """

        self.resource.write("S?")
        response = self.resource.read().replace("S", "")

        if int(response) == 1:
            return 0
        elif int(response) == 0:
            return 1

    @light_enabled.setter
    def light_enabled(self, light_enabled: bool):
        """Turn on / off shutter (light source)

        Args:
            light_enabled (bool): Enable / Disable light source
        """
        if light_enabled:
            self.resource.write("S0")
        else:
            self.resource.write("S1")

        self.resource.read()