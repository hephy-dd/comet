# Emulators

To emulate one or more instruments using TCP sockets create a `emulators.yaml`
configuration file in your project directory specifying emulator module and
port.

```yaml
version: '1.0'
emulators:
  smu:
    module: keithley.k2470
    port: 11001
  lcr:
    module: keysight.e4980a
    port: 11002
```

To spin up the emulator sockets execute the `comet.emulator` package.

```bash
python -m comet.emulator
```

Use command line argument `-f` to use a custom configuration file.

```bash
python -m comet.emulator -f custom_emulators.yaml
```

See package [comet.emulator](https://github.com/hephy-dd/comet/tree/main/comet/emulator) for available instrument emulators.
