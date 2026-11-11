
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utcnow,
        nullable=False
    )

    # Tasks created by this user
    tasks = db.relationship(
        "Task",
        foreign_keys="Task.user_id",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # Comments written by this user
    comments = db.relationship(
        "Comment",
        foreign_keys="Comment.user_id",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    # Tasks assigned to this user
    assigned_tasks = db.relationship(
        "Task",
        foreign_keys="Task.assigned_to_id",
        back_populates="assignee"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="", nullable=False)
    status = db.Column(db.String(20), default="pending", nullable=False, index=True)
    priority = db.Column(db.String(10), default="medium", nullable=False, index=True)
    category = db.Column(db.String(60), default="", nullable=False, index=True)
    due_date = db.Column(db.Date, nullable=True, index=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utcnow,
        nullable=False,
        index=True
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    assigned_to_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    # Task owner relationship
    owner = db.relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="tasks"
    )

    # Assigned user relationship
    assignee = db.relationship(
        "User",
        foreign_keys=[assigned_to_id],
        back_populates="assigned_tasks"
    )

    comments = db.relationship(
        "Comment",
        back_populates="task",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "category": self.category,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "user_id": self.user_id,
            "assigned_to_id": self.assigned_to_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000), nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utcnow,
        nullable=False
    )

    task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    task = db.relationship(
        "Task",
        back_populates="comments"
    )

    author = db.relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="comments"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "body": self.body,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat()
        }
