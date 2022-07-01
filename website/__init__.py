# Python package file of 'website' folder
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from flask_login import LoginManager

# Initializes database
db = SQLAlchemy()
DATABASE = 'database.db'

def create_web_app():
    web_app = Flask(__name__)
    web_app.secret_key = '0123456789'

# Initializes remote database location
    web_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE}'
    db.init_app(web_app)

    from .routes import routes
    from .authentication import authentication

    web_app.register_blueprint(routes, url_prefix = '/')
    web_app.register_blueprint(authentication, url_prefix = '/')

# Importing database models
    from .db_models import Account
    from .db_models import Note

    get_database(web_app)

    manage_login = LoginManager()
    manage_login.login_view = 'authentication.sign_in'

    manage_login.init_app(web_app)

    @manage_login.user_loader
    def user_load(id):
        return Account.query.get(int(id))

    return web_app

# Checks if database is already created and initializes it if not already done so
def get_database(web_app):
    if not path.exists('website/' + DATABASE):
        db.create_all(web_app = web_app)
        print('Database created successfuly.')