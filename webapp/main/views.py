import bcrypt
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
import os
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.main.forms import AccountForm, LoginForm, RegistrationForm
from webapp.models import User
from webapp import db
from time import sleep

main = Blueprint(
    "main",
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)

@main.route("/logout")
def logout():
    if '_flashes' in session:
        session['_flashes'].clear()
    logout_user()
    flash("Je bent uitgelogd", "success")
    return redirect(url_for("main.home"))


@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Dit e-mailadres is al geregistreerd. Probeer een ander e-mailadres.", "danger")
            return redirect(url_for("main.register"))
        else:
            hashed_password = generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Je account is aangemaakt! Je kunt nu inloggen.", "success")
            return redirect(url_for("main.login"))
    return render_template("register.html", title="Registreren", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.naam.data
        password = form.wachtwoord.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login succesvol!", "success")        
            return redirect(url_for("main.home"))
        else:
            flash("Onjuiste gebruikersnaam of wachtwoord. Probeer het opnieuw.", "danger")
            return redirect(url_for("main.login"))  
    return render_template("login.html", form=form)

@main.route("/account", methods=["GET", "POST"])
@login_required
def account():
    Succesvol = False  
    form = AccountForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash("Het nieuwe wachtwoord en de bevestiging komen niet overeen. Probeer het opnieuw.", "danger")
            return render_template("account.html", form=form, Succesvol=Succesvol)
        
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)
            flash("Wachtwoord succesvol gewijzigd!", "success")
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Accountgegevens succesvol bijgewerkt!", "success")
        Succesvol = True  
        session['Succesvol'] = True 
        return redirect(url_for("main.home"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", form=form, Succesvol=Succesvol) 




@main.route("/")
def home():
    Succesvol = session.pop('Succesvol', False) 
    return render_template("home.html", Succesvol=Succesvol)

@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/bungalows")
def bungalows():
    return render_template("bungalows.html")

