"""
Auth utils copied over from https://github.com/IMS-IIITH/backend/blob/master/utils/auth_utils.py,
courtesy of https://github.com/bhavberi
"""

from fastapi import HTTPException, Cookie
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pytz import timezone
from os import getenv

from utils.ldap_utils import get_user_by_email

# JWT Authentication
SECRET_KEY = (
        getenv("JWT_SECRET_KEY", "this_is_my_very_secretive_secret") + "__RMS__"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = int(getenv("ACCESS_TOKEN_EXPIRE_DAYS", 5))


# Create Access Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone("UTC")) + expires_delta
    else:
        expire = datetime.now(timezone("UTC")) + timedelta(
            days=ACCESS_TOKEN_EXPIRE_DAYS
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependency for User Authentication
async def get_current_user(access_token_RMS: str = Cookie(None)):
    if access_token_RMS is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    try:
        payload = jwt.decode(access_token_RMS, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        email = payload.get("email")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        user = get_user_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        email = user["mail"][0].decode()
        username = user["uid"][0].decode()
        name = user["cn"][0].decode()

        return {"username": username, "email": email, "name": name}
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


# Function to check the current user is logged in or not
async def check_current_user(access_token_RMS: str = Cookie(None)):
    if access_token_RMS is None:
        return None
    try:
        payload = jwt.decode(access_token_RMS, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            return None
        user = get_user_by_email(email)
        if user is None:
            return None
        return access_token_RMS
    except JWTError:
        return None
