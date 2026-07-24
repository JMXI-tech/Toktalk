from flask_login import UserMixin
from datetime import datetime
from models import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(150), nullable=False)

    username = db.Column(db.String(80), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    bio = db.Column(db.Text, default="")

    profile_picture = db.Column(
        db.String(255),
        default="default_profile.png"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )

    is_suspended = db.Column(
        db.Boolean,
        default=False
    )

    is_banned = db.Column(
        db.Boolean,
        default=False
    )

    def __repr__(self):
        return f"<User {self.username}>"