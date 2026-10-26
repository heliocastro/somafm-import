# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import importlib
from typing import Any, ClassVar


class SomaPlugins:
    """SomaPlugins main class
    Init accept to entries, a plugin name ( required ) and a set of parameters
    """

    _plugins: ClassVar[list[str]] = ["radiola"]
    _commands: ClassVar[list[Any] | None] = None

    def __init__(self) -> None:
        # Load plugins is specified
        for plugin in self._plugins:
            command = importlib.import_module(f".{plugin}", "somafm.plugins")
            if SomaPlugins._commands is None:
                SomaPlugins._commands = [command.plugin_group]
            else:
                SomaPlugins._commands.append(command.plugin_group)

    def run(self) -> None:
        """Import main function call"""

    @property
    def commands(self) -> list[Any] | None:
        """Return the dynamic commands from plugins"""
        return self._commands
