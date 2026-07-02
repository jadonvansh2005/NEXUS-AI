from sqlalchemy.orm import Session

from memory.episodic.episodic_memory import (
    EpisodicMemory
)


class EpisodicService:

    def save_event(

        self,

        db: Session,

        user_id: int,

        event_type: str,

        event: str

    ):

        memory = EpisodicMemory(

            user_id=user_id,

            event_type=event_type,

            event=event

        )

        db.add(
            memory
        )

        db.commit()

        db.refresh(
            memory
        )

        return memory

    def get_user_events(

        self,

        db: Session,

        user_id: int

    ):

        return (

            db.query(
                EpisodicMemory
            )

            .filter(
                EpisodicMemory.user_id
                == user_id
            )

            .order_by(
                EpisodicMemory.id.desc()
            )

            .all()

        )

    def get_latest_event(

        self,

        db: Session,

        user_id: int

    ):

        return (

            db.query(
                EpisodicMemory
            )

            .filter(
                EpisodicMemory.user_id
                == user_id
            )

            .order_by(
                EpisodicMemory.id.desc()
            )

            .first()

        )

    def get_recent_events(

        self,

        db: Session,

        user_id: int,

        limit: int = 10

    ):

        return (

            db.query(
                EpisodicMemory
            )

            .filter(
                EpisodicMemory.user_id
                == user_id
            )

            .order_by(
                EpisodicMemory.id.desc()
            )

            .limit(limit)

            .all()

        )
    
    def get_latest_decision(

        self,

        db: Session,

        user_id: int

    ):

        return (

            db.query(
                EpisodicMemory
            )

            .filter(
                EpisodicMemory.user_id
                == user_id
            )

            .filter(
                EpisodicMemory.event_type
                == "technology_decision"
            )

            .order_by(
                EpisodicMemory.id.desc()
            )

            .first()

        )
    

    def get_latest_milestone(

        self,

        db: Session,

        user_id: int

    ):

        return (

            db.query(
                EpisodicMemory
            )

            .filter(
                EpisodicMemory.user_id
                == user_id
            )

            .filter(
                EpisodicMemory.event_type
                == "milestone"
            )

            .order_by(
                EpisodicMemory.id.desc()
            )

            .first()

        )