from datetime import datetime, timedelta
from typing import Annotated
from jose import jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from database import get_db
from authentication import verify_password
from models.user import User
from routers import router


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = User.get_user(form_data.username, db)
    if user:
        if verify_password(form_data.password, user.password):
            data = {
                "sub": form_data.username,
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            }
            access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
