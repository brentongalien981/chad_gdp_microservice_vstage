from app import db
from sqlalchemy import String, Integer
from dataclasses import dataclass

@dataclass
class User(db.Model):
    id: int
    name: str
    email: str

    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
