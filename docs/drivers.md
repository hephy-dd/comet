# Drivers

Generic instrument drivers use a PyVISA compatible resource to communicate with.

```python
import pyvisa

from comet.driver.keithley import K2470

rm = pyvisa.ResourceManager("@py")

with rm.open_resource("TCPIP::0.0.0.0::11001::SOCKET") as res:
    smu = K2470(res)
    print(smu.identify())

    smu.reset()
    smu.function = smu.FUNCTION_VOLTAGE
    smu.current_compliance = 1e-6
    smu.output = smu.OUTPUT_ON
    smu.voltage_level = 5.0

    reading = smu.measure_current()
    print(reading)

    smu.voltage_level = 0.0
    smu.output = smu.OUTPUT_OFF
```

Switching between generic drivers.

```python
from comet.driver.keithley import K2410
from comet.driver.keithley import K2470
from comet.driver.keithley import K2657A

smu_drivers = {
    "Keithely2410": K2410,
    "Keithely2470": K2470,
    "Keitley2657A": K2657A,
}

driver_name = "Keithely2470"

rm = pyvisa.ResourceManager("@py")

with rm.open_resource("TCPIP::0.0.0.0::11001::SOCKET") as res:
    smu = smu_drivers.get(driver_name)(res)
```

See package [comet.driver](https://github.com/hephy-dd/comet/tree/main/comet/driver) for available instrument drivers.
