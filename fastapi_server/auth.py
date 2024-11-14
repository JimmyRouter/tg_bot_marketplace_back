from datetime import datetime, timedelta, timezone
from typing import Annotated, Tuple
from fastapi import Depends, FastAPI, HTTPException, status
import motor.motor_asyncio
from passlib.context import CryptContext
from jose import JWTError, jwt

from constants import SECRET_KEY, ALGORITHM, OAUTH2_SCHEME, CREDENTIALS_EXEPTION, ROLE_EXEPTION
from db_manager.connector import users_cll
from db_manager.models import StaffInDb, TokenData, TGUser, Staff, Role

# ======================================================================================================= #


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def user_exist(users_collection: motor.motor_asyncio.AsyncIOMotorCollection,
               username: str):  # SECURITY BREACH :username:  check tg id, db id
    user = users_collection.find_one({'username': username})
    if user:
        return StaffInDb(**user)
    else:
        return False


def authenticate_user(users_collection, username: str, password: str):
    user = user_exist(users_collection, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_pwd):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# get curent user from front token
async def get_current_user(token: Annotated[str, Depends(OAUTH2_SCHEME)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if not username:
            raise CREDENTIALS_EXEPTION
        user = user_exist(users_cll, username=username)
        if not user:
            raise CREDENTIALS_EXEPTION
        return user
    except JWTError:
        raise CREDENTIALS_EXEPTION


async def get_current_active_user(
        current_user: Annotated[Staff, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class PermissionsChecker:
    def __init__(self, model_crud: Tuple[str, str]):
        self.model_name = model_crud[0]
        self.model_operation = model_crud[1]

    def __call__(self, user: Staff):
        if user:
            permissions = user.role['permissions']
            for permission in permissions:
                if self.model_name == permission[0] and self.model_operation in permission[1]:
                    return user
                raise ROLE_EXEPTION
            raise ROLE_EXEPTION
        raise ROLE_EXEPTION


async def user_is_manager(
        current_user: Annotated[Staff, Depends(get_current_active_user)],
):
    if current_user.role == Role.MANAGER:
        return current_user
    else:
        raise ROLE_EXEPTION


async def user_is_admin(
        current_user: Annotated[Staff, Depends(user_is_manager)],
):
    if current_user.role == Role.ADMIN:
        return current_user
    else:
        raise ROLE_EXEPTION


async def user_is_super(
        current_user: Annotated[Staff, Depends(user_is_admin)],
):
    if current_user.role == Role.SUPERUSER:
        return current_user
    else:
        raise ROLE_EXEPTION
