from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from . import db
from .forms import InstitutionForm
from .models import Dminstitution

navdropdown_blueprint = Blueprint('navdropdown_blueprint', __name__)



@navdropdown_blueprint.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

@navdropdown_blueprint.route('/upload', methods=['POST'])
@login_required
def upload_post():
    return render_template('upload.html')


@navdropdown_blueprint.route('/institutions')
@login_required
def institutions():
    form = InstitutionForm().new()
    return render_template('institutions.html', form=form)
    
@navdropdown_blueprint.route('/institutions', methods=['POST'])
@login_required
def institutions_post():
    form = InstitutionForm().new()
    print(request.form, flush=True) 
    # Add new inst entry logic
    if request.form.get('institution') == 'add':
        new_inst = Dminstitution(
                    instcode=request.form.get('inst_code'),
                    name=request.form.get('inst_name'),
                    additionalinfo=request.form.get('info'))
        # add the new inst to the database
        db.session.add(new_inst)
        db.session.commit()
        flash('New institution added successfully!')
    else:
        institution = db.session.query(Dminstitution).filter_by(instcode=request.form.get('institution')).first()
        institution.name = request.form.get('inst_name') or institution.name
        institution.instcode = request.form.get('inst_code') or institution.instcode
        institution.additionalinfo = request.form.get('info') or institution.additionalinfo
        db.session.commit()
        flash('Selected institution updated successfully!')

    return render_template('institutions.html', form=form)

