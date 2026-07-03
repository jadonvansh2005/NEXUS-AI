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
        tokenUrl="/auth/login",
        auto_error=False
    )
)


def get_current_user(
    token: str | None = Depends(
        oauth2_scheme
    )
):
    if not token:
        # Local development bypass: return the first user in the database
        db = SessionLocal()
        try:
            user = db.query(User).first()
            if user:
                return user
            # Fallback mock if database has no users yet
            class MockUser:
                id = 1
                name = "Developer"
                email = "developer@example.com"
            return MockUser()
        finally:
            db.close()

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