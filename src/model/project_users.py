from sqlalchemy import ForeignKey
from src import db

bridge_table = db.Table(
    "project_users",
    db.metadata,
    db.Column("project_id", ForeignKey("project.id"), primary_key=True),
    db.Column("user_id", ForeignKey("user.id"), primary_key=True)
)
