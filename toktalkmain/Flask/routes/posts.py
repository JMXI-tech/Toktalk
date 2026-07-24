from flask_login import current_user, login_required
from flask import Blueprint, request, render_template, redirect, url_for, abort

from models.user import db
from models.post import Post
from models.comment import Comment
from models.like import Like


posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


# CREATE POST
@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            return render_template(
                'create_post.html',
                error='Title and content are required.'
            )

        post = Post(
            title=title,
            content=content,
            author_id=current_user.id
        )

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts.get_post', post_id=post.id))

    return render_template('create_post.html')


# VIEW ALL POSTS
@posts_bp.route('', methods=['GET'])
def get_posts():
    return redirect(url_for('home'))


# VIEW SINGLE POST + COMMENTS
@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template(
        'post.html',
        post=post
    )


# EDIT POST
@posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            return render_template(
                'edit_post.html',
                post=post,
                error='Title and content are required.'
            )

        post.title = title
        post.content = content

        db.session.commit()

        return redirect(
            url_for('posts.get_post', post_id=post.id)
        )

    return render_template(
        'edit_post.html',
        post=post
    )


# DELETE POST
@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author_id != current_user.id:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('home'))


# CREATE COMMENT
@posts_bp.route('/<int:post_id>/comments', methods=['POST'])
@login_required
def create_comment(post_id):
    Post.query.get_or_404(post_id)

    content = request.form.get('content', '').strip()

    if not content:
        return redirect(
            url_for('posts.get_post', post_id=post_id)
        )

    comment = Comment(
        content=content,
        author_id=current_user.id,
        post_id=post_id
    )

    db.session.add(comment)
    db.session.commit()

    return redirect(
        url_for('posts.get_post', post_id=post_id)
    )

# DELETE COMMENT


@posts_bp.route('/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Only the person who created the comment can delete it
    if comment.author_id != current_user.id:
        abort(403)

    post_id = comment.post_id

    db.session.delete(comment)
    db.session.commit()

    return redirect(
        url_for('posts.get_post', post_id=post_id)
    )


# LIKE / UNLIKE POST
@posts_bp.route('/<int:post_id>/like', methods=['POST'])
@login_required
def toggle_like(post_id):
    Post.query.get_or_404(post_id)

    like = Like.query.filter_by(
        user_id=current_user.id,
        post_id=post_id
    ).first()

    if like:
        db.session.delete(like)
    else:
        new_like = Like(
            user_id=current_user.id,
            post_id=post_id
        )
        db.session.add(new_like)

    db.session.commit()

    return redirect(
        url_for('posts.get_post', post_id=post_id)
    )
