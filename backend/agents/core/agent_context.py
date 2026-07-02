from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentContext:

    session_id: str

    user_id: str

    timestamp: datetime