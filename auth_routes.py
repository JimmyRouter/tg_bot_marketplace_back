from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

from constants import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, OAUTH2_SCHEME, ROLE_EXEPTION
from db_manager import users_cll
from db_manager.models import Token, TGUser, Staff, TokenData
from db_manager.manager import delete_instance
from fastapi_server.auth import authenticate_user, create_access_token, get_current_active_user, PermissionsChecker

auth_router = APIRouter()


@auth_router.post('/auth/login/')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(users_cll, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post('auth/refresh/')
async def refresh_token(
        token: Annotated[str, Depends(OAUTH2_SCHEME)]) -> Token:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": token_data.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    except JWTError:
        raise credentials_exception


@auth_router.delete('auth/{shop_id}/')
async def delete_shop(
        current_user: Annotated[Staff, Depends(PermissionsChecker(('Shop', 'd')))],
        shop_id,
):
    if current_user:
        await delete_instance('shop',
                              shop_id=shop_id
        )
    else:
        raise ROLE_EXEPTION


@auth_router.get("/users/me/", response_model=TGUser)
async def read_users_me(
    current_user: Annotated[TGUser, Depends(get_current_active_user)],
):
    return current_user

