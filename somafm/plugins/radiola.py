# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import Element, ElementTree, SubElement, indent, tostring

import click
from appdirs import AppDirs
from defusedxml.ElementTree import parse

from somafm.soma import Soma

RADIOLA_APP_IDENTIFIER = "com.github.SokoloffA.Radiola"


class RadiolaPlugin:
    """Radiola Plugin
    Mac systemtray application
    """

    def __init__(self, update: bool = False) -> None:
        self._soma = Soma()
        self._update: bool = update

        radiola_config: Path = Path(AppDirs(RADIOLA_APP_IDENTIFIER).user_data_dir) / "bookmarks.opml"

        root: Element | Any = Element("ompl")
        if radiola_config.exists():
            logging.info("Importing current config from Radiola.")
            tree = parse(radiola_config)
            root = tree.getroot()
            # Take only the fist element
            self._body = root.findall("body")[0]
        else:
            logging.info("Creating new config to Radiola.")
            root.set("version", "2.0")
            SubElement(root, "head")
            self._body = SubElement(root, "body")

        # Create the tree
        self.update_tree()

        tree = ElementTree(root)
        if self._update:
            indent(tree, "  ")
            tree.write(radiola_config, short_empty_elements=False, encoding="utf-8")
        else:
            indent(root)
            print(tostring(root, encoding="unicode"))

    def update_tree(self) -> None:
        """Create Radiola file config"""

        # group: Element | None = SubElement(self._body, "outline")
        group: Element | None = None
        for channel in self._body.findall("outline"):
            if channel.attrib["text"] == "SomaFM":
                # Clean all entries
                channel.clear()
                group = channel

        # We didn't found SomaFM channel group
        if not isinstance(group, Element):
            group = SubElement(self._body, "outline")

        group.set("text", "SomaFM")
        group.set("group", "true")
        for channel in self._soma.channels:
            sub = SubElement(group, "outline")
            sub.set("text", channel["title"])
            sub.set("fav", "true")
            for pls in channel["playlists"]:
                if pls["format"] == "aac" and pls["quality"] == "highest":
                    sub.set("url", pls["url"])
                    break


@click.group()
def plugin_group() -> None:
    pass


@plugin_group.command()
@click.option("--update", default=False, is_flag=True, help="Update the current file instead of print only")
def radiola(update: bool) -> None:
    RadiolaPlugin(update)
