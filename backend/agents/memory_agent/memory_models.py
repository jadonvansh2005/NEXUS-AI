"""
Memory Models

Responsibilities

- Memory types
- Retrieval modes
- Memory importance
- Memory configuration

Used by

- Memory Agent
- Memory Router
- Memory Retriever
- Memory Writer
- Memory Manager
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


# ==========================================================
# Memory Type
# ==========================================================

class MemoryType(str, Enum):

    SHORT_TERM = "short_term"

    FACT = "fact"

    EPISODIC = "episodic"

    SEMANTIC = "semantic"

    LONG_TERM = "long_term"

    KNOWLEDGE = "knowledge"


# ==========================================================
# Retrieval Mode
# ==========================================================

class RetrievalMode(str, Enum):

    NONE = "none"

    FACT_ONLY = "fact_only"

    CONTEXT_ONLY = "context_only"

    KNOWLEDGE_ONLY = "knowledge_only"

    HYBRID = "hybrid"


# ==========================================================
# Memory Importance
# ==========================================================

class MemoryImportance(str, Enum):

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


# ==========================================================
# Memory Action
# ==========================================================

class MemoryAction(str, Enum):

    READ = "read"

    WRITE = "write"

    UPDATE = "update"

    DELETE = "delete"


# ==========================================================
# Memory Configuration
# ==========================================================

class MemoryConfiguration(BaseModel):

    enable_short_term: bool = True

    enable_fact_memory: bool = True

    enable_semantic_memory: bool = True

    enable_episodic_memory: bool = True

    enable_long_term_memory: bool = True

    enable_knowledge_memory: bool = True

    max_retrieved_memories: int = 10

    similarity_threshold: float = 0.75

    summarize_before_store: bool = True