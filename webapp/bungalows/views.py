from flask import render_template, session, url_for, flash, redirect, Blueprint, request
from flask_login import login_required, current_user
from webapp import db
from webapp.bungalows.forms import BungalowForm
from webapp.models import Bungalow
import os
import random

bung = Blueprint("bung", __name__, template_folder="templates")


def get_random_image():
    img_folder = os.path.join("webapp", "static", "img")
    images = [f for f in os.listdir(img_folder) if f.startswith("bungalow")]
    if images:
        selected_image = random.choice(images)
        print("Geselecteerde afbeelding:", selected_image)
        return selected_image
    else:
        print("Geen afbeeldingen gevonden in de map:", img_folder)
        return None


@bung.route("/admin", methods=["GET", "POST"])
def admin():
    if "_flashes" in session:
        session["_flashes"].clear()
    return render_template("admin.html")


@bung.route("/bungalows")
def bungalows():
    bungalows = Bungalow.query.all()
    print("Bungalows gevonden:", bungalows)
    return render_template("bungalows.html", bungalows=bungalows)


@bung.route("/admin/add_bungalow", methods=["GET", "POST"])
def add_bungalow():
    form = BungalowForm()
    if form.validate_on_submit():
        image_file = get_random_image()
        bungalow = Bungalow(
            name=form.name.data,
            content=form.content.data,
            bungalow_type=form.bungalow_type.data,
            weekprice=form.weekprice.data,
            image_file=image_file,
        )
        db.session.add(bungalow)
        db.session.commit()
        flash("Bungalow succesvol toegevoegd!", "success")
        return redirect(url_for("bung.bungalows"))
    return render_template("add_bungalow.html", form=form)


@bung.route("/admin/edit_bungalow", methods=["GET", "POST"])
def edit_view():
    bungalows = Bungalow.query.all()
    return render_template("edit_bungalow.html", bungalows=bungalows)


@bung.route("/admin/edit/<int:bungalow_id>", methods=["GET", "POST"])
def edit_bungalow(bungalow_id):
    bungalow = Bungalow.query.get_or_404(bungalow_id)
    form = BungalowForm(obj=bungalow)
    if form.validate_on_submit():
        form.populate_obj(bungalow)
        db.session.commit()
        flash("Bungalow succesvol bijgewerkt!", "success")
        return redirect(url_for("bung.admin"))
    return render_template("edit.html", form=form)


@bung.route("/admin/delete/<int:bungalow_id>", methods=["GET", "POST"])
def delete_bungalow(bungalow_id):
    bungalow = Bungalow.query.get_or_404(bungalow_id)
    db.session.delete(bungalow)
    db.session.commit()
    flash("Bungalow succesvol verwijderd!", "success")
    return redirect(url_for("bung.admin"))
