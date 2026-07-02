from dataclasses import Field, dataclass
from dataclasses import field

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class AgentState:

    # =====================================================
    # User Information
    # =====================================================

    user_query: str

    user_id: Optional[int] = None

    email: Optional[str] = None

    session_id: Optional[str] = None

    conversation_id: Optional[int] = None

    # =====================================================
    # Agent Information
    # =====================================================

    domain: str = ""

    execution_plan: List[str] = field(

        default_factory=list

    )

    planner_result: Optional[Any] = None

    workflow_result: Optional[Any] = None

    collaboration_result: Optional[Any] = None

    selected_tools: list = field(
        default_factory=list
    )

    tool_selection_result: Optional[Any] = None

    # =====================================================
    # Input Resources
    # =====================================================

    file_path: str = ""

    # =====================================================
    # Memory / RAG
    # =====================================================

    context: Dict[str, Any] = field(

        default_factory=dict

    )

    memory_context: str = ""

    prompt: str = ""

    retrieved_sources: List[str] = field(

        default_factory=list

    )

    # =====================================================
    # Tool Layer
    # =====================================================

    tool_outputs: Dict[str, Any] = field(

        default_factory=dict

    )

    # =====================================================
    # LLM
    # =====================================================

    llm_provider: str = ""

    llm_model: str = ""

    # =====================================================
    # Final Output
    # =====================================================

    response: str = ""

    final_response: str = ""

    # =====================================================
    # Metadata
    # =====================================================

    metadata: Dict[str, Any] = field(

        default_factory=dict

    )


    