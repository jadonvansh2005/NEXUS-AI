from agents.registry.registry import (
    AgentRegistry
)


class DummyAgent:

    pass


def test_registry():

    registry = AgentRegistry()

    registry.register(
        "data_science",
        DummyAgent()
    )

    agent = registry.get_agent(
        "data_science"
    )

    assert agent is not None


if __name__ == "__main__":

    test_registry()

    print("PASSED")