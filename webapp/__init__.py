from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LekWOUpAAAAAFbyLqbQvfV7Xw98wxRAcc2RDzzE'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LekWOUpAAAAAPzuUhXki0_6ISVUImgEETZi2r9k'


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

from webapp.main.views import main
from webapp.bungalows.views import bung
from webapp.bookings.views import bookings

app.register_blueprint(main)
app.register_blueprint(bung)
app.register_blueprint(bookings, url_prefix="/bookings")

@login_manager.user_loader
def load_user(user_id):
    from webapp.models import User
    return User.query.get(int(user_id))

def init_admin():
    from webapp.models import User
    with app.app_context():
        admin_email = 'admin@gmail.com'
        admin_username = 'admin'
        admin_password = 'admin'

        # Check if admin user already exists
        admin = User.query.filter_by(email=admin_email).first()
        if admin is None:
            admin = User(
                username=admin_username,
                email=admin_email,
                password=generate_password_hash(admin_password),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user '{admin_username}' created with email '{admin_email}'")
        else:
            print(f"Admin user already exists with email '{admin_email}'")

with app.app_context():
    db.create_all()
    init_admin()
