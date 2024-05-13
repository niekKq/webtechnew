from flask import Blueprint, render_template
import os

main = Blueprint('main', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@main.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/bungalows")
def bungalows():
    return render_template("bungalows.html")