from pydantic import (
    BaseModel,
    EmailStr
)

class SignupRequest(

    BaseModel

):

    name: str

    email: EmailStr

    password: str


class LoginRequest(

    BaseModel

):

    email: EmailStr

    password: str


class TokenResponse(

    BaseModel

):

    access_token: str

    token_type: str


class VerifyEmailRequest(

    BaseModel

):

    email: EmailStr

    otp: str


class GoogleLoginRequest(

    BaseModel

):

    token: str