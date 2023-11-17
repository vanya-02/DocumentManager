from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .utils import format_date
from . import db
from .forms import InstitutionForm, ProjectForm
from .models import Dminstitution, Dmproject, Dmuser

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


@navdropdown_blueprint.route('/projects')
@login_required
def projects():
    form = ProjectForm().new()
    return render_template('projects.html', form=form)

@navdropdown_blueprint.route('/projects', methods=['POST'])
@login_required
def projects_post():
    form = ProjectForm().new()
    print(request.form, flush=True)
    
    # add new project to the database
    if form.validate_on_submit():
        institution = db.session.query(Dminstitution).filter_by(instcode=request.form.get('institution')).first()
        new_project = Dmproject(
                        idinstitution = institution.id,
                        iduser = current_user.id,
                        name = request.form.get('project_name'),
                        datefrom = format_date(request.form.get('date_from')),
                        datetill = format_date(request.form.get('date_till')),
                        isactive = 'True' if request.form.get('is_active') else 'False')
        db.session.add(new_project)
        db.session.commit()
        flash('New project created!')
    else:
        print(form.errors.items())
        flash('Smth went wrong...')


    return render_template('projects.html', form=form)


