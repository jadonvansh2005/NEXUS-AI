from agents.domain_detector.classifier import (
    DomainClassifier
)

from agents.domain_detector.domain_mapper import (
    DomainMapper
)


class DomainDetector:
    """
    Detects the most relevant domain for a user query.
    """

    def __init__(self):

        self.classifier = DomainClassifier()

        self.mapper = DomainMapper()

    def detect(
        self,
        query: str
    ) -> dict:

        domain = self.classifier.classify(
            query
        )

        display_name = self.mapper.map_domain(
            domain
        )

        return {

            "domain": domain,

            "display_name": display_name,

            # Future-ready fields
            "confidence": 1.0,

            "detected_by": "keyword_classifier",

            "query": query

        }