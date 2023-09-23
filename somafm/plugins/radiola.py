# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import logging
import xml.etree.ElementTree as ElementTree
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement

import click
from appdirs import AppDirs
from defusedxml import defuse_stdlib
from defusedxml.ElementTree import parse
from defusedxml.minidom import parseString

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

        # Override standard xml functions
        defuse_stdlib()

        if radiola_config.exists():
            logging.info("Importing current config from Radiola.")
            tree = parse(radiola_config)
            root = tree.getroot()
            self._body = root.findall("body")
        else:
            logging.info("Creating new config to Radiola.")
            root = Element("ompl")
            root.set("version", "2.0")
            SubElement(root, "head")
            self._body = SubElement(root, "body")

        # Create the tree
        self.update_tree()

        tree = ElementTree.ElementTree(root)
        if self._update:
            ElementTree.indent(tree, "  ")
            tree.write(radiola_config, short_empty_elements=False, encoding="utf-8")
        else:
            dom = parseString(ElementTree.tostring(root))
            print(dom.toprettyxml())

    def update_tree(self) -> None:
        """Create Radiola file config"""

        self._body.findall

        # group: Element | None = SubElement(self._body, "outline")
        group: Element | None = None
        for channel in self._body.findall("ouline"):
            if channel.attrib["text"] == "SomaFM":
                # Clean all entries
                channel.clear()
                group = channel

        # We didn't found SomaFM channel group
        if not group:
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
