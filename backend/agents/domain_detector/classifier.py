import re

class DomainClassifier:

    def classify(
        self,
        query: str
    ) -> str:

        query = query.lower()

        # Helper function for matching whole-word / whole-phrase with word boundaries
        def match_keyword(keywords) -> bool:
            for word in keywords:
                pattern = r"\b" + re.escape(word) + r"\b"
                if re.search(pattern, query):
                    return True
            return False

        # Force "general" domain for browser automation actions
        if match_keyword([
            "browser search",
            "web search",
            "screenshot",
            "download",
            "capture webpage",
            "capture page",
            "browser history",
            "search",
        ]):
            return "general"

        # ==========================================
        # Data Science
        # ==========================================
        if match_keyword([
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
            "prediction",
            "ml",
            "DL",
            "NLP"

        ]):
            return "data_science"

        # ==========================================
        # Travel
        # ==========================================
        if match_keyword([
            "travel",
            "trip", "trips",
            "flight", "flights",
            "hotel", "hotels",
            "train", "trains",
            "booking", "bookings",
            "book ticket", "book tickets",
            "visa", "visas",
            "passport", "passports",
            "airport", "airports",
            "airline", "airlines",
            "destination", "destinations",
            "tour", "tours",
            "tourist", "tourists",
            "vacation", "vacations",
            "holiday", "holidays",
            "itinerary", "itineraries",
            "cab", "cabs",
            "taxi", "taxis",
            "nearby places",
            "currency exchange",
            "packing",
            "travel insurance"
        ]):
            return "travel"

        # ==========================================
        # Career
        # ==========================================
        if match_keyword([
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
        ]):
            return "career"

        # ==========================================
        # Coding
        # ==========================================
        if match_keyword([
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
            "node",
            "node.js",
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
            "repository",
            "repo",
            "commit",
            "clone",
            "push",
            "pull request",
            "pr",
            "issue",
            "docker"
        ]):
            return "coding"

        # ==========================================
        # Education
        # ==========================================
        if match_keyword([
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
        ]):
            return "education"

        # ==========================================
        # Finance
        # ==========================================
        if match_keyword([
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
        ]):
            return "finance"

        # ==========================================
        # Research
        # ==========================================
        if match_keyword([
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
        ]):
            return "research"

        # ==========================================
        # Business
        # ==========================================
        if match_keyword([
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
        ]):
            return "business"

        # ==========================================
        # Communication
        # ==========================================
        if match_keyword([
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
        ]):
            return "communication"

        # ==========================================
        # Healthcare
        # ==========================================
        if match_keyword([
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
        ]):
            return "healthcare"

        # ==========================================
        # Legal
        # ==========================================
        if match_keyword([
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
        ]):
            return "legal"

        # ==========================================
        # Productivity
        # ==========================================
        if match_keyword([
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
        ]):
            return "productivity"

        # ==========================================
        # System
        # ==========================================
        if match_keyword([
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
        ]):
            return "system"

        # ==========================================
        # General
        # ==========================================
        return "general"