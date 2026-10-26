# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from pathlib import Path
from typing import Any

import click
from appdirs import AppDirs
from lxml import etree
from pydantic_settings import BaseSettings
from rich import print as rprint

from somafm import logger
from somafm.soma import Soma


class Settings(BaseSettings):
    RADIOLA_APP_IDENTIFIER: str = "com.github.SokoloffA.Radiola"
    RADIOLA_CONFIG_FILE: Path = Path(AppDirs(RADIOLA_APP_IDENTIFIER).user_data_dir) / "bookmarks.opml"


class RadiolaPlugin:
    """Radiola Plugin
    Mac systemtray application
    """

    def __init__(
        self,
        update: bool = False,
        rewrite: bool = False,
    ) -> None:
        self._soma = Soma()
        self._update: bool = update
        self.body: Any

        settings: Settings = Settings()

        radiola_config: Path = settings.RADIOLA_CONFIG_FILE

        if radiola_config.exists():
            logger.info("Importing current config from Radiola.")
            tree = etree.parse(radiola_config)
            root = tree.getroot()
        else:
            logger.info("Creating new config to Radiola.")
            root = etree.Element("opml")
            root.set("version", "2.0")
            etree.SubElement(root, "head")
            etree.SubElement(root, "body")
            tree = etree.ElementTree(root)
        self.body = root.find("body")

        # Create the tree
        self.update_tree()

        if self._update:
            logger.info(f"Updating config file at {radiola_config}")
            tree.write(
                radiola_config,
                pretty_print=True,
                xml_declaration=True,
                encoding="UTF-8",
            )
        else:
            rprint(
                etree.tostring(
                    root,
                    pretty_print=True,
                    encoding="unicode",
                )
            )

    def find_group(self, name: str) -> Any:  # noqa: ANN401
        for outline in self.body.findall("outline"):
            if outline.get("text") == name and outline.get("group") == "true":
                return outline
        return None

    def find_radio(
        self,
        name: str,
        parent: Any = None,  # noqa: ANN401
    ) -> Any:  # noqa: ANN401
        search_element = parent if parent is not None else self.body
        for outline in search_element.findall("outline"):
            if outline.get("text") == name:
                return outline
        return None

    def update_tree(self) -> None:
        """Create Radiola file config"""

        group = self.find_group("SomaFM")

        # Create SomaFM channel group if it doesn't exist
        if group is None:
            group = etree.SubElement(
                self.body,
                "outline",
                text="SomaFM",
                group="true",
            )

        for channel in self._soma.channels:
            outline = self.find_radio(
                channel["title"],
                parent=group,
            )
            if outline is not None:
                for pls in channel["playlists"]:
                    if pls["format"] == "aac" and pls["quality"] == "highest":
                        if outline.get("url") != pls["url"]:
                            logger.warning(f"Channel {channel['title']} exists but url differs.")
                        break
            else:
                sub = etree.SubElement(group, "outline")
                sub.set("text", channel["title"])
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
