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

from .stack import AsyncEmulatorStack

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        dest="filename",
        metavar="filename",
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
        await stack.serve_forever()


def main() -> None:
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        # Fallback for platforms where asyncio signal handlers are unavailable.
        ...


if __name__ == "__main__":
    main()
