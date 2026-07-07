from sqlalchemy.orm import Session
import random
from datetime import datetime, timedelta

from models.user import User

from auth.jwt.password_handler import (
    hash_password,
    verify_password
)

from auth.jwt.jwt_handler import (
    create_access_token
)

from auth.jwt.email_utils import send_verification_email


class AuthService:

    def signup(
        self,
        db: Session,
        name: str,
        email: str,
        password: str
    ):
        existing_user = db.query(
            User
        ).filter(
            User.email == email
        ).first()

        if existing_user:
            raise Exception(
                "Email already exists"
            )

        # Generate a random 6-digit OTP
        otp = str(random.randint(100000, 999999))
        otp_expiry = datetime.utcnow() + timedelta(minutes=10)

        user = User(
            name=name,
            email=email,
            password_hash=hash_password(
                password
            ),
            is_verified=False,
            verification_otp=otp,
            otp_expiry=otp_expiry
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # Send the verification email containing the OTP
        send_verification_email(email, otp)

        return user

    def login(
        self,
        db: Session,
        email: str,
        password: str
    ):
        user = db.query(
            User
        ).filter(
            User.email == email
        ).first()

        if not user:
            raise Exception(
                "Invalid Credentials"
            )

        if not verify_password(
            password,
            user.password_hash
        ):
            raise Exception(
                "Invalid Credentials"
            )

        # Enforce email verification check
        if not user.is_verified:
            # Generate a fresh OTP in case they need to verify
            otp = str(random.randint(100000, 999999))
            user.verification_otp = otp
            user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
            db.commit()

            # Trigger email send
            send_verification_email(user.email, otp)
            raise Exception(
                "Please verify your email first before logging in. A new verification code has been sent to your email."
            )

        token = create_access_token(
            {
                "user_id": user.id,
                "email": user.email
            }
        )

        return token