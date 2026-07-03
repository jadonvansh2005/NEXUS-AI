class TaskClassifier:

    def classify(
        self,
        query: str,
        domain: str
    ) -> str:

        query = query.lower()

        # If a specific domain is already detected, map it directly to align the task type
        if domain and domain != "general":
            return domain

        # ==========================================
        # Coding
        # ==========================================
        if any(
            word in query
            for word in [
                "code", "coding", "program", "programming", "bug", "debug",
                "python", "java", "c++", "javascript", "typescript", "react",
                "nextjs", "fastapi", "flask", "django", "api", "backend",
                "frontend", "website", "software", "algorithm", "git", "github",
                "docker"
            ]
        ):
            return "coding"

        # ==========================================
        # Research & Browser webpage reader keywords
        # ==========================================
        if any(
            word in query
            for word in [
                "research", "paper", "journal", "citation", "arxiv", "pubmed",
                "survey", "literature review", "reference", "publication", "doi",
                "read this webpage", "read webpage", "webpage", "read", "url", "link"
            ]
        ):
            return "research"

        # ==========================================
        # Data Science
        # ==========================================
        if any(
            word in query
            for word in [
                "dataset", "csv", "excel", "data", "eda", "data analysis",
                "analytics", "analysis", "data visualization", "visualization",
                "dashboard", "machine learning", "deep learning", "neural network",
                "regression", "classification", "clustering", "feature engineering",
                "data cleaning", "pandas", "numpy", "matplotlib", "seaborn",
                "xgboost", "model training", "prediction"
            ]
        ):
            return "data_science"

        # ==========================================
        # Travel
        # ==========================================
        if any(
            word in query
            for word in [
                "travel", "trip", "flight", "hotel", "train", "booking",
                "book ticket", "visa", "passport", "airport", "airline",
                "destination", "tour", "tourist", "vacation", "holiday",
                "itinerary", "cab", "taxi", "nearby places", "currency exchange",
                "packing", "travel insurance"
            ]
        ):
            return "travel"

        # ==========================================
        # Career
        # ==========================================
        if any(
            word in query
            for word in [
                "resume", "cv", "ats", "job", "career", "internship",
                "placement", "linkedin", "interview", "cover letter",
                "portfolio", "salary", "hiring", "recruiter"
            ]
        ):
            return "career"

        # ==========================================
        # Education
        # ==========================================
        if any(
            word in query
            for word in [
                "study", "education", "course", "lesson", "chapter", "exam",
                "assignment", "homework", "notes", "quiz", "college", "school",
                "teacher", "student", "learning", "syllabus"
            ]
        ):
            return "education"

        # ==========================================
        # Finance
        # ==========================================
        if any(
            word in query
            for word in [
                "finance", "money", "stock", "stocks", "market", "investment",
                "mutual fund", "portfolio", "crypto", "bitcoin", "trading", "tax",
                "gst", "invoice", "expense", "budget", "profit", "loss", "sip"
            ]
        ):
            return "finance"

        # ==========================================
        # Communication
        # ==========================================
        if any(
            word in query
            for word in [
                "whatsapp", "discord", "slack", "teams", "sms", "email", "mail",
                "message", "translate", "translation", "grammar", "rewrite",
                "rephrase", "tone", "meeting summary", "compose message",
                "communication", "send this mail"
            ]
        ):
            return "communication"

        # ==========================================
        # Other domains default
        # ==========================================
        return "general"