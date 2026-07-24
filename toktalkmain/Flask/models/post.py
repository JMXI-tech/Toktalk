from datetime import datetime
from models import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    comments = db.relationship(
        'Comment', backref='post', cascade='all, delete-orphan', lazy=True)
    likes = db.relationship('Like', backref='post',
                            cascade='all, delete-orphan', lazy=True)
    author = db.relationship("User", backref="posts")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "author": self.author.username,
            "created_at": self.created_at.isoformat()
            if self.created_at else None,
            "updated_at": self.updated_at.isoformat()
            if self.updated_at else None,
            "comment_count": len(self.comments),
            "like_count": len(self.likes),
        }
