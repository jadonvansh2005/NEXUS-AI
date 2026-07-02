class RoutingEngine:

    def route(self, domain: str):

        routes = {

            "data_science":
                "DataScienceAgent",

            "travel":
                "TravelAgent",

            "career":
                "CareerAgent",

            "coding":
                "CodingAgent",

            "healthcare":
                "HealthcareAgent"
        }

        return routes.get(
            domain,
            "GeneralAgent"
        )