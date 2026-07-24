from flask import Flask
from flask_login import LoginManager
from models.user import db, User
from routes.auth import auth

login_manager = LoginManager()


def create_app():

    app = Flask(_name_)

    app.config["SECRET_KEY"] = "your_secret_key"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///toktalk.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    app.register_blueprint(auth)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app
