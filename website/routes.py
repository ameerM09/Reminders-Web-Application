from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify

from flask_login import login_required
from flask_login import current_user

from .db_models import Note
from . import db

import json

routes = Blueprint('routes', __name__)

# Route for the home page of the website where users see their notes
# This page only apepars after the user signs up or signs in
@routes.route('/', methods = ['GET', 'POST'])
@login_required
def home_page():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) <= 5:
            flash('Length of note must be greater than 5 characters.', category = 'error')

# Creates new object for when user adds new note and adds it to the database
        else:
            added_note = Note(content = note, account_id = current_user.id)
            db.session.add(added_note)
            db.session.commit()

# Renders a successful message when new note is created
            flash('Note successfully added!', category = 'successful')

    return render_template('home_page.html', account = current_user)

@routes.route('/about')
def about_us():
    return render_template('about_us.html', account = current_user)

@routes.route('/del-account-note', methods = ['POST'])
def del_account_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

# Checks for the event in which a user decides to remove a note
# Deletes elemetn from database
    if note:
        if note.account_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

# Returns object
    return jsonify({})