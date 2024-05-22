# webapp/models.py
from datetime import datetime, timedelta
from flask_login import UserMixin
from webapp import db
from sqlalchemy.orm import relationship


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    bookings = relationship("Booking", back_populates="user")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', 'Admin={self.is_admin}'))"


class Bungalow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    bungalow_type = db.Column(db.String(100), nullable=False)
    weekprice = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(100), nullable=True, default="default.jpg")

    bookings = relationship("Booking", backref="bungalow", lazy=True)

    def available_timeslots(self):
        booked_timeslots = [booking.timeslot for booking in self.bookings]
        min_date = datetime.now()
        max_date = min_date + timedelta(days=30)
        available_timeslots = []
        current_date = min_date
        while current_date <= max_date:
            timeslot = current_date.strftime("%Y-%m-%d")
            if timeslot not in booked_timeslots:
                available_timeslots.append(timeslot)
            current_date += timedelta(days=1)
        return available_timeslots

    def __repr__(self):
        return f"Bungalow('{self.name}', '{self.bungalow_type}', '{self.weekprice}', '{self.image_file}')"


# webapp/models.py
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bungalow_id = db.Column(db.Integer, db.ForeignKey("bungalow.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user = relationship("User", back_populates="bookings")

    def __repr__(self):
        return f"<Booking {self.id}>"


class BungalowAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bungalow_id = db.Column(db.Integer, db.ForeignKey("bungalow.id"), nullable=False)
    timeslot = db.Column(db.String(50), nullable=False)
    available = db.Column(db.Boolean, default=True)

    def release_timeslot(self, timeslot):
        if self.timeslot == timeslot:
            self.available = True

    def book_timeslot(self, timeslot):
        if self.timeslot == timeslot:
            self.available = False

    def __repr__(self):
        return f"<BungalowAvailability bungalow_id={self.bungalow_id}, timeslot={self.timeslot}, available={self.available}>"
