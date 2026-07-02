class AgentRegistry:

    def __init__(self):

        self.agents = {}

    def register(

        self,

        domain: str,

        agent

    ):

        self.agents[
            domain
        ] = agent

    def get_agent(

        self,

        domain: str

    ):

        return self.agents.get(
            domain
        )

    def list_agents(
        self
    ):

        return list(
            self.agents.keys()
        )