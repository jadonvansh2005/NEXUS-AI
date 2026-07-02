from memory.long_term.message import (
    Message
)

from memory.long_term.conversation import (
    Conversation
)


class RecallService:

    def get_user_messages(

        self,

        db,

        user_id: int

    ):

        return (

            db.query(Message)

            .join(

                Conversation,

                Message.conversation_id
                ==
                Conversation.id

            )

            .filter(

                Conversation.user_id
                ==
                user_id

            )

            .order_by(

                Message.id.desc()

            )

            .all()

        )

    def search_history(

        self,

        db,

        user_id: int,

        query: str

    ):

        messages = (

            self.get_user_messages(

                db=db,

                user_id=user_id

            )

        )

        query_words = set(

            query.lower().split()

        )

        scored = []

        for msg in messages:

            content_words = set(

                msg.content.lower().split()

            )

            score = len(

                query_words.intersection(

                    content_words

                )

            )

            if score > 0:

                scored.append(

                    (

                        score,

                        msg.content

                    )

                )

        scored.sort(

            reverse=True

        )

        return [

            item[1]

            for item in scored[:5]

        ]