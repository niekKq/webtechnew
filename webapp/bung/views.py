import bcrypt
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
import os
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.main.forms import AccountForm, LoginForm, RegistrationForm, BungalowForm
from webapp.models import User, Bungalow
from webapp import db
from time import sleep



bung = Blueprint(
    "bung",
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)


@bung.route("/admin/add_bungalow", methods=["GET", "POST"])
def add_bungalow():
    form = BungalowForm()
    if form.validate_on_submit():
        bungalow = Bungalow(name=form.name.data, content=form.content.data, bungalow_type=form.bungalow_type.data, weekprice=form.weekprice.data)
        db.session.add(bungalow)
        db.session.commit()
        flash("Bungalow succesvol toegevoegd!", "success")
        return redirect(url_for("bung.admin"))
    return render_template("add_bungalow.html", form=form)

@bung.route("/admin/edit_bungalow", methods=["GET", "POST"])
def edit_view():
    bungalows = Bungalow.query.all()
    print("Bungalows gevonden:", bungalows)
    return render_template("edit_bungalow.html", bungalows=bungalows)

@bung.route("/admin/edit/<int:bungalow_id>", methods=["GET", "POST"])
def edit_bungalow(bungalow_id):
    bungalow = Bungalow.query.get_or_404(bungalow_id)
    form = BungalowForm(obj=bungalow)
    if form.validate_on_submit():
        form.populate_obj(bungalow)  # Vul het bungalow object met de gegevens uit het formulier
        db.session.commit()  # Bevestig de wijzigingen aan de database
        flash("Bungalow succesvol bijgewerkt!", "success")
        return redirect(url_for("bung.admin"))  # Stuur de gebruiker terug naar de admin pagina
    return render_template("edit.html", form=form)

@bung.route("/admin/delete/<int:bungalow_id>", methods=["GET", "POST"])
def delete_bungalow(bungalow_id):
    bungalow = Bungalow.query.get_or_404(bungalow_id)
    db.session.delete(bungalow)
    db.session.commit()
    flash("Bungalow succesvol verwijderd!", "success")
    return redirect(url_for("main.admin"))