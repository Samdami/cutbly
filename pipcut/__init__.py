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

# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dams_user:PGHQ7g8rQKgradIsKeQM4AMFn0eP0EnN@dpg-clct1seg1b2c73f1qbd0-a.oregon-postgres.render.com/dams'

# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["m3pgWQMM7276cJvcEFKIyw"] = os.environ.get("m3pgWQMM7276cJvcEFKIyw")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

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
