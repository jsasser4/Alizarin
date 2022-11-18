from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from src import db


class User(db.Model):
    id: int = db.Column(Integer, primary_key=True)
    first_name: str = db.Column(String(128))
    last_name: str = db.Column(String(128))
    email: str = db.Column(String(128))
    password_hash: str = db.Column(String(256))
    created_at: datetime = db.Column(DateTime())

    __tablename__ = "user"

    def __int__(self, first_name, last_name, email, password_hash):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now()
