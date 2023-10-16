from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from . import Base


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    @staticmethod
    def get_user(username: str, db: Session):
        return db.query(User).filter(User.username == username).first()
