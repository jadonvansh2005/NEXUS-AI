from memory.fact_memory.fact_service import (
    FactService
)

from memory.recall.recall_service import (
    RecallService
)

from typing import List

from agents.memory_agent.memory_models import (
    MemoryType,
)

from agents.memory_agent.memory_state import (
    MemoryState,
)




class MemoryRouter:

    def __init__(self):

        self.fact_service = (
            FactService()
        )

        self.recall_service = (
            RecallService()
        )

        self.fact_patterns = {

            "name": [
                "what is my name",
                "tell me my name",
                "do you know my name"
            ],

            "nickname": [
                "what is my nickname",
                "what do friends call me",
                "what do people call me",
                "what should you call me"
            ],

            "location": [
                "where do i live",
                "where am i from",
                "where do i stay",
                "where do i reside",
                "what is my location"
            ],

            "hometown": [
                "what is my hometown",
                "where is my hometown",
                "what is my native place",
                "where is my native place"
            ],

            "college": [
                "which college do i study in",
                "where do i study",
                "what is my college",
                "which college do i attend"
            ],

            "branch": [
                "which branch am i in",
                "what is my branch",
                "what is my stream",
                "what branch do i study"
            ],

            "learning": [
                "what am i learning",
                "what am i studying",
                "what framework am i learning",
                "what tech am i learning"
            ],

            "project": [
                "what project am i building",
                "which project am i building",
                "what am i building",
                "what project am i working on",
                "what is my project"
            ],

            "career_goal": [
                "what is my goal",
                "what is my career goal",
                "what do i want to become",
                "what is my dream job"
            ],

            "dream_company": [
                "what is my dream company",
                "where do i want to work",
                "which company do i want to join",
                "my dream company"
            ],

            "favorite_language": [
                "what is my favorite language",
                "what language do i like coding in",
                "my favorite language",
                "what programming language do i prefer"
            ],

            "likes": [
                "what i like",
                "what do i like",
                "what do i love",
                "what do i enjoy",
                "my hobbies",
                "what are my hobbies"
            ],

            "favorite_subject": [
                "what is my favorite subject",
                "my favorite subject",
                "what subject do i like"
            ],

            "job_role": [
                "what is my job role",
                "what do i work as",
                "what is my role",
                "what is my job"
            ],

            "skills": [
                "what are my skills",
                "what am i skilled in",
                "what experience do i have",
                "what do i know"
            ],

            "age": [
                "how old am i",
                "what is my age",
                "tell me my age"
            ]

        }

    def try_answer(

        self,

        db,

        user_id: int,

        query: str

    ):

        query = query.strip().lower()

        # 1. Name query
        if ("what" in query or "who" in query or "tell" in query) and ("name" in query or "nickname" in query or "call" in query):
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="nickname")
            if fact:
                return f"nickname: {fact.fact_value}"
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="name")
            if fact:
                return f"name: {fact.fact_value}"

        # 2. Learning query
        if ("what" in query or "tell" in query) and ("learning" in query or "studying" in query or "study" in query):
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="learning")
            if fact:
                return f"learning: {fact.fact_value}"

        # 3. Project query
        if ("what" in query or "tell" in query) and ("project" in query or "building" in query or "work" in query):
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="project")
            if fact:
                return f"project: {fact.fact_value}"

        # 4. Likes query
        if ("what" in query or "tell" in query) and ("like" in query or "love" in query or "enjoy" in query or "hobby" in query or "hobbies" in query):
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="likes")
            if fact:
                return f"likes: {fact.fact_value}"

        # 5. Location query
        if ("where" in query or "what" in query) and ("live" in query or "from" in query or "stay" in query or "reside" in query or "location" in query):
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="location")
            if fact:
                return f"location: {fact.fact_value}"

        # 6. Hometown query
        if "hometown" in query or "native" in query:
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="hometown")
            if fact:
                return f"hometown: {fact.fact_value}"

        # 7. College query
        if "college" in query or "institute" in query or "university" in query or "enrolled" in query:
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="college")
            if fact:
                return f"college: {fact.fact_value}"

        # 8. Branch query
        if "branch" in query or "stream" in query or "major" in query:
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="branch")
            if fact:
                return f"branch: {fact.fact_value}"

        # 9. Career Goal query
        if "goal" in query or "become" in query or "dream job" in query:
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="career_goal")
            if fact:
                return f"career_goal: {fact.fact_value}"

        # 10. Dream Company query
        if "dream company" in query or "work at" in query:
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="dream_company")
            if fact:
                return f"dream_company: {fact.fact_value}"

        # 11. Favorite Language query
        if "favorite language" in query or "coding language" in query or "programming language" in query:
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="favorite_language")
            if fact:
                return f"favorite_language: {fact.fact_value}"

        # 12. Favorite Subject query
        if "favorite subject" in query:
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="favorite_subject")
            if fact:
                return f"favorite_subject: {fact.fact_value}"

        # 13. Job Role query
        if "job role" in query or "work as" in query or "my role" in query:
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="job_role")
            if fact:
                return f"job_role: {fact.fact_value}"

        # 14. Skills query
        if "skills" in query or "skilled" in query or "experience" in query:
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="skills")
            if fact:
                return f"skills: {fact.fact_value}"

        # 15. Age query
        if "age" in query or "old" in query:
            fact = self.fact_service.get_fact(db=db, user_id=user_id, fact_key="age")
            if fact:
                return f"age: {fact.fact_value}"

        # Fallback to the patterns loop if none of the quick matches hit
        for fact_key, patterns in self.fact_patterns.items():
            for pattern in patterns:
                if pattern in query:
                    fact = self.fact_service.get_fact(
                        db=db,
                        user_id=user_id,
                        fact_key=fact_key
                    )
                    if fact:
                        return f"{fact_key.lower()}: {fact.fact_value}"

        return None
    
    def search_conversation_history(

        self,

        db,

        user_id: int,

        query: str

    ):

        messages = (

            self.recall_service.get_user_messages(

                db=db,

                user_id=user_id

            )

        )

        query = query.lower()

        if "name" in query:

            for msg in messages:

                text = msg.content.lower()

                if "my name is" in text:

                    return msg.content

                if "this is" in text:

                    return msg.content

        return None
    


    # =====================================================
    # Memory Routing
    # =====================================================

    def route(

        self,

        state: MemoryState,

    ) -> List[MemoryType]:

        """
        Decide which memory stores should be queried
        for the current user query.

        NOTE:
        This method DOES NOT retrieve memory.
        It only decides which memory sources
        should be used.

        Existing methods like try_answer()
        and search_conversation_history()
        remain untouched.
        """

        query = state.query.lower()

        routes: List[MemoryType] = []

        # -------------------------------------------------
        # Fact Memory
        # -------------------------------------------------

        if any(

            word in query

            for word in [

                "my",

                "me",

                "mine",

                "remember",

                "preference",

                "favorite",

            ]

        ):

            routes.append(

                MemoryType.FACT

            )

        # -------------------------------------------------
        # Episodic Memory
        # -------------------------------------------------

        if any(

            word in query

            for word in [

                "last",

                "previous",

                "earlier",

                "before",

                "conversation",

                "recent",

            ]

        ):

            routes.append(

                MemoryType.EPISODIC

            )

        # -------------------------------------------------
        # Semantic Memory
        # -------------------------------------------------

        if any(

            word in query

            for word in [

                "project",

                "architecture",

                "workflow",

                "system",

                "agent",

            ]

        ):

            routes.append(

                MemoryType.SEMANTIC

            )

        # -------------------------------------------------
        # Knowledge Memory (RAG)
        # -------------------------------------------------

        if any(

            word in query

            for word in [

                "explain",

                "research",

                "paper",

                "documentation",

                "guide",

                "manual",

            ]

        ):

            routes.append(

                MemoryType.KNOWLEDGE

            )

        # -------------------------------------------------
        # Short-Term Memory
        # -------------------------------------------------

        routes.append(

            MemoryType.SHORT_TERM

        )

        # -------------------------------------------------
        # Remove duplicates
        # -------------------------------------------------

        state.requested_memory_types = list(

            dict.fromkeys(

                routes

            )

        )

        return state.requested_memory_types