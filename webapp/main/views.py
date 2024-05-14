import bcrypt
from flask import Blueprint, flash, redirect, render_template, url_for
import os
from flask_login import current_user, login_required

from webapp.main.forms import InfoForm, RegistrationForm

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
    return render_template("home.html")


@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/bungalows")
def bungalows():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    return render_template("bungalows.html")


@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = InfoForm()
    if form.validate_on_submit():
        # Haal gebruikersinformatie op uit het formulier
        username = form.naam.data
        password = form.wachtwoord.data

        # Zoek de gebruiker in de database
        user = User.query.filter_by(username=username).first()

        # Controleer of de gebruiker bestaat en of het wachtwoord overeenkomt
        if user and user.check_password(password):
            # Log de gebruiker in
            flash('Login succesvol!', 'success')
            # Hier kun je bijvoorbeeld de gebruiker inloggen met Flask-Login
            # login_user(user)
            return redirect(url_for('main.home'))
        else:
            # Geef een foutmelding weer als de inloggegevens onjuist zijn
            flash('Onjuiste gebruikersnaam of wachtwoord. Probeer het opnieuw.', 'danger')

    # Laad de login-pagina
    return render_template("login.html", form=form)
