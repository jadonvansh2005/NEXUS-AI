from memory.long_term.memory_service import (
    MemoryService
)


class MemoryManager:

    def __init__(self):

        self.memory_service = (
            MemoryService()
        )

    def build_context(

        self,

        db,

        conversation_id: int

    ):

        messages = (

            self.memory_service

            .get_recent_messages(

                db=db,

                conversation_id=conversation_id

            )

        )

        context = []

        for msg in messages:

            context.append(

                f"{msg.role}: {msg.content}"

            )

        return "\n".join(
            context
        )