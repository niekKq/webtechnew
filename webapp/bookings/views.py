from flask import Blueprint, render_template, request, flash, redirect, url_for
from webapp.models import Bungalow, Booking, BungalowAvailability
from webapp import db
from webapp.bookings.forms import BookingForm, UpdateBookingForm
from flask_login import current_user, login_required

bookings = Blueprint("bookings", __name__, template_folder="templates")


@bookings.route("/my_bookings")
@login_required
def my_bookings():
    user_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template("my_bookings.html", bookings=user_bookings)


@bookings.route("/update_booking/<int:booking_id>", methods=["GET", "POST"])
@login_required
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    form = UpdateBookingForm()
    availability = BungalowAvailability.query.filter_by(
        bungalow_id=booking.bungalow_id
    ).first()
    if availability:
        form.new_timeslot.choices = [
            (timeslot, timeslot) for timeslot in availability.available_timeslots
        ]

    if form.validate_on_submit():
        new_timeslot = form.new_timeslot.data
        if new_timeslot not in availability.available_timeslots:
            flash("Dit tijdvak is niet beschikbaar. Kies een andere tijdvak.", "danger")
            return redirect(url_for("bookings.update_booking", booking_id=booking.id))

        availability.release_timeslot(booking.timeslot)
        availability.book_timeslot(new_timeslot)

        booking.timeslot = new_timeslot
        db.session.commit()

        flash("Boeking succesvol bijgewerkt!", "success")
        return redirect(url_for("bookings.my_bookings"))

    return render_template("update_booking.html", booking=booking, form=form)


# webapp/bookings/views.py
@bookings.route("/book_bungalow/<int:bungalow_id>", methods=["GET", "POST"])
@login_required
def book_bungalow(bungalow_id):
    bungalow = Bungalow.query.get_or_404(bungalow_id)
    form = BookingForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data

        # Controleer of de geselecteerde periode beschikbaar is
        booked_timeslots = [
            booking.timeslot
            for booking in bungalow.bookings
            if booking.timeslot >= start_date and booking.timeslot <= end_date
        ]

        if booked_timeslots:
            flash("Dit tijdvak is niet beschikbaar. Kies een andere tijdvak.", "danger")
            return redirect(url_for("bookings.book_bungalow", bungalow_id=bungalow_id))

        # Voeg nieuwe boeking toe
        booking = Booking(
            bungalow_id=bungalow.id,
            start_date=start_date,
            end_date=end_date,
            user_id=current_user.id,
        )
        db.session.add(booking)
        db.session.commit()

        flash("Bungalow succesvol geboekt!", "success")
        return redirect(url_for("bookings.my_bookings"))

    return render_template("book_bungalow.html", bungalow=bungalow, form=form)
