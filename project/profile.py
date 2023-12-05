# the non-auth routes for the app
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import ProfileForm, UpdatePassordForm
from .models import Dmusers, Dminstitutions
from . import db

profile_blueprint = Blueprint('profile_blueprint', __name__)

@profile_blueprint.route('/profile')
@login_required
def profile():
    profile_form = ProfileForm().new()
    password_form = UpdatePassordForm()
    return render_template('profile.html', profile_form=profile_form, password_form=password_form)

@profile_blueprint.route('/profile', methods=['POST'])
@login_required
def profile_post():
    profile_form = ProfileForm().new()
    password_form = UpdatePassordForm()
    user = db.session.query(Dmusers).filter_by(email=current_user.email).first()
    
    # change user settings 
    if profile_form.validate_on_submit():
        institution = db.session.query(Dminstitutions).filter(Dminstitutions.instcode == request.form.get('institution')).first()
        user.idinstitution = (institution.id)
        user.name = request.form.get('name') or current_user.name # In case form field is empty
        user.surname = request.form.get('surname') or current_user.surname
        user.patronymic = request.form.get('patronymic') or current_user.patronymic
        if check_password_hash(user.password, request.form.get('password')):
            db.session.commit()
            flash('User profile updated successfully!', 'profile')
        else:
            flash('Wrong password. Try again', 'profile')
    # change password logic
    if password_form.validate_on_submit():
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        if check_password_hash(user.password, old_password): 
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password updated successfully!', 'password')
        else:
            flash('Wrong password. Try again', 'password')

    return render_template('profile.html', profile_form=profile_form, password_form=password_form)
