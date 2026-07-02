"""
UPSS HTTP Client
"""

from __future__ import annotations

import httpx

from tools.http.retry import retry


class HTTPClient:

    def __init__(

        self,

        timeout: int = 30,

    ):

        self.timeout = timeout

        self.client = httpx.AsyncClient(

            timeout=timeout

        )

    async def get(

        self,

        url: str,

        **kwargs,

    ):

        async def request():

            response = await self.client.get(

                url,

                **kwargs,

            )

            response.raise_for_status()

            return response

        return await retry(request)

    async def post(

        self,

        url: str,

        **kwargs,

    ):

        async def request():

            response = await self.client.post(

                url,

                **kwargs,

            )

            response.raise_for_status()

            return response

        return await retry(request)

    async def close(self):

        await self.client.aclose()