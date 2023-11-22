from database import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey

from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    bio_by_user = Column(String, nullable=True)

class Twit(Base):
    __tablename__ = "twits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String)
    created_at = Column(DateTime, default=func.now())

class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    being_followed_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    twit_id = Column(Integer, ForeignKey('twits.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
