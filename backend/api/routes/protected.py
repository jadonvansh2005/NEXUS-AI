from fastapi import APIRouter
from fastapi import Depends

from auth.jwt.auth_dependency import (
    get_current_user
)

router = APIRouter()


@router.get("/me")
def me(

    current_user = Depends(
        get_current_user
    )

):

    return {

        "id":
            current_user.id,

        "name":
            current_user.name,

        "email":
            current_user.email

    }