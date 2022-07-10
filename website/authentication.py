from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash

from flask import redirect
from flask import url_for

from .db_models import Account
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from . import db

from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user

authentication = Blueprint('authentication', __name__)

# Server user requests
@authentication.route('/signin', methods = ['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        account = Account.query.filter_by(email = email).first()

# Sign-in functionality
        if account:
            if check_password_hash(account.password, password):
                flash(f'Welcome back, {email}!', category = 'successful')
                login_user(account, remember = True)

                return redirect(url_for('routes.home_page'))

            elif len(password) == 0:
                flash('Please enter a valid password.', category = 'error')

            else:
                flash('Incorrect account password.', category = 'error')

        else:
            flash(f'No account by the email, "{email}" exists. Sign up to continue.', category = 'error')

    return render_template('sign_in.html', account = current_user)

@authentication.route('/signup', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        account = Account.query.filter_by(email = email).first()

# Renders a message is they have previously signed up and need to now sign-in with their email
        if account:
            flash(f'The email, "{email}" already exists. Sign in to continue.', category = 'error')

# Conditionals to make sure that user enters valid information
        elif len(email) < 6:
            flash('Please enter a valid email.', category = 'error')

        elif len(password) < 6:
            flash('Password must be greater than 5 characters in length.', category = 'error')

        elif password != password2:
            flash('The entered passwords do not match.', category = 'error')

# Successful account setup with no errors
        else:
# Object for new user inherited from database model associated with accounts
# Uses a hashing algoritm to store user password string as unique computer output
            new_account = Account(email = email, password = generate_password_hash(password, method = 'sha256'))
            db.session.add(new_account)
            db.session.commit()
            
            login_user(account, remember = True)
            login_user(new_account, remember = True)

            flash(f'Welcome, {email}!', category = 'successful')

# Redirects user to home page after signing up
            return redirect(url_for('routes.home_page'))

    return render_template('sign_up.html', account = current_user)

# Logs user out and redirects to sign-in page
@authentication.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('authentication.sign_in'))
