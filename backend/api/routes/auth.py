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
    LoginRequest,
    VerifyEmailRequest,
    GoogleLoginRequest
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


@router.post("/verify")
def verify_email(
    request: VerifyEmailRequest,
    db: Session = Depends(get_db)
):
    from models.user import User
    from datetime import datetime

    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if user.is_verified:
        return {"message": "Email is already verified"}

    if not user.verification_otp or not user.otp_expiry:
        raise HTTPException(status_code=400, detail="No active verification code found. Please attempt to login to generate a new code.")

    if datetime.utcnow() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="Verification code has expired. Please attempt to login to generate a new code.")

    if user.verification_otp != request.otp:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    # Success! Verify user
    user.is_verified = True
    user.verification_otp = None
    user.otp_expiry = None
    db.commit()

    return {"message": "Email verified successfully! You can now log in."}


@router.post("/google")
def google_login(
    request: GoogleLoginRequest,
    db: Session = Depends(get_db)
):
    import urllib.request
    import json
    from models.user import User
    from auth.jwt.jwt_handler import create_access_token
    from auth.jwt.password_handler import hash_password
    import uuid
    from app.settings import settings

    google_token = request.token
    # Call Google's tokeninfo API to verify the token
    tokeninfo_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={google_token}"
    try:
        req = urllib.request.Request(tokeninfo_url, method="GET")
        with urllib.request.urlopen(req, timeout=5.0) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to verify Google token: {e}")

    # Check client ID verification if configured
    google_client_id = settings.GOOGLE_CLIENT_ID
    if google_client_id and payload.get("aud") != google_client_id:
        raise HTTPException(status_code=400, detail="Google Client ID mismatch")

    email = payload.get("email")
    name = payload.get("name") or "Google User"

    if not email:
        raise HTTPException(status_code=400, detail="Invalid Google token payload (missing email)")

    # Find or create user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Create a new verified user for Google OAuth login
        user = User(
            name=name,
            email=email,
            password_hash=hash_password(str(uuid.uuid4())), # Random secure password
            is_verified=True, # Google accounts are pre-verified
            verification_otp=None,
            otp_expiry=None
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # If user exists but is not marked verified, mark them verified since Google verified them
        if not user.is_verified:
            user.is_verified = True
            user.verification_otp = None
            user.otp_expiry = None
            db.commit()
            db.refresh(user)

    # Generate access token
    token = create_access_token(
        {
            "user_id": user.id,
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }