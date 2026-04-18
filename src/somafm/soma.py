# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro

from typing import Any

import requests

from . import logger, settings


class Soma:
    """Class to interact with feeds from Soma"""

    def __init__(self) -> None:
        self._channels: list[dict[str, Any]] = []
        self.populate()

    def populate(self) -> None:
        try:
            response = requests.get(
                settings.SOMAFM_URL,
                timeout=120,
            )
            response.raise_for_status()

            channels = response.json()
            self._channels = channels["channels"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Request not successful: {e}")
            return

    @property
    def channels(self) -> list[dict[str, Any]]:
        """Return the stored list of SomaFM channels

        Returns:
            List[Dict[str, str]] | None: Channel list or None
        """
        return self._channels
