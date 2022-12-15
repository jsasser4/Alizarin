from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from src import db
from .sprint import Sprint
from .project import Project


class Task(db.Model):
    task_id: int = db.Column(Integer, primary_key=True)
    name: str = db.Column(String(128))
    description: str = db.Column(String(512))

    is_completed: bool = db.Column(Boolean())
    created_at: datetime = db.Column(DateTime())

    __tablename__ = "tasks"

    def __init__(self, name, description, project: Project, sprint: Sprint):
        self.name = name
        self.description = description
        self.is_completed = False
        self.created_at = datetime.now()
