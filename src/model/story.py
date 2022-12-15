from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from src import db


class Story(db.Model):
    __tablename__ = "story"
    id: int = db.Column(Integer, primary_key=True)
    name: str = db.Column(String(128))
    text: str = db.Column(String(2048))
    created_at: datetime = db.Column(DateTime, default=datetime.utcnow)

    def __int__(self, name, text):
        self.name = name
        self.text = text
        self.created_at = datetime.now()
