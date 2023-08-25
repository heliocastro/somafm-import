# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import click
from dotenv import load_dotenv

from somafm.somaplugins import SomaPlugins


def main() -> None:
    # Read env file
    load_dotenv()

    # Start application
    app = SomaPlugins()
    app.run()

    cli = click.CommandCollection(sources=app.commands)

    # Call click
    cli()


if __name__ == "__main__":
    main()
