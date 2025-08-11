# Station

A Station represents a physical arrangement of instruments that you can control and interact with programmatically.
It serves as a centralized interface for managing multiple instruments in a safe way.

## Creation

### From API

Add instruments programmatically using API methods.
This is useful when you want full control in code without relying on external config files.

```python
from comet.station import Station

station = Station()
station.add_instrument("smu", resource_name="GPIB::16", model="keithley.k2410")
station.add_instrument("dmm", resource_name="GPIB::18", model="keithley.k2700")
```

### From dict

Create a station from a config dict:

```python
from comet.station import Station

station = Station.from_config({"instruments": {
    "smu": {"resource_name": "GPIB::16", "model": "keithley.k2410"},
    "dmm": {"resource_name": "GPIB::18", "model": "keithley.k2700"},
}})
```

### From config file

Create a station from a config file (either YAML or JSON):

```yaml
# station.yml
instruments:
  smu:
    resource_name: GPIB::16
    model: keithley.k2410
  dmm:
    resource_name: GPIB::18
    model: keithley.k2700
```

```python
from comet.station import Station

station = Station.from_file("station.yml")
```

If filename is omitted a station tries to load `station.yaml`, `station.yml` or
`station.json` relative to current working directory (in given order).

```python
station = Station.from_file()  # loads station.y[a]ml|json
```

Or pass a file like object to read from:

```python
with open("station.yml") as fp:
    station = Station.from_file(fp)
```

## Usage

A Station is used as a context manager.

When entering the with block, it automatically opens connections to all configured instruments.
When the block ends—whether normally or due to an error—it safely closes all connections.

Within the block, instruments can be accessed as attributes or dictionary-style keys, and the station itself is iterable for convenient bulk operations.

```python
from comet.station import Station

# Load station configuration (YAML, JSON, or dict)
with Station.from_file() as station:
    # Access instruments by attribute
    print(station.smu.identify())
    print(station.dmm.identify())

    # Or by dictionary-style key access (Station implements Mapping)
    print(station["smu"].identify())
    print(station["dmm"].identify())

    # Iterate over all instruments
    for name, instrument in station.items():
        print(f"{name}: {instrument.identify()}")
```
