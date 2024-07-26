from comet.driver import Driver

__all__ = ["Photonic"]


class PhotonicDriver(Driver):
    """Photonic LED light source base class"""

    def __init__(self, resource):
        self.resource = resource
        self.resource.write_termination = "\r"
        self.resource.read_termination = "\r"


class Photonic(PhotonicDriver):
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

        Raises:
            ValueError: Brightness outside of range [0,100]
        """
        brightness = int(brightness)
        if brightness < 0 or brightness > 100:
            raise ValueError("Brightness must be between 0 and 100")

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
