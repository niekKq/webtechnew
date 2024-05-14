from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from webapp.main.forms import InfoForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

from webapp.main.views import main
app.register_blueprint(main)

@login_manager.user_loader
def load_user(user_id):
    from webapp.models import User
    return User.query.get(int(user_id))

# Voer db.create_all() uit om de database te maken
with app.app_context():
    db.create_all()
