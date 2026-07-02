from enum import Enum


# ==========================================================
# Metadata Version
# ==========================================================

METADATA_VERSION = "1.0"


# ==========================================================
# Source Types
# ==========================================================

class SourceType(Enum):

    CONVERSATION = "conversation"

    DOCUMENT = "document"

    SEMANTIC = "semantic"

    PROJECT = "project"

    KNOWLEDGE = "knowledge"

    CODE = "code"

    INTERNET = "internet"


# ==========================================================
# Memory Types
# ==========================================================

class MemoryType(Enum):

    FACT = "fact"

    PREFERENCE = "preference"

    DECISION = "decision"

    GOAL = "goal"

    HABIT = "habit"

    SKILL = "skill"

    PROFILE = "profile"


# ==========================================================
# Document Types
# ==========================================================

class DocumentType(Enum):

    PDF = "pdf"

    DOCX = "docx"

    PPTX = "pptx"

    XLSX = "xlsx"

    CSV = "csv"

    TXT = "txt"

    MARKDOWN = "md"

    HTML = "html"

    JSON = "json"

    XML = "xml"

    PYTHON = "py"

    JAVASCRIPT = "js"

    TYPESCRIPT = "ts"

    JAVA = "java"

    CPP = "cpp"

    C = "c"

    GO = "go"

    RUST = "rs"

    SQL = "sql"


# ==========================================================
# Project Modules
# ==========================================================

class ProjectModule(Enum):

    MEMORY = "memory"

    RAG = "rag"

    AGENT = "agent"

    CHAT = "chat"

    AUTH = "authentication"

    DATABASE = "database"

    API = "api"

    FRONTEND = "frontend"

    BACKEND = "backend"

    ANALYTICS = "analytics"

    WORKFLOW = "workflow"

    SETTINGS = "settings"


# ==========================================================
# Architecture Layers
# ==========================================================

class ArchitectureLayer(Enum):

    FRONTEND = "frontend"

    BACKEND = "backend"

    DATABASE = "database"

    INFRASTRUCTURE = "infrastructure"

    DEVOPS = "devops"

    AI = "ai"

    ML = "machine_learning"


# ==========================================================
# Conversation Roles
# ==========================================================

class ConversationRole(Enum):

    USER = "user"

    ASSISTANT = "assistant"

    SYSTEM = "system"

    TOOL = "tool"


# ==========================================================
# Importance Levels
# ==========================================================

class ImportanceLevel(Enum):

    LOW = 0.5

    NORMAL = 1.0

    HIGH = 2.0

    CRITICAL = 5.0


# ==========================================================
# Permanence
# ==========================================================

class Permanence(Enum):

    SHORT_TERM = "short_term"

    MEDIUM_TERM = "medium_term"

    LONG_TERM = "long_term"

    PERMANENT = "permanent"


# ==========================================================
# Supported Languages
# ==========================================================

class Language(Enum):

    ENGLISH = "en"

    HINDI = "hi"

    JAPANESE = "ja"

    CHINESE = "zh"

    FRENCH = "fr"

    GERMAN = "de"

    SPANISH = "es"

    ARABIC = "ar"

    RUSSIAN = "ru"


# ==========================================================
# Retrieval Types
# ==========================================================

class RetrievalType(Enum):

    VECTOR = "vector"

    KEYWORD = "keyword"

    HYBRID = "hybrid"

    BM25 = "bm25"

    GRAPH = "graph"


# ==========================================================
# Embedding Status
# ==========================================================

class EmbeddingStatus(Enum):

    PENDING = "pending"

    PROCESSING = "processing"

    COMPLETED = "completed"

    FAILED = "failed"