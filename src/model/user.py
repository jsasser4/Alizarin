from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from src import db


class User(db.Model):
    id: int = db.Column(Integer, primary_key=True)
    name: str = db.Column(String(100))
    email: str = db.Column(String(100))
    password_hash: str = db.Column(String(256))
    created_at: datetime = db.Column(DateTime())

    __tablename__ = "user"

    def __int__(self, name, email, password_hash):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now()
