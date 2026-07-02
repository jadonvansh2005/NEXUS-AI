class DomainMapper:

    def map_domain(
        self,
        domain: str
    ) -> str:

        mapping = {

            # ==========================================
            # Core Domains
            # ==========================================

            "data_science":
                "Data Science",

            "travel":
                "Travel",

            "career":
                "Career",

            "coding":
                "Coding",

            "education":
                "Education",

            "finance":
                "Finance",

            "research":
                "Research",

            "business":
                "Business",

            "communication":
                "Communication",

            "healthcare":
                "Healthcare",

            "legal":
                "Legal",

            "productivity":
                "Productivity",

            "system":
                "System",

            "general":
                "General",
        }

        return mapping.get(
            domain,
            "General"
        )