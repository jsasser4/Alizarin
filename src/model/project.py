from datetime import datetime
from sqlalchemy import DateTime

from src import db
from .project_users import project_users

class Project(db.Model):
    __tablename__: str = "projects"
    project_id = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(128))
    users = db.relationship('User', secondary='project_users', back_populates='projects')
    created_at: datetime = db.Column(DateTime, default=datetime.utcnow)

    def __int__(self, name: str):
        self.name = name

    def __repr__(self):
        return str(self.name)