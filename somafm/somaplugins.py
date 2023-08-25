# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import importlib

import click


class SomaPlugins:
    """SomaPlugins main class
    Init accept to entries, a plugin name ( required ) and a set of parameters
    """

    _plugins = ["radiola"]
    _commands: list[click.MultiCommand] | None = None

    def __init__(self) -> None:
        # Load plugins is specified
        for plugin in self._plugins:
            command = importlib.import_module(f".{plugin}", "somafm.plugins")
            if self._commands is None:
                self._commands = [command.plugin_group]
            else:
                self._commands.append(command.plugin_group)

    def run(self) -> None:
        """Import main function call"""
        pass

    @property
    def commands(self) -> list[click.MultiCommand] | None:
        """Return the dynamic commands from plugins"""
        return self._commands
