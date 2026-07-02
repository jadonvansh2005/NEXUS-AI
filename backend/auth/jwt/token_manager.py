from datetime import (
    datetime,
    timedelta
)

from jose import (
    jwt
)

from app.settings import (
    settings
)


class TokenManager:

    SECRET_KEY = (
        settings.JWT_SECRET_KEY
    )

    ALGORITHM = (
        "HS256"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = (
        60 * 24
    )

    @classmethod
    def create_access_token(

        cls,

        data: dict

    ):

        payload = data.copy()

        expire = (

            datetime.utcnow()

            + timedelta(

                minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        )

        payload.update(

            {
                "exp": expire
            }

        )

        return jwt.encode(

            payload,

            cls.SECRET_KEY,

            algorithm=cls.ALGORITHM

        )

    @classmethod
    def verify_token(

        cls,

        token: str

    ):

        return jwt.decode(

            token,

            cls.SECRET_KEY,

            algorithms=[
                cls.ALGORITHM
            ]

        )