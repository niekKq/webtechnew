import bcrypt
from flask import Blueprint, flash, redirect, render_template, url_for
import os
from flask_login import current_user, login_required, login_user, logout_user

from webapp.main.forms import LoginForm, RegistrationForm, InfoForm

from werkzeug.security import generate_password_hash, check_password_hash
from webapp.models import User
from webapp import db

main = Blueprint(
    "main",
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)


@main.route("/")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("main.login"))
    return render_template("home.html")


@main.route("/about")
def about():
    if not current_user.is_authenticated:
        return redirect(url_for("main.login"))
    return render_template("about.html")


@main.route("/bungalows")
def bungalows():
    if not current_user.is_authenticated:
        return redirect(url_for("main.login"))
    return render_template("bungalows.html")


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Formulier gevalideerd")

        # Controleren of de gebruiker al bestaat
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash(
                "Dit e-mailadres is al geregistreerd. Probeer een ander e-mailadres.",
                "danger",
            )
            print("Gebruiker bestaat al")
            return redirect(url_for("main.register"))
        else:
            print("Nieuwe gebruiker wordt aangemaakt")
            # Wachtwoord niet hashen
            # hashed_password = generate_password_hash(form.password.data)
            print("Wachtwoord niet gehasht")
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            db.session.add(user)
            db.session.commit()
            print("Gebruiker toegevoegd aan database")
            flash("Je account is aangemaakt! Je kunt nu inloggen.", "success")
            return redirect(url_for("main.login"))
    return render_template("register.html", title="Registreren", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Formulier is correct gevalideerd")
        username = form.naam.data
        password = form.wachtwoord.data

        # Zoek de gebruiker in de database op basis van de gebruikersnaam
        user = User.query.filter_by(username=username).first()

        # Controleer of de gebruiker bestaat
        if user:
            print("Gebruiker gevonden:", user)

            # Controleer of het ingevoerde wachtwoord overeenkomt met het opgeslagen wachtwoord
            if user.password == password:
                print("Wachtwoord correct")

                # Log de gebruiker in
                login_user(user)
                flash("Login succesvol!", "success")
                return redirect(url_for("main.home"))
            else:
                print("Onjuist wachtwoord")
                flash("Onjuiste wachtwoord. Probeer het opnieuw.", "danger")
        else:
            print("Gebruiker niet gevonden")
            flash("Gebruiker niet gevonden. Probeer het opnieuw.", "danger")

    return render_template("login.html", form=form)
