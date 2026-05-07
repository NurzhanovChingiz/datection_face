"""CLI entrypoint with subcommands."""

from __future__ import annotations

import sys

from detection_face.entrypoints.cli.analyze import main as analyze_main

_COMMANDS = {
    "analyze": analyze_main,
}


def _main() -> None:
    """Dispatch to the appropriate subcommand."""
    if len(sys.argv) > 1 and sys.argv[1] in _COMMANDS:
        command = sys.argv.pop(1)
    else:
        command = "analyze"

    _COMMANDS[command]()


_main()
