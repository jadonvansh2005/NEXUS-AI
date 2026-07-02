from sqlalchemy.orm import Session

from models.user import User

from auth.jwt.password_handler import (

    hash_password,
    verify_password

)

from auth.jwt.jwt_handler import (

    create_access_token

)


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

        user = User(

            name=name,

            email=email,

            password_hash=hash_password(
                password
            )

        )

        db.add(user)

        db.commit()

        db.refresh(user)

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

        token = create_access_token(

            {
                "user_id": user.id,
                "email": user.email
            }

        )

        return token