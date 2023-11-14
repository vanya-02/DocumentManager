# the auth routes for the app
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import Dmuser
from . import db
from .forms import SignUpForm, LogInForm

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/login')
def login():
    form = LogInForm()
    return render_template('login.html', form=form)

@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = db.session.query(Dmuser).filter_by(email=email).first()
    print(request.form, flush=True)
    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth_blueprint.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('profile_blueprint.profile'))

@auth_blueprint.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)

@auth_blueprint.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    surname = request.form.get('surname', default='')
    patronymic = request.form.get('patronymic', default='')
    username = '.'.join([name, surname]).lower()
    password = request.form.get('password')
    
    # if this returns a user, then the email already exists in database
    user = db.session.query(Dmuser).filter_by(email=email).first()
    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth_blueprint.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = Dmuser(
                email=email,
                name=name, 
                surname=surname, 
                patronymic=patronymic, 
                username=username, 
                password=generate_password_hash(password))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('User created!')
    return redirect(url_for('auth_blueprint.signup'))

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_blueprint.index'))

