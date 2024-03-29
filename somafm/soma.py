# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import json
import os
from typing import Any

import requests


class Soma:
    """Class to interact with feeds from Soma"""

    def __init__(self) -> None:
        self._channels: list[dict[str, Any]] = []
        self.populate()

    def populate(self) -> None:
        somafm_endpoint: str = os.getenv("SOMAFM_URL", default="https://somafm.com/channels.json")

        req = requests.get(somafm_endpoint, timeout=10)
        if req.status_code != requests.codes.ok:
            return
        channels = json.loads(req.text)
        self._channels = channels["channels"]

    @property
    def channels(self) -> list[dict[str, Any]]:
        """Return the stored list of SomaFM channels

        Returns:
            List[Dict[str, str]] | None: Channel list or None
        """
        return self._channels
