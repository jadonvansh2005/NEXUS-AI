from sqlalchemy.orm import Session

from memory.long_term.conversation import (
    Conversation
)

from memory.long_term.message import (
    Message
)


class MemoryService:

    def create_conversation(

        self,

        db: Session,

        user_id: int,

        title: str = "New Chat"

    ):

        conversation = Conversation(

            user_id=user_id,

            title=title

        )

        db.add(
            conversation
        )

        db.commit()

        db.refresh(
            conversation
        )

        return conversation

    def get_conversation(

        self,

        db: Session,

        conversation_id: int

    ):

        return (

            db.query(
                Conversation
            )

            .filter(
                Conversation.id
                == conversation_id
            )

            .first()

        )

    def get_user_conversations(

        self,

        db: Session,

        user_id: int

    ):

        return (

            db.query(
                Conversation
            )

            .filter(
                Conversation.user_id
                == user_id
            )

            .order_by(
                Conversation.id.desc()
            )

            .all()

        )

    def save_message(

        self,

        db: Session,

        conversation_id: int,

        role: str,

        content: str

    ):

        message = Message(

            conversation_id=conversation_id,

            role=role,

            content=content

        )

        db.add(
            message
        )

        db.commit()

        db.refresh(
            message
        )

        return message

    def get_conversation_messages(

        self,

        db: Session,

        conversation_id: int

    ):

        return (

            db.query(
                Message
            )

            .filter(
                Message.conversation_id
                == conversation_id
            )

            .order_by(
                Message.created_at.asc()
            )

            .all()

        )

    def get_recent_messages(

        self,

        db: Session,

        conversation_id: int,

        limit: int = 20

    ):

        return (

            db.query(
                Message
            )

            .filter(
                Message.conversation_id
                == conversation_id
            )

            .order_by(
                Message.id.asc()
            )

            .limit(
                limit
            )

            .all()

        )
    
    def delete_conversation(

        self,

        db,

        conversation_id: int

    ):

        db.query(Message).filter(

            Message.conversation_id
            == conversation_id

        ).delete()

        db.query(Conversation).filter(

            Conversation.id
            == conversation_id

        ).delete()

        db.commit()

        return True


    def get_conversation_by_user(

        self,

        db,

        conversation_id: int,

        user_id: int

    ):

        return (

            db.query(
                Conversation
            )

            .filter(
                Conversation.id
                == conversation_id
            )

            .filter(
                Conversation.user_id
                == user_id
            )

            .first()

        )