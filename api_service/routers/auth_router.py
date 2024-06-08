from pydantic import BaseModel
from database_manager import DatabaseManager
from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from schemas import UserSchema
from database_manager import DatabaseManager
from uuid import uuid4
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from schemas import *

router = APIRouter(prefix="/auth")


@router.post('/signup', summary="Create new user", response_model=UserSchema)
async def create_user(data: UserSchema):
    db = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")

    user = db.get_user_by_email(data.email)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
    }

    db.create_user(email=data.email, 
                   password=get_hashed_password(data.password))
    return user


@router.post('/login', summary="Create access and refresh tokens for user", response_model=UserSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    user = db.get_user_by_email(form_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }
