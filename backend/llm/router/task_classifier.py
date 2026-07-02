class TaskClassifier:

    def classify(
        self,
        query: str,
        domain: str
    ):

        query = query.lower()

        if any(
            word in query
            for word in [
                "code",
                "python",
                "bug",
                "fix",
                "program"
            ]
        ):
            return "coding"

        if any(
            word in query
            for word in [
                "research",
                "paper",
                "study",
                "analysis"
            ]
        ):
            return "research"

        if domain == "data_science":
            return "data_science"

        return "general"