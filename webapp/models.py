from flask_login import UserMixin
from webapp import db, bcrypt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_active(self):
        # Hier kun je de logica implementeren om te controleren of de gebruiker actief is.
        return True  # Of pas deze aan op basis van je applicatielogica

    def is_authenticated(self):
        # Implementeer de logica om te controleren of de gebruiker geauthenticeerd is.
        return True  # Of pas deze aan op basis van je applicatielogica

    def is_anonymous(self):
        # Implementeer de logica om te controleren of de gebruiker anoniem is.
        return False  # Of pas deze aan op basis van je applicatielogica

    def get_id(self):
        # Implementeer de logica om de unieke id van de gebruiker op te halen.
        return str(self.id)  # Of pas deze aan op basis van je applicatielogica

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Bungalow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    bungalow_type = db.Column(db.Integer, nullable=False)
    weekprice = db.Column(db.Integer, nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"Bungalow('{self.name}', '{self.bungalow_type}', '{self.weekprice}')"
    
