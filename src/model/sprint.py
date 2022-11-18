from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from src import db


class Sprint(db.Model):
    id: int = db.Column(Integer, primary_key=True)
    name: str = db.Column(String(255))
    tasks: [object] = db.relationship("tasks", back_populates="parent")
    created_at: datetime = db.Column(DateTime())

    __tablename__ = "sprint"

    def __int__(self, name: str):
        self.name = name
        self.tasks = []
        self.created_at = datetime.now()