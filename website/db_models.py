from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(10000))
    note_date= db.Column(db.DateTime(timezone = True), default = func.now())

# Uses a foreign key relationship of one user to many notes
# This method connects the user to their corresponding notes thorugh inheritance
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)

# Enforces that no two accounts can hold the same associated emai
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))

# Stores notes onto account through foreign keys
    notes = db.relationship('Note')
