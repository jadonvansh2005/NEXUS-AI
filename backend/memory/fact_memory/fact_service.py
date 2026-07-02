from sqlalchemy.orm import Session

from models.user_fact import (
    UserFact
)


class FactService:

    def save_fact(

        self,

        db: Session,

        user_id: int,

        fact_key: str,

        fact_value: str

    ):

        existing_fact = (

            db.query(UserFact)

            .filter(
                UserFact.user_id
                == user_id
            )

            .filter(
                UserFact.fact_key
                == fact_key
            )

            .first()

        )

        if existing_fact:

            existing_fact.fact_value = (
                fact_value
            )

            db.commit()

            db.refresh(
                existing_fact
            )

            print(

                f"[FACT UPDATED] "

                f"{fact_key} = {fact_value}"

            )

            return existing_fact

        fact = UserFact(

            user_id=user_id,

            fact_key=fact_key,

            fact_value=fact_value

        )

        db.add(
            fact
        )

        db.commit()

        db.refresh(
            fact
        )

        print(

            f"[FACT SAVED] "

            f"{fact_key} = {fact_value}"

        )

        return fact

    def get_user_facts(

        self,

        db: Session,

        user_id: int

    ):

        return (

            db.query(UserFact)

            .filter(
                UserFact.user_id
                == user_id
            )

            .all()

        )

    def get_fact(

        self,

        db: Session,

        user_id: int,

        fact_key: str

    ):

        return (

            db.query(UserFact)

            .filter(
                UserFact.user_id
                == user_id
            )

            .filter(
                UserFact.fact_key
                == fact_key
            )

            .first()

        )