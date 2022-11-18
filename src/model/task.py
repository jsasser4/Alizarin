from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from src import db
from .user import User
from .sprint import Sprint


class Task(db.Model):
    id: int = db.Column(Integer, primary_key=True)
    name: str = db.Column(String(100))
    description: str = db.Column(String(512))

    assigned_user_id: int = db.Column(Integer, ForeignKey("user.id"), nullable=True)
    assigned_user: Optional[User] = db.relationship("user", foreign_keys=[assigned_user_id])

    sprint_id: int = db.Column(Integer, ForeignKey("sprint.id"))
    sprint: Sprint = db.relationship("sprint", back_populates="tasks")

    is_completed: bool = db.Column(Boolean())
    created_at: datetime = db.Column(DateTime())

    __tablename__ = "task"

    def __init__(self, name, description, sprint):
        self.name = name
        self.description = description
        self.sprint = sprint
        self.assigned_user = None
        self.is_completed = False
        self.created_at = datetime.now()
