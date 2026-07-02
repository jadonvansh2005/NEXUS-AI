class PromptBuilder:

    def __init__(

        self

    ):

        self.default_system_prompt = (

            "You are UPSS AI, an intelligent assistant. "

            "Answer using the retrieved context whenever possible. "

            "If the answer is not present in the context, "

            "clearly state that the information is unavailable "

            "instead of making up facts."

        )

    # --------------------------------------------------
    # Build Prompt
    # --------------------------------------------------

    def build(

        self,

        user_query: str,

        context: str,

        system_prompt: str | None = None

    ) -> str:

        system = (

            system_prompt

            if system_prompt

            else self.default_system_prompt

        )

        sections = [

            "========== SYSTEM ==========",

            system,

            "",

            "========== RETRIEVED CONTEXT ==========",

            context if context else "No context retrieved.",

            "",

            "========== USER QUESTION ==========",

            user_query,

            "",

            "========== ASSISTANT =========="

        ]

        return (

            "\n".join(

                sections

            )

        )

    # --------------------------------------------------
    # Custom System Prompt
    # --------------------------------------------------

    def set_system_prompt(

        self,

        prompt: str

    ) -> None:

        self.default_system_prompt = (

            prompt

        )

    # --------------------------------------------------
    # Reset System Prompt
    # --------------------------------------------------

    def reset_system_prompt(

        self

    ) -> None:

        self.default_system_prompt = (

            "You are UPSS AI, an intelligent assistant. "

            "Answer using the retrieved context whenever possible. "

            "If the answer is not present in the context, "

            "clearly state that the information is unavailable "

            "instead of making up facts."

        )