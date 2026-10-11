"""Run instrument emulators as TCP sockets based on a simple `emulators.yaml`
configuration file.

Example configuration:

```
emulators:
  smu:
    model: urn:comet:model:keithley:2410
    port: 10001
  lcr:
    model: urn:comet:model:keysight:e4980a
    port: 11002
```

Loading a configuration filename (default filenames are `emulators.yaml` and `emulators.yml`).

```
python -m comet.emulator [-f emulators.yaml]
```

Hit Ctrl+C to stop all emulator sockets.

"""

import argparse
import asyncio
import logging
from importlib.metadata import version

from .service import AsyncEmulatorStackService
from .stack import AsyncEmulatorStack

logger = logging.getLogger(__name__)


def port_number(value: str) -> int:
    port = int(value)
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
    return port


def positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return number


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        dest="filename",
        metavar="filename",
    )
    parser.add_argument(
        "--service-port",
        type=port_number,
        metavar="port",
        help="Enable the emulator hook JSON-RPC service on localhost",
    )
    parser.add_argument(
        "--service-session-timeout",
        type=positive_float,
        default=30.0,
        metavar="seconds",
        help="Close inactive service sessions after this many seconds (default: 30)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {version('comet')}",
        help="Print version information and quit",
    )
    return parser.parse_args()


async def async_main() -> None:
    args = parse_args()

    logging.basicConfig(level=logging.INFO)

    async with AsyncEmulatorStack.from_file(args.filename or None) as stack:
        if args.service_port is None:
            await stack.serve_forever()
        else:
            async with AsyncEmulatorStackService(
                stack,
                args.service_port,
                args.service_session_timeout,
            ):
                await stack.serve_forever()


def main() -> None:
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        # Fallback for platforms where asyncio signal handlers are unavailable.
        ...


if __name__ == "__main__":
    main()
