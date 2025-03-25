# Drivers

Generic instrument drivers use a PyVISA compatible resource to communicate with.

See package [comet.driver](https://github.com/hephy-dd/comet/tree/main/src/comet/driver) for available instrument drivers.

## Examples

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

Loading driver by module name using driver factory.

```python
from comet.driver import driver_factory

rm = pyvisa.ResourceManager("@py")

with rm.open_resource("TCPIP::0.0.0.0::11001::SOCKET") as res:
    smu = driver_factory("keithley.k2410")(res)
```

Switching between generic drivers.

```python
from comet.driver import driver_factory

smu_drivers = {
    "Keithely2410": "keihtley.k2410",
    "Keithely2470": "keihtley.k2470",
    "Keitley2657A": "keihtley.k2657a",
}

driver_name = "Keithely2470"

rm = pyvisa.ResourceManager("@py")

with rm.open_resource("TCPIP::0.0.0.0::11001::SOCKET") as res:
    smu = smu_drivers.get(driver_name)(res)
```

Open multiple resources using `contextlib.ExitStack` to guarantee all
resources are automatically closed properly.

```python
from contextlib import ExitStack

import pyvisa

resource_name_1 = "TCPIP::0.0.0.0::11001::SOCKET"
resource_name_2 = "TCPIP::0.0.0.0::11002::SOCKET"

rm = pyvisa.ResourceManager("@py")

with ExitStack() as stack:
    res_1 = stack.enter_context(rm.open_resource(resource_name_1))
    res_2 = stack.enter_context(rm.open_resource(resource_name_2))
    ...
```
