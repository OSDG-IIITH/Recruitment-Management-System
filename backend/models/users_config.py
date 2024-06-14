"""
Some users functionality copied over from
https://github.com/IMS-IIITH/backend/blob/master/routers/users_router.py,
courtesy of https://github.com/bhavberi
"""

from fastapi import APIRouter, HTTPException, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from utils.ldap_utils import authenticate_user
from utils.auth_utils import create_access_token, check_current_user, get_current_user


async def user_login(response: Response, username, password):
    auth_success, user_data = authenticate_user(username, password)
    if not auth_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
            headers={"set-cookie": ""},
        )

    email = user_data["mail"][0].decode()
    username = user_data["uid"][0].decode()

    # Create Access Token and Set Cookie
    new_access_token = create_access_token(data={"username": username, "email": email})
    response.set_cookie(
        key="access_token_RMS", value=new_access_token, httponly=True
    )

    return {"message": "Logged In Successfully"}


async def user_logout(response: Response, current_user):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not Logged In!")
    response.delete_cookie("access_token_RMS")
    return {"message": "Logged Out Successfully"}


async def user_extend_cookie(response, username, email):
    # Extend the access token/expiry time
    new_access_token = create_access_token(
        data={"username": username, "email": email}
    )
    response.set_cookie(
        key="access_token_RMS", value=new_access_token, httponly=True
    )
    return {"message": "Cookie Extended Successfully"}
