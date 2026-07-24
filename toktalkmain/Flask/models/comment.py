from datetime import datetime
from models import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship("User", backref="comments")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "author_id": self.author_id,
            "author": self.author.username,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
