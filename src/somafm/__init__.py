# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro

import logging

from .settings import Settings

settings = Settings()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
