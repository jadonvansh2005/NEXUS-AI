from database.connection import (
    engine
)

from models.user import (
    Base,
    User
)

from memory.long_term.conversation import (
    Conversation
)

from memory.episodic.episodic_memory import (
    EpisodicMemory
)

from models.user_fact import (
    UserFact
)

from memory.long_term.message import (
    Message
)


def create_tables():

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "✅ Tables Created Successfully"
    )


if __name__ == "__main__":

    create_tables()