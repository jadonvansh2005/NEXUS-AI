import asyncio

from integration.mcp_client import CombinedMCPClient
from mcp_integration.filesystem_handler import FilesystemMCPHandler


async def main():
    async with CombinedMCPClient() as client:
        handler = FilesystemMCPHandler(client)

        queries = [
            "List files in the backend directory",
            'Read file "integration/mcp_client.py"',
            'Search for "*.py" in the backend directory',
        ]

        for query in queries:
            print(f"\nUSER: {query}")
            result = await handler.handle_query(query)
            print("RESULT:", result)


if __name__ == "__main__":
    asyncio.run(main())