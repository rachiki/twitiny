from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

# Models for FastAPI
class User(BaseModel):
    id: int
    username: str
    password: str
    email: str
    created_at: str
    bio_by_user: str = None

class Twit(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: str

class Follow(BaseModel):
    follower_id: int
    being_followed_id: int
    created_at: str

class Like(BaseModel):
    user_id: int
    twit_id: int
    created_at: str