from fastapi import Depends, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models.user import User
from database import get_db
from authentication import get_password_hash
from routers import router


class CreateUser(BaseModel):
    username: str
    password: str


@router.post("/user")
def create_user(
    user_data: CreateUser,
    db: Session = Depends(get_db),
):
    # Create an ECG instance and associate it with the user
    user = User(username=user_data.username, password=get_password_hash(user_data.password))
    db.add(user)
    db.commit()
    
    return Response(status_code=200)
