from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import db, User

auth = Blueprint("auth", __name__)

# Register


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("fullname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists.")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# -------------------------
# Login
# -------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        login = request.form.get("login")
        password = request.form.get("password")

        user = User.query.filter(
            (User.email == login) | (User.username == login)).first()

        if user and check_password_hash(user.password, password):
            if user.is_banned:
                return render_template(
                    "login.html",
                    error="Your account has been banned. Please contact an administrator."
                )
            if user.is_suspended:
                return render_template(
                    "login.html",
                    error="Your account has been suspended. Please contact an administrator."
                )

            login_user(user)

            flash("Login successful.")

            return redirect(url_for("home"))

        flash("Invalid email or password.")

    return render_template("login.html")


# -------------------------
# Logout
# -------------------------
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.")

    return redirect(url_for("auth.profile"))


# Profile
@auth.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html",
        user=current_user
    )


@auth.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    if request.method == "POST":

        current_user.full_name = request.form.get("fullname")
        current_user.username = request.form.get("username")
        current_user.email = request.form.get("email")
        current_user.bio = request.form.get("bio")

        db.session.commit()

        flash("Profile updated successfully.")

        return redirect(url_for("auth.profile"))

    return render_template("edit_profile.html", user=current_user)
