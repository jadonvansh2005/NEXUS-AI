from sqlalchemy.orm import Session

from memory.fact_memory.fact_extractor import (
    FactExtractor
)

from memory.fact_memory.fact_service import (
    FactService
)


class FactManager:

    def __init__(self):

        self.extractor = (
            FactExtractor()
        )

        self.service = (
            FactService()
        )

    def process_message(

        self,

        db: Session,

        user_id: int,

        message: str

    ):

        facts = (

            self.extractor.extract(
                message
            )

        )

        print("MESSAGE =", message)
        print("EXTRACTED FACTS =", facts)

        for key, value in facts.items():

            self.service.save_fact(

                db=db,

                user_id=user_id,

                fact_key=key,

                fact_value=value

            )

        return facts

    def build_fact_context(

        self,

        db: Session,

        user_id: int

    ):

        facts = (

            self.service.get_user_facts(

                db=db,

                user_id=user_id

            )

        )

        if not facts:

            return ""

        context = []

        for fact in facts:

            context.append(

                f"{fact.fact_key}: {fact.fact_value}"

            )

        return "\n".join(
            context
        )