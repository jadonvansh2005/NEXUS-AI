from fastapi import (

    Depends,
    HTTPException,
    status

)

from fastapi.security import (

    OAuth2PasswordBearer

)

from jose import (

    JWTError

)

from database.connection import (
    SessionLocal
)

from models.user import (
    User
)

from auth.jwt.token_manager import (
    TokenManager
)


oauth2_scheme = (

    OAuth2PasswordBearer(

        tokenUrl="/auth/login"
    )

)


def get_current_user(

    token: str = Depends(
        oauth2_scheme
    )

):

    try:

        payload = (

            TokenManager.verify_token(
                token
            )

        )

        user_id = (
            payload.get(
                "user_id"
            )
        )

    except JWTError:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid Token"

        )

    db = SessionLocal()

    try:

        user = (

            db.query(User)

            .filter(
                User.id == user_id
            )

            .first()

        )

        if not user:

            raise HTTPException(

                status_code=status.HTTP_401_UNAUTHORIZED,

                detail="User Not Found"

            )

        return user

    finally:

        db.close()