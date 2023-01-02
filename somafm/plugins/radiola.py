# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
import xml.dom.minidom
import xml.etree.ElementTree as ET

import click

from somafm.soma import Soma


class RadiolaPlugin:
    """Radiola Plugin
    Mac systemtray application
    """

    def __init__(self) -> None:
        self._soma = Soma()

    def create_tree(self) -> None:
        """Create Radiola file config"""
        root = ET.Element("opml")
        root.set("version", "2.0")
        ET.SubElement(root, "head")
        body = ET.SubElement(root, "body")
        for channel in self._soma.channels:
            sub = ET.SubElement(body, "outline")
            sub.set("text", channel["title"])
            for pls in channel["playlists"]:
                if pls["format"] == "aac" and pls["quality"] == "highest":
                    sub.set("url", pls["url"])
                    break
            sub.set("fav", "false")

        tree = ET.ElementTree(root)
        tree.write("bookmarks.opml", short_empty_elements=False)

        dom = xml.dom.minidom.parseString(ET.tostring(root))
        print(dom.toprettyxml())


@click.group()
def plugin_group() -> None:
    pass


@plugin_group.command()
@click.option("--message", default="Hello World", help="Message to hello")
def radiola(message: str) -> None:
    plugin = RadiolaPlugin()
    plugin.create_tree()
