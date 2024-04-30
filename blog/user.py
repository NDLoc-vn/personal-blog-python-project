from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_user, login_required, logout_user
from .models import User

from . import db

user = Blueprint("user", __name__)

@user.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user:
            if password == user.password:
                session.permanent = True
                login_user(user, remember=True)
                return redirect(url_for("views.admin"))
    return redirect(url_for("views.guest"))

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.guest"))