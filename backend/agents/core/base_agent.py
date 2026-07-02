from abc import ABC, abstractmethod

from agents.core.agent_state import AgentState


class BaseAgent(ABC):

    def __init__(self, name: str):

        self.name = name

    @abstractmethod
    def execute(
        self,
        state: AgentState
    ) -> AgentState:
        pass

    def log(self, message: str):

        print(
            f"[{self.name}] {message}"
        )