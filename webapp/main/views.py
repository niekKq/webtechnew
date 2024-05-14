from flask import Blueprint, flash, redirect, render_template, url_for
import os
from flask_login import login_user
from webapp.main.forms import InfoForm
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint(
    "main",
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)


@main.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/bungalows")
def bungalows():
    return render_template("bungalows.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")
