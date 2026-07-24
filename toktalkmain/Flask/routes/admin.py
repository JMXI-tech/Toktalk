from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required, current_user

from models.user import db, User
from models.post import Post
from models.comment import Comment
from models.like import Like

# creates admin blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@login_required
def dashboard():  # loads admin dashboard

    if not current_user.is_admin:
        abort(403)

    stats = {
        "users": User.query.count(),
        "posts": Post.query.count(),
        "comments": Comment.query.count(),
        "likes": Like.query.count(),
    }

    return render_template(
        "admin/dashboard.html",
        stats=stats
    )


@admin_bp.route("/users")
@login_required
def users():

    if not current_user.is_admin:
        abort(403)

    users = User.query.order_by(User.created_at.desc()).all()

    return render_template(
        "admin/users.html",
        users=users
    )


@admin_bp.route("/posts")
@login_required
def posts():

    if not current_user.is_admin:
        abort(403)

    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template(
        "admin/posts.html",
        posts=posts
    )


@admin_bp.route("/post/add", methods=["GET", "POST"])
@login_required
def add_post():
    if not current_user.is_admin:
        abort(403)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            return render_template(
                "admin/add_post.html",
                error="Title and content are required."
            )

        post = Post(
            title=title,
            content=content,
            author_id=current_user.id
        )

        db.session.add(post)
        db.session.commit()

        return redirect(url_for("admin.posts"))

    return render_template("admin/add_post.html")


@admin_bp.route("/post/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    if not current_user.is_admin:
        abort(403)

    post = Post.query.get_or_404(id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            return render_template(
                "admin/edit_post.html",
                post=post,
                error="Title and content are required."
            )

        post.title = title
        post.content = content

        db.session.commit()

        return redirect(url_for("admin.posts"))

    return render_template(
        "admin/edit_post.html",
        post=post
    )


@admin_bp.route("/post/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_post(id):
    if not current_user.is_admin:
        abort(403)

    post = Post.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for("admin.posts"))

    return render_template(
        "admin/delete_post.html",
        post=post
    )

# SUSPEND USER


@admin_bp.route("/user/suspend/<int:id>", methods=["POST"])
@login_required
def suspend_user(id):
    if not current_user.is_admin:
        abort(403)

    user = User.query.get_or_404(id)

    # Admin cannot suspend themselves
    if user.id == current_user.id:
        abort(403)

    user.is_suspended = True
    db.session.commit()

    return redirect(url_for("admin.users"))


# UNSUSPEND USER
@admin_bp.route("/user/unsuspend/<int:id>", methods=["POST"])
@login_required
def unsuspend_user(id):
    if not current_user.is_admin:
        abort(403)

    user = User.query.get_or_404(id)

    user.is_suspended = False
    db.session.commit()

    return redirect(url_for("admin.users"))


# BAN USER
@admin_bp.route("/user/ban/<int:id>", methods=["POST"])
@login_required
def ban_user(id):
    if not current_user.is_admin:
        abort(403)

    user = User.query.get_or_404(id)

    # Admin cannot ban themselves
    if user.id == current_user.id:
        abort(403)

    user.is_banned = True
    db.session.commit()

    return redirect(url_for("admin.users"))


# UNBAN USER
@admin_bp.route("/user/unban/<int:id>", methods=["POST"])
@login_required
def unban_user(id):
    if not current_user.is_admin:
        abort(403)

    user = User.query.get_or_404(id)

    user.is_banned = False
    db.session.commit()

    return redirect(url_for("admin.users"))
