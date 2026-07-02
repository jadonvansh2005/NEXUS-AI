from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from database.connection import (
    SessionLocal
)

from auth.jwt.auth_dependency import (
    get_current_user
)

from memory.long_term.memory_service import (
    MemoryService
)

router = APIRouter()

memory_service = (
    MemoryService()
)


@router.get("/")
def get_conversations(

    current_user=Depends(
        get_current_user
    )

):

    db = SessionLocal()

    try:

        conversations = (

            memory_service.get_user_conversations(

                db=db,

                user_id=current_user.id

            )

        )

        return [

            {

                "id":
                    conv.id,

                "title":
                    conv.title,

                "created_at":
                    conv.created_at

            }

            for conv in conversations

        ]

    finally:

        db.close()


@router.get("/{conversation_id}")
def get_conversation(

    conversation_id: int,

    current_user=Depends(
        get_current_user
    )

):

    db = SessionLocal()

    try:

        conversation = (

            memory_service.get_conversation_by_user(

                db=db,

                conversation_id=conversation_id,

                user_id=current_user.id

            )

        )

        if not conversation:

            raise HTTPException(

                status_code=404,

                detail="Conversation Not Found"

            )

        messages = (

            memory_service.get_conversation_messages(

                db=db,

                conversation_id=conversation_id

            )

        )

        return {

            "conversation_id":
                conversation.id,

            "title":
                conversation.title,

            "messages": [

                {

                    "role":
                        msg.role,

                    "content":
                        msg.content,

                    "created_at":
                        msg.created_at

                }

                for msg in messages

            ]

        }

    finally:

        db.close()


@router.delete("/{conversation_id}")
def delete_conversation(

    conversation_id: int,

    current_user=Depends(
        get_current_user
    )

):

    db = SessionLocal()

    try:

        conversation = (

            memory_service.get_conversation_by_user(

                db=db,

                conversation_id=conversation_id,

                user_id=current_user.id

            )

        )

        if not conversation:

            raise HTTPException(

                status_code=404,

                detail="Conversation Not Found"

            )

        memory_service.delete_conversation(

            db=db,

            conversation_id=conversation_id

        )

        return {

            "message":
                "Conversation Deleted"

        }

    finally:

        db.close()