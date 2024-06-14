"""
Some users functionality copied over from
https://github.com/IMS-IIITH/backend/blob/master/routers/users_router.py,
courtesy of https://github.com/bhavberi
"""

from fastapi import APIRouter, HTTPException, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from utils.auth_utils import create_access_token, check_current_user, get_current_user

from models.users_config import user_login, user_logout, user_extend_cookie

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# User Login Endpoint
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
        request: Request,
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        access_token_RMS: str | None = Depends(check_current_user),
):
    if access_token_RMS is not None:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="Already Logged In!",
        )

    return await user_login(response, form_data.username, form_data.password)


# User Logout
@router.post("/logout", status_code=status.HTTP_202_ACCEPTED)
async def logout(
        response: Response, current_user: str | None = Depends(check_current_user)
):
    return await user_logout(response, current_user)


@router.post("/extend_cookie", status_code=status.HTTP_200_OK)
async def extend_cookie(
        request: Request,
        response: Response,
        user_data=Depends(get_current_user),
):
    username, email = user_data["username"], user_data["email"]
    return await user_extend_cookie(response, username, email)
