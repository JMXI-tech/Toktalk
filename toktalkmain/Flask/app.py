from flask import Flask, render_template
from flask_login import LoginManager

from models import db
from models.user import User
import os

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "toktalk_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///toktalk.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)

    # Import models
    from models.post import Post
    from models.comment import Comment
    from models.like import Like

    # Import routes
    from routes.auth import auth
    from routes.posts import posts_bp
    from routes.search import search_bp
    from routes.admin import admin_bp

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(posts_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(admin_bp)

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Welcome route
    @app.route("/")
    def welcome():
        return render_template("toktalk_welcome.html")

    #Home route
    @app.route("/home")
    def home():
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template("home.html", posts=posts)

    # Error handlerss
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("error/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("error/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("error/500.html"), 500

    @app.route("/about")
    def about():
        return render_template("about.html")

        # Create database tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

