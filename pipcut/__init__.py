from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_share import Share
from flask_caching import Cache
import os
from dotenv import load_dotenv
import secrets

# base_dir = os.path.dirname(os.path.realpath(__file__))

load_dotenv()
app = Flask(__name__)

secret = secrets.token_urlsafe(32)

app.secret_key = secret

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["m3pgWQMM7276cJvcEFKIyw"] = os.environ.get("m3pgWQMM7276cJvcEFKIyw")
# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_PORT"] = 465
# app.config["MAIL_USE_TLS"] = False
# app.config["MAIL_USE_SSL"] = True
# app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
# app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
# postgres://pipcut_user:Ng626gxN13C8BGaVeKmJQj5jnOWJ9g72@dpg-ciar7ll9aq007teh7370-a.oregon-postgres.render.com/pipcut


db = SQLAlchemy(app)
mail = Mail(app)
share = Share(app)
cache = Cache(app)


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from . import routes
from .models import User
from .models import Url

db.create_all()