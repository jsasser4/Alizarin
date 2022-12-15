from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from src import db
from .project import Project


class Sprint(db.Model):
    sprint_id: int = db.Column(Integer, primary_key=True)
    name: str = db.Column(String(256))
    created_at: datetime = db.Column(DateTime())

    __tablename__ = "sprints"

    def __int__(self, name: str, project: Project):
        self.name = name
        self.created_at = datetime.now()
