
from mcp_integration.tool_router import ToolRouter


def main():
    router = ToolRouter()

    cases = {
        "List files in the backend directory": "filesystem_mcp",
        'Read file "integration/mcp_client.py"': "filesystem_mcp",
        'Search for "*.py"': "filesystem_mcp",
        "Explain how a filesystem works": "upss",
        "Calculate the distance between two cities": "upss",
        "Create file test.txt": "upss",
        "Delete the file test.txt": "upss",
    }

    for query, expected in cases.items():
        actual = router.route(query)
        print(f"{'PASS' if actual == expected else 'FAIL'}: {query}")
        assert actual == expected, (
            f"Expected {expected!r}, received {actual!r}"
        )

    print("\nAll routing tests passed.")


if __name__ == "__main__":
    main()
