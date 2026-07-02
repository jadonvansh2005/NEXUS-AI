"""
Retry Helper
"""

from __future__ import annotations

import asyncio
from typing import Callable


async def retry(
    func: Callable,
    retries: int = 3,
    delay: float = 1.0,
):

    last_exception = None

    for attempt in range(retries):

        try:

            return await func()

        except Exception as exc:

            last_exception = exc

            if attempt < retries - 1:

                await asyncio.sleep(delay)

    raise last_exception