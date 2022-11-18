from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DateTime
from src import db
from .user import User

bridge_table = db.Table(
    "project_users",
    db.metadata,
    db.Column("project_id", ForeignKey("project.id")),
    db.Column("user_id", ForeignKey("user.id")),
)


class Project(db.Model):
    id: int = db.Column(Integer, primary_key=True)
    name: str = db.Column(String(128))
    created_by_id: int = db.Column(Integer, ForeignKey("user.id"))
    created_by: User = db.relationship(User, foreign_keys=[created_by_id])

    members = db.relationship(User, secondary=bridge_table)
    created_at: datetime = db.Column("created_at", DateTime())

    __tablename__: str = "project"

    def __int__(self, name: str, created_by: User):
        self.name = name
        self.created_by = created_by
        self.created_at = datetime.now()
