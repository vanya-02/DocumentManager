from flask import Blueprint, redirect, render_template, current_app, request, flash, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .utils import format_date, RawSQL, placeholder_query
from . import db
from .forms import InstitutionForm, ProjectForm, UploadForm, ReportsForm
from .models import Dminstitutions, Dmprojects, Dmusers, Dmdocuments
from sqlalchemy import select, event, text
import datetime
import os

navdropdown_blueprint = Blueprint('navdropdown_blueprint', __name__)

# TODO: institution form field placeholder update, if possible via AJAX?

@navdropdown_blueprint.route('/get_placeholder/<name>')
def get_placeholder_values(name):
    return placeholder_query(name)

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
        new_inst = Dminstitutions(
                    instcode=request.form.get('inst_code'),
                    name=request.form.get('inst_name'),
                    additionalinfo=request.form.get('info'))
        # add the new inst to the database
        db.session.add(new_inst)
        db.session.commit()
        flash('New institution added successfully!')
    # Update inst
    else:
        institution = db.session.query(Dminstitutions).filter_by(instcode=request.form.get('institution')).first()
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
        # This returns a Result object, contains the query... result
        institution = db.session.execute(select(Dminstitutions.id).where(Dminstitutions.instcode==request.form.get('institution')))
        if request.form.get('project_id') == 'add':
            new_project = Dmprojects(
                            idinstitution = institution.scalar(),
                            iduser = current_user.id,
                            name = request.form.get('project_name'),
                            datefrom = format_date(request.form.get('date_from')),
                            datetill = format_date(request.form.get('date_till')),
                            isactive = 'True' if request.form.get('is_active') else 'False')
            db.session.add(new_project)
            db.session.commit()
            flash('New project created!')
        else:
            project_row = db.session.query(Dmprojects).filter_by(id=request.form.get('project_id')).first()
            project_row.idinstitution = institution.scalar() 
            project_row.name = request.form.get('project_name') or project_row.name
            project_row.datefrom = format_date(request.form.get('date_from')) or project_row.datefrom
            project_row.datetill = format_date(request.form.get('date_till')) or project_row.datetill
            project_row.additionalinfo = request.form.get('info') or project_row.additionalinfo
            project_row.isactive = 'True' if request.form.get('is_active') else 'False'
            db.session.commit()
            flash('Project updated!')
    else:
        print(form.errors.items())
        flash('Smth went wrong...')

    return render_template('projects.html', form=form)



@navdropdown_blueprint.route('/upload')
@login_required
def upload():
    form = UploadForm().new()
    return render_template('upload.html', form=form)

# add ajax for updating the uploaded filename, rn it works after posting the form 
@navdropdown_blueprint.route('/upload', methods=['POST'])
@login_required
def upload_post():

    form = UploadForm().new()
    print(request.form, flush=True)
    print(request.files, '\n')

    if request.files['file'].filename == '':
        flash('No file selected')
        return redirect(request.url)
    elif form.validate_on_submit(): 
        # institution = db.session.execute(select(Dminstitutions.id).where(Dminstitutions.instcode==request.form.get('institution')))
        filename = secure_filename(request.files['file'].filename)
        request.files['file'].save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        new_doc = Dmdocuments(
            idinstitution = "3",
            iduser = current_user.id,
            idtype = request.form.get('service'),
            idproject = request.form.get('project_id'),
            name = filename,
            savedpath = '\\'.join([current_app.config['UPLOAD_FOLDER'], filename]),
            uploaddate = datetime.date.today(),
            additionalinfo = request.form.get('info'))
        db.session.add(new_doc)
        db.session.commit()
        # locally save file logic

        flash('File uploaded successfuly!')

    return render_template('upload.html', form=form)


@navdropdown_blueprint.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)


@navdropdown_blueprint.route('/reports')
@login_required
def reports():
    form = ReportsForm()   
    return render_template('reports.html', form=form)

@navdropdown_blueprint.route('/reports', methods=['POST'])
@login_required
def reports_post():
    form = ReportsForm()
    rows, cols = None, None

    if form.validate_on_submit():
        query = RawSQL[request.form.get('report_type')]
        report_type = request.form.get('report_type')
        print(request.form)
        print(query)

        if query:
            result = db.session.execute(text(query))
            cols = result.keys()
            rows = result.all()
            print(rows)

    return render_template('reports.html', form=form, rows=rows, cols=cols, report_type=report_type)



