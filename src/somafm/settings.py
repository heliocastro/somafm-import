# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Helio Chissini de Castro

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SOMAFM_URL: str = "https://somafm.com/channels.json"
