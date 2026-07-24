from flask import Blueprint, render_template, request
from sqlalchemy import or_

from models.post import Post

# Blueprint keeps search feature away from the rest of the application
search_bp = Blueprint("search", __name__)


@search_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip()

    results = []

    if query:
        results = Post.query.filter(
            or_(
                Post.title.ilike(f"%{query}%"),
                Post.content.ilike(f"%{query}%")
            )
        ).order_by(Post.created_at.desc()).all()

    return render_template(
        "search.html",
        query=query,
        results=results
    )
