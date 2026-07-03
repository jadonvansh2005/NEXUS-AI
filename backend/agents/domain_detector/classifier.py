class DomainClassifier:

    def classify(
        self,
        query: str
    ) -> str:

        query = query.lower()

        # ==========================================
        # Data Science
        # ==========================================

        if any(
            word in query
            for word in [

                "dataset",
                "csv",
                "excel",
                "data",
                "eda",
                "data analysis",
                "analytics",
                "analysis",
                "data visualization",
                "visualization",
                "dashboard",
                "machine learning",
                "deep learning",
                "neural network",
                "regression",
                "classification",
                "clustering",
                "feature engineering",
                "data cleaning",
                "pandas",
                "numpy",
                "matplotlib",
                "seaborn",
                "xgboost",
                "model training",
                "prediction"

            ]
        ):
            return "data_science"

        # ==========================================
        # Travel
        # ==========================================

        if any(
            word in query
            for word in [

                "travel",
                "trip",
                "flight",
                "hotel",
                "train",
                "booking",
                "book ticket",
                "visa",
                "passport",
                "airport",
                "airline",
                "destination",
                "tour",
                "tourist",
                "vacation",
                "holiday",
                "itinerary",
                "cab",
                "taxi",
                "nearby places",
                "currency exchange",
                "packing",
                "travel insurance"

            ]
        ):
            return "travel"

        # ==========================================
        # Career
        # ==========================================

        if any(
            word in query
            for word in [

                "resume",
                "cv",
                "ats",
                "job",
                "career",
                "internship",
                "placement",
                "linkedin",
                "interview",
                "cover letter",
                "portfolio",
                "salary",
                "hiring",
                "recruiter"

            ]
        ):
            return "career"

        # ==========================================
        # Coding
        # ==========================================

        if any(
            word in query
            for word in [

                "code",
                "coding",
                "program",
                "programming",
                "bug",
                "debug",
                "python",
                "java",
                "c++",
                "javascript",
                "typescript",
                "react",
                "nextjs",
                "fastapi",
                "flask",
                "django",
                "api",
                "backend",
                "frontend",
                "website",
                "software",
                "algorithm",
                "git",
                "github",
                "docker"

            ]
        ):
            return "coding"

        # ==========================================
        # Education
        # ==========================================

        if any(
            word in query
            for word in [

                "study",
                "education",
                "course",
                "lesson",
                "chapter",
                "exam",
                "assignment",
                "homework",
                "notes",
                "quiz",
                "college",
                "school",
                "teacher",
                "student",
                "learning",
                "syllabus"

            ]
        ):
            return "education"

        # ==========================================
        # Finance
        # ==========================================

        if any(
            word in query
            for word in [

                "finance",
                "money",
                "stock",
                "stocks",
                "market",
                "investment",
                "mutual fund",
                "portfolio",
                "crypto",
                "bitcoin",
                "trading",
                "tax",
                "gst",
                "invoice",
                "expense",
                "budget",
                "profit",
                "loss",
                "sip"

            ]
        ):
            return "finance"

        # ==========================================
        # Research
        # ==========================================

        if any(
            word in query
            for word in [

                "research",
                "paper",
                "journal",
                "citation",
                "arxiv",
                "pubmed",
                "survey",
                "literature review",
                "reference",
                "publication",
                "doi",
                "read this webpage"

            ]
        ):
            return "research"

        # ==========================================
        # Business
        # ==========================================

        if any(
            word in query
            for word in [

                "business",
                "startup",
                "company",
                "customer",
                "marketing",
                "sales",
                "revenue",
                "strategy",
                "product",
                "branding",
                "business plan",
                "entrepreneur"

            ]
        ):
            return "business"

        # ==========================================
        # Communication
        # ==========================================

        if any(
            word in query
            for word in [

                "whatsapp",
                "discord",
                "slack",
                "teams",
                "sms",
                "email",
                "message",
                "translate",
                "translation",
                "grammar",
                "rewrite",
                "rephrase",
                "tone",
                "meeting summary",
                "compose message",
                "communication",
                "send this mail"

            ]
        ):
            return "communication"

        # ==========================================
        # Healthcare
        # ==========================================

        if any(
            word in query
            for word in [

                "doctor",
                "hospital",
                "health",
                "healthcare",
                "disease",
                "symptom",
                "medicine",
                "tablet",
                "diabetes",
                "blood pressure",
                "fever",
                "treatment",
                "diagnosis"

            ]
        ):
            return "healthcare"

        # ==========================================
        # Legal
        # ==========================================

        if any(
            word in query
            for word in [

                "legal",
                "law",
                "court",
                "judge",
                "advocate",
                "lawyer",
                "contract",
                "agreement",
                "license",
                "copyright",
                "patent",
                "trademark",
                "legal notice"

            ]
        ):
            return "legal"

        # ==========================================
        # Productivity
        # ==========================================

        if any(
            word in query
            for word in [

                "calendar",
                "schedule",
                "meeting",
                "todo",
                "task",
                "reminder",
                "productivity",
                "plan my day",
                "organize",
                "time management"

            ]
        ):
            return "productivity"

        # ==========================================
        # System
        # ==========================================

        if any(
            word in query
            for word in [

                "settings",
                "profile",
                "logout",
                "login",
                "memory",
                "preferences",
                "account",
                "configuration",
                "system",
                "connect gmail",
                "connect account"

            ]
        ):
            return "system"

        # ==========================================
        # General
        # ==========================================

        return "general"