import importlib
import pkgutil

from agents.registry.registry import (
    AgentRegistry
)

import agents.domains


class AgentFactory:

    @staticmethod
    def build():

        registry = AgentRegistry()

        for _, module_name, _ in pkgutil.iter_modules(
            agents.domains.__path__
        ):

            try:

                module = importlib.import_module(

                    f"agents.domains.{module_name}.{module_name}_agent"

                )

                class_name = "".join(

                    word.capitalize()

                    for word in module_name.split("_")

                ) + "Agent"

                agent_class = getattr(
                    module,
                    class_name
                )

                registry.register(

                    module_name,

                    agent_class()

                )

                print(
                    f"[Registry] Loaded {class_name}"
                )

            except Exception as e:

                print(
                    f"[Registry] Failed {module_name}: {e}"
                )

        return registry