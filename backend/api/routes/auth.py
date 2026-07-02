from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.connection import (
    get_db
)

from auth.jwt.auth_service import (
    AuthService
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)



from schemas.auth import (
    SignupRequest,
    LoginRequest
)

router = APIRouter()

service = AuthService()


@router.post("/signup")
def signup(

    request: SignupRequest,

    db: Session = Depends(
        get_db
    )

):

    try:

        user = service.signup(

            db,

            request.name,

            request.email,

            request.password

        )

        return {

            "message":
                "User Created",

            "user_id":
                user.id

        }

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


@router.post("/login")
def login(

    request: LoginRequest,

    db: Session = Depends(
        get_db
    )

):

    try:

        token = service.login(

            db,

            request.email,

            request.password

        )

        return {

            "access_token":
                token,

            "token_type":
                "bearer"

        }

    except Exception as e:

        raise HTTPException(

            status_code=401,

            detail=str(e)

        )
    

@router.post("/token")
def token_login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(
        get_db
    )

):

    try:

        token = service.login(

            db,

            form_data.username,

            form_data.password

        )

        return {

            "access_token": token,

            "token_type": "bearer"

        }

    except Exception as e:

        raise HTTPException(

            status_code=401,

            detail=str(e)

        )