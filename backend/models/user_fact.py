from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from database.connection import Base


class UserFact(Base):

    __tablename__ = "user_facts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    fact_key = Column(
        String,
        nullable=False
    )

    fact_value = Column(
        String,
        nullable=False
    )