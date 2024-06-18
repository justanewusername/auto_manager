from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database_manager import DatabaseManager
from utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError
from schemas import TokenPayload, UserSchema, SystemUser

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def get_current_user_impl(token: str = Depends(reuseable_oauth)) -> SystemUser:
    print("hello i'm here!!!")
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError) as e:
        print(f"JWT validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    db = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    # token_data.sub is users email
    user = db.get_user_by_email(token_data.sub)
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return SystemUser(id=user['id'], email=user['email'])


def get_current_user(token: str) -> SystemUser:
    print("hello i'm here!!!")
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            return None
        
    except(jwt.JWTError, ValidationError):
        return None
    
    db = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    # token_data.sub is users email
    user = db.get_user_by_email(token_data.sub)
    
    
    if user is None:
        return None
    
    return SystemUser(**user)