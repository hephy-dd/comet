# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] - 2025-11-18

### Added

- Support for Python 3.14 (#99).
- Generic oscilloscope driver (#97).
- Rohde&Schwarz RTO6/RTP164 drivers and emulators (#97).
- Type annotations in emulator code.
- Emulator module tests.
- Display measure function to Keithley 2657A emulator.

### Changed

- Emulator yields `TextResponse`, `RawResponse` or `RawResponse`.
- Renamed `--hostname` to `--host` for emulator parameters.
- Set default emulator host to `localhost`.
- Renamed this changelog to `CHANGELOG.md`.

### Removed

- Obsolete `mypy.ini` (not required with recent mypy versions).

### Fixed

- Emulator routes are now properly overriden from derived classes in function `get_routes`.

## [1.3.1] - 2025-10-23

### Fixed

- PILAS emulator missing response from tune command (#100).

## [1.3.0] - 2025-08-11

### Added

- Station context manager for handling collections of instruments.

### Changed

- Replaced methods by properties in PILAS driver.

### Fixed

- Unpacking emulator TCPIP server address (IPv4/IPv6).

## [1.2.2] - 2025-03-27

### Added

- Tests for Keithley K2700 emulator.

### Fixed

- Keithley K2700 reading format

## [1.2.1] - 2025-03-26

### Changed

- Deprecated version key in emulator files (#92).

### Fixed

- Install instructions and links.

## [1.2.0] - 2025-03-25

### Added

- Generic base class `DigitalMultiMeter`.
- Keithley DAQ6510 DMM (#88).
- Keithley K2700 DMM (#89).
- Driver factory (#90).

## [1.1.1] - 2025-03-17

### Added

- Executable script `comet-emulator` (#87).
- Deploying docs using gh-pages (#86).

## [1.1.0] - 2025-03-14

### Added

- Support for Python 3.13
- Emulator mock resources (#84).
- Missing type hints for static type checking (#82).
- Generic base classes `PowerSupply` and `PowerSupplyChannel` and `LightSource`.
- Additional HEPHY EnvironBox commands for driver and emulator (#74).
- Rhode&Schwarz NGE100 power supply (#77).
- Photonic F3000 LED light source (#75).
- Thorlabs PM100 USB optical power meter (#78).
- Rohde&Schwarz SMA100B (#79).
- NKT Photonics PILAS laser (#80).
- ERS AC3 Thermal Chuck (#83).

### Changed

- Restructured driver mixins (#81).

### Removed

- Dropped support for Python 3.8

## [1.0.0] - 2024-03-26

### Added

- ITK Hydra emulator.

### Changed

- ITK CorvusTT emulator.

[unreleased]: https://github.com/hephy-dd/comet/releases/tag/v1.4.0...HEAD
[1.4.0]: https://github.com/hephy-dd/comet/compare/v1.3.1...v1.4.0
[1.3.1]: https://github.com/hephy-dd/comet/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/hephy-dd/comet/compare/v1.2.2...v1.3.0
[1.2.2]: https://github.com/hephy-dd/comet/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/hephy-dd/comet/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/hephy-dd/comet/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/hephy-dd/comet/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/hephy-dd/comet/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/hephy-dd/comet/releases/tag/v1.0.0
