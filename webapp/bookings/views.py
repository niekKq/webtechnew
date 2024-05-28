from flask import Blueprint, abort, render_template, request, flash, redirect, url_for
from webapp.models import Bungalow, Booking, BungalowAvailability
from webapp import db
from webapp.bookings.forms import BookingForm, DeleteBookingForm, UpdateBookingForm
from flask_login import current_user, login_required
from datetime import timedelta

bookings = Blueprint("bookings", __name__, template_folder="templates")


@bookings.route("/my_bookings")
@login_required
def my_bookings():
    user_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template("my_bookings.html", bookings=user_bookings, form=DeleteBookingForm())


@bookings.route("/update_booking/<int:booking_id>", methods=["GET", "POST"])
@login_required
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    form = UpdateBookingForm()
    
    if form.validate_on_submit():
        new_start = form.new_start.data
        new_end = form.new_end.data
        
        if new_end < new_start:
            flash("De einddatum moet na de startdatum liggen.", "danger")
            return redirect(url_for("bookings.update_booking", booking_id=booking.id))

        booking.start_date = new_start
        booking.end_date = new_end
        db.session.commit()

        flash("Boeking succesvol bijgewerkt!", "success")
        return redirect(url_for("bookings.my_bookings"))

    return render_template("update_booking.html", booking=booking, form=form)


@bookings.route('/booking/<int:booking_id>/delete', methods=["POST", "GET"])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    bungalow_name = booking.bungalow.name

    if booking.user_id != current_user.id:
        abort(403)

    db.session.delete(booking)

    availability = BungalowAvailability.query.filter_by(
        bungalow_id=booking.bungalow_id,
        timeslot=booking.start_date
    ).first()

    if availability:
        availability.available = True

    db.session.commit()

    flash(f"Je boeking voor {bungalow_name} is succesvol verwijderd!", 'success')
    return redirect(url_for('bookings.my_bookings'))


@bookings.route("/book_bungalow/<int:bungalow_id>", methods=["GET", "POST"])
@login_required
def book_bungalow(bungalow_id):
    bungalow = Bungalow.query.get_or_404(bungalow_id)

    form = BookingForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data

        booked_timeslot = next(
            (booking for booking in bungalow.bookings 
             if not (booking.end_date < start_date or booking.start_date > end_date)), 
            None
        )
        bungalow.max_days = 7

        if end_date - start_date > timedelta(days=bungalow.max_days):

            flash(f"De minimale boekingsperiode is {bungalow.max_days} dagen.", "danger")
            return redirect(url_for("bookings.book_bungalow", bungalow_id=bungalow_id))

        if booked_timeslot:
            flash(
                f"Dit tijdvak is niet beschikbaar. Kies een andere tijdvak.\n "
                f"Dit tijdvlak is al bezet: {booked_timeslot.start_date} tot {booked_timeslot.end_date}.", 
                "danger"
            )
            return redirect(url_for("bookings.book_bungalow", bungalow_id=bungalow_id))

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

