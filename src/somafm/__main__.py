# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro

import click

from somafm.somaplugins import SomaPlugins


def main() -> None:

    # Start application
    app = SomaPlugins()
    app.run()

    cli = click.CommandCollection(sources=app.commands)

    # Call click
    cli()


if __name__ == "__main__":
    main()
