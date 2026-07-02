"""
Authentication Helpers
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class APIKeyAuth:

    api_key: str

    header_name: str = "Authorization"

    prefix: str = "Bearer"

    def headers(self):

        return {

            self.header_name:

            f"{self.prefix} {self.api_key}"

        }