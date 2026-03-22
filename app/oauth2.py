from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from .config import settings

from sqlalchemy.orm import Session

from . import schema, models
from .database import get_db

SECRET = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    token = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return token

def verify_access_token(token:str, credentials_exception:HTTPException):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        uid: int = payload.get("user_id")
        if not uid:
            raise credentials_exception
        token_data = schema.TokenData(id=uid)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials")

    user_id = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    return user
