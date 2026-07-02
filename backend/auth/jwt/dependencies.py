from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from auth.jwt.jwt_handler import (
    decode_access_token
)

oauth2_scheme = OAuth2PasswordBearer(

    tokenUrl="/auth/token"

)


def get_current_user(

    token: str = Depends(
        oauth2_scheme
    )

):

    payload = decode_access_token(
        token
    )

    if not payload:

        raise HTTPException(

            status_code=401,

            detail="Invalid Token"

        )

    return payload