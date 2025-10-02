from flask import render_template, request, redirect, url_for, flash
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from settings import Session
from flask import Blueprint


bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not validate_password(password):
            flash("Пароль повинен містити не менше 8 символів")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)  # type: ignore

        user = User(username=username, email=email, hash_password=hashed_password)
        with Session() as session:
            session.add(user)
            session.commit()

        flash("Registration successful")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


def validate_password(password):
    return len(password) >= 8


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.get_by_username(username=username)  # type: ignore
        if user and check_password_hash(user.hash_password, password):  # type: ignore

            login_user(user)
            flash("Login successful")

            return redirect(url_for("auth.register"))
        flash("Invalid username or password")

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful")
    return redirect(url_for("index"))
