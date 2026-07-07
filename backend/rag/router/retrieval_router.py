from typing import Dict
from typing import List
from typing import Any
from typing import Optional

from rag.pipelines.conversation_pipeline import (
    ConversationPipeline
)

from rag.pipelines.document_pipeline import (
    DocumentPipeline
)

from rag.pipelines.semantic_pipeline import (
    SemanticPipeline
)

from rag.pipelines.project_pipeline import (
    ProjectPipeline
)

from rag.pipelines.knowledge_pipeline import (
    KnowledgePipeline
)

from rag.pipelines.code_pipeline import (
    CodePipeline
)

from rag.vector_store.vector_schema import (
    SearchResult
)


class RetrievalRouter:

    def __init__(

        self

    ):

        self.conversation = (

            ConversationPipeline()

        )

        self.document = (

            DocumentPipeline()

        )

        self.semantic = (

            SemanticPipeline()

        )

        self.project = (

            ProjectPipeline()

        )

        self.knowledge = (

            KnowledgePipeline()

        )

        self.code = (

            CodePipeline()

        )

    # --------------------------------------------------
    # Route Query
    # --------------------------------------------------

    def classify_query(self, query: str) -> List[str]:
        import re
        query_lower = query.lower()
        routes = []

        def match_keyword(keywords) -> bool:
            for kw in keywords:
                pattern = r"\b" + re.escape(kw) + r"\b"
                if re.search(pattern, query_lower):
                    return True
            return False

        # 1. Document Routing
        doc_keywords = ["document", "pdf", "file", "csv", "excel", "xlsx", "chapter", "summarize", "docx", "paper", "text file", "read file", "uploaded"]
        if match_keyword(doc_keywords):
            routes.append("document")

        # 2. Code Routing
        code_keywords = ["code", "function", "class", "method", "variable", "python", "javascript", "react", "typescript", "fastapi", "implement", "repository", "github", "file structure", "backend", "frontend", "login", "auth", "api", "route"]
        if match_keyword(code_keywords):
            routes.append("code")

        # 3. Project Routing
        project_keywords = ["project", "upss", "architecture", "system design", "workflow", "roadmap", "tech stack", "agents", "multi-agent", "orchestrator", "planner", "reporting", "model router"]
        if match_keyword(project_keywords):
            routes.append("project")

        # 4. Conversation Routing
        conv_keywords = ["conversation", "discuss", "chat", "history", "previous", "earlier", "last time", "we talked", "you said", "i said"]
        if match_keyword(conv_keywords):
            routes.append("conversation")

        # 5. Semantic Routing (user preference)
        semantic_keywords = ["my name", "who am i", "my preference", "i prefer", "user preference", "my info", "profile", "about me"]
        if match_keyword(semantic_keywords):
            routes.append("semantic")

        # 6. Knowledge Routing (policies, general company facts)
        knowledge_keywords = ["policy", "sop", "faq", "hr", "company", "employee", "guidelines", "rules", "organization"]
        if match_keyword(knowledge_keywords):
            routes.append("knowledge")

        # Strict document override: if the user explicitly references "this file/pdf/document"
        # or "uploaded file/pdf/document", route ONLY to the document pipeline to avoid
        # conflicts with internal system code or project database.
        document_pointers = [
            "this file", "this pdf", "this document", "this csv", "this docx",
            "uploaded file", "uploaded pdf", "uploaded document", "uploaded csv",
            "in the file", "in the pdf", "in the document", "in the csv",
            "in this file", "in this pdf", "in this document"
        ]
        if any(ptr in query_lower for ptr in document_pointers):
            routes = ["document"]

        # If no specific route matched, try Gemini classification
        if not routes:
            try:
                from llm.providers.gemini.gemini_client import GeminiClient
                client = GeminiClient()
                prompt = (
                    "You are a query router for a Retrieval-Augmented Generation (RAG) system.\n"
                    "Your job is to classify the user query into one or more of these categories:\n"
                    "1. 'conversation': References to chat history, past discussions, or previous user/assistant exchanges.\n"
                    "2. 'document': Questions about uploaded files, PDFs, CSVs, chapters, or documentation.\n"
                    "3. 'semantic': Questions about user preferences, personal details (like name, age), or profile info.\n"
                    "4. 'project': Questions about the UPSS project, its system architecture, workflow, roadmap, or design decisions.\n"
                    "5. 'knowledge': Corporate/general knowledge base questions, SOPs, policies, HR FAQs.\n"
                    "6. 'code': Programming code, technical implementation, backend, routing, frontend components.\n"
                    "7. 'none': General conversation, greetings, general knowledge questions (like 'what is python', 'how are you', 'tell me a joke') that do not require specialized local context.\n\n"
                    f"User Query: \"{query}\"\n\n"
                    "Output ONLY a comma-separated list of categories that are highly relevant to answering the query (e.g. 'code, project', 'document', or 'none'). Do not output any other text."
                )
                response = client.generate(prompt).strip().lower()
                if "none" in response:
                    routes = ["conversation"]
                else:
                    for source in ["conversation", "document", "semantic", "project", "knowledge", "code"]:
                        if source in response:
                            routes.append(source)
            except Exception as e:
                print(f"[Router LLM Classify Failed] {e}")
                # Fallback: run a default set of retrievers
                routes = ["conversation"]

        # Ensure we always have at least one route
        if not routes:
            routes = ["conversation"]

        return list(set(routes))

    def route(
        self,
        query: str,
        limit: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[
        str,
        List[SearchResult]
    ]:
        active_routes = self.classify_query(query)
        print(f"\n[Retrieval Router] Active Routes for query: {active_routes}")

        retrieval_results = {
            "conversation": [],
            "document": [],
            "semantic": [],
            "project": [],
            "knowledge": [],
            "code": []
        }

        if "conversation" in active_routes:
            try:
                retrieval_results["conversation"] = self.conversation.retrieve(query=query, limit=limit, filters=filters)
            except Exception as e:
                print(f"[Retrieval Router Error] Failed conversation retrieval: {e}")

        if "document" in active_routes:
            try:
                retrieval_results["document"] = self.document.retrieve(query=query, limit=limit, filters=filters)
            except Exception as e:
                print(f"[Retrieval Router Error] Failed document retrieval: {e}")

        if "semantic" in active_routes:
            try:
                retrieval_results["semantic"] = self.semantic.retrieve(query=query, limit=limit, filters=filters)
            except Exception as e:
                print(f"[Retrieval Router Error] Failed semantic retrieval: {e}")

        if "project" in active_routes:
            try:
                retrieval_results["project"] = self.project.retrieve(query=query, limit=limit, filters=filters)
            except Exception as e:
                print(f"[Retrieval Router Error] Failed project retrieval: {e}")

        if "knowledge" in active_routes:
            try:
                retrieval_results["knowledge"] = self.knowledge.retrieve(query=query, limit=limit, filters=filters)
            except Exception as e:
                print(f"[Retrieval Router Error] Failed knowledge retrieval: {e}")

        if "code" in active_routes:
            try:
                retrieval_results["code"] = self.code.retrieve(query=query, limit=limit, filters=filters)
            except Exception as e:
                print(f"[Retrieval Router Error] Failed code retrieval: {e}")

        return retrieval_results

    # --------------------------------------------------
    # Available Pipelines
    # --------------------------------------------------

    @staticmethod

    def available_sources(

    ) -> List[str]:

        return [

            "conversation",

            "document",

            "semantic",

            "project",

            "knowledge",

            "code"

        ]