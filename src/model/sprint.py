from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from src import db
from .project import Project


class Sprint(db.Model):
    id: int = db.Column(Integer, primary_key=True)
    name: str = db.Column(String(255))
    project_id: int = db.Column(Integer, ForeignKey("project.id"))
    project: Project = db.relationship("user", foreign_keys=[project_id])
    tasks: [] = db.relationship("tasks", back_populates="parent")
    created_at: datetime = db.Column(DateTime())

    __tablename__ = "sprint.html"

    def __int__(self, name: str, project: Project):
        self.name = name
        self.project = project
        self.tasks = []
        self.created_at = datetime.now()
