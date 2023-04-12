# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import xml.etree.ElementTree as ET
from pathlib import Path

import click
from appdirs import AppDirs
from defusedxml.ElementTree import parse
from defusedxml.minidom import parseString
from defusedxml import defuse_stdlib

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
            tree = parse(radiola_config)
            root = tree.getroot()
            self._body = root.findall("body")
        else:
            root = ET.Element("ompl")
            root.set("version", "2.0")
            ET.SubElement(root, "head")
            self._body = ET.SubElement(root, "body")

        # Create the tree
        self.update_tree()

        tree = ET.ElementTree(root)
        if self._update:
            ET.indent(tree, "  ")
            tree.write(radiola_config, short_empty_elements=False, encoding="utf-8")
        else:
            dom = parseString(ET.tostring(root))
            print(dom.toprettyxml())

    def update_tree(self) -> None:
        """Create Radiola file config"""
        for channel in self._body[0]:
            if channel.attrib["text"] == "SomaFM":
                self._body[0].remove(channel)

        group = ET.SubElement(self._body[0], "outline")
        group.set("text", "SomaFM")
        group.set("group", "true")
        for channel in self._soma.channels:
            sub = ET.SubElement(group, "outline")
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
@click.option("--update/--no-update", default=False, help="Update the current file instead of print only")
def radiola(update: bool) -> None:
    RadiolaPlugin(update)
