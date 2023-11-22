from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import RadioField, FileField, StringField, SubmitField, EmailField, PasswordField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email
from project.utils import institutions, projects


class SignUpForm(FlaskForm):
    email = EmailField('', validators=[Email(), DataRequired(), Length(1, 32)], render_kw={"class": "input is-large", "placeholder": "Your Email"})
    name = StringField('', validators=[DataRequired(), Length(1, 32)], render_kw={"class": "input is-large", "placeholder": "Your Name"})
    surname = StringField('', validators=[DataRequired(), Length(1, 32)], render_kw={"class": "input is-large", "placeholder": "Your Surname"})
    patronymic = StringField('', validators=[DataRequired(), Length(1,32)], render_kw={"class": "input is-large", "placeholder": "Your Patronymic"})
    password = PasswordField('', validators=[DataRequired()], render_kw={"class": "input is-large", "placeholder": "Your Password"})

    submit = SubmitField('Submit', render_kw={"class": "button is-block is-info is-large is-fullwidth"})

class LogInForm(FlaskForm):
    email = EmailField('', validators=[Email(), DataRequired(), Length(1, 32)], render_kw={"class": "input is-large", "placeholder": "Your Email"})
    password = PasswordField('', validators=[DataRequired()], render_kw={"class": "input is-large", "placeholder": "Your Password"})
    remember = BooleanField('Remember me')

    submit = SubmitField('Login', render_kw={"class": "button is-block is-info is-large is-fullwidth"})

class ProfileForm(FlaskForm):
    email = EmailField('', render_kw={"disabled": "disabled", "class": "input is-large"})
    institution = SelectField('', render_kw={"class": "input is-large"})
    name = StringField('', render_kw={"class": "input is-large"})
    surname = StringField('', render_kw={"class": "input is-large"})
    patronymic = StringField('', render_kw={"class": "input is-large"})
    password = PasswordField('', validators=[DataRequired()], render_kw={"class": "input is-large", "placeholder": "Password"})

    update = SubmitField('Update Info', render_kw={"class": "button is-block is-info is-large is-fullwidth"})
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the institution field
        form.institution.choices = institutions()
        return form

class UpdatePassordForm(FlaskForm):
    old_password = PasswordField('', validators=[DataRequired()], render_kw={"class": "input is-large", "placeholder": "Old Password"})
    new_password = PasswordField('', validators=[DataRequired()], render_kw={"class": "input is-large", "placeholder": "New Password"})

    update = SubmitField('Update Password', render_kw={"class": "button is-block is-info is-large is-fullwidth"})

class InstitutionForm(FlaskForm):
    institution = SelectField('', render_kw={"class": "input is-large"})
    inst_name = StringField('', validators=[DataRequired(), Length(1, 32)], render_kw={"class": "input is-large", "placeholder": "Institution name"})
    inst_code = StringField('', validators=[DataRequired(), Length(1, 20)], render_kw={"class": "input is-large", "placeholder": "Institution code, e.g. MAIB"})
    info = StringField('', validators=[Length(0, 256)], render_kw={"class": "input is-large", "placeholder": "Additional info"})

    submit = SubmitField('Submit', render_kw={"class": "button is-block is-info is-large is-fullwidth"})
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the institution field
        form.institution.choices = [("add","-Add Institution-"), *institutions()]
        return form
    
class ProjectForm(FlaskForm):
    institution = SelectField('Institution:', render_kw={"class": "input is-large"})
    user = StringField('User responsable for creation:', render_kw={"class": "input is-large", "disabled": "disabled"})
    project_name = StringField('', validators=[DataRequired(), Length(1, 20)], render_kw={"class": "input is-large", "placeholder": "Project name"})
    project_id =  SelectField('', render_kw={"class": "input is-large"})
    info = StringField('', validators=[Length(0, 1000)], render_kw={"class": "input is-large", "placeholder": "Additional info"})
    date_from = DateField('Date From', validators=[DataRequired()], render_kw={"class": "button is-block is-info is-large is-fullwidth"})
    date_till = DateField('Date To', validators=[DataRequired()], render_kw={"class": "button is-block is-info is-large is-fullwidth"})
    is_active = BooleanField('Is active?')

    submit = SubmitField('Create project', render_kw={"class": "button is-block is-info is-large is-fullwidth"})
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the institution field and projects
        form.institution.choices = institutions()
        form.project_id.choices = [("add","-Add Project-"), *projects()]
        return form
    
class UploadForm(FlaskForm):
    file = FileField('')
    institution = SelectField('Institution:', render_kw={"class": "input is-large"})
    service = RadioField('Document Type:', choices=[('2', 'Service - Network'), ('3', 'Service - Safety'), ('4', 'Service - Change'), ('5', 'Service - Backup'),
                                                    ('6', 'SLA Report'), ('8', 'Design - Analysis'), ('9', 'Design - Transition'), ('10', 'Design - Production'),
                                                    ('11', 'Design - Test'), ('12', 'Design - Monitoring')])
    project_id =  SelectField('', render_kw={"class": "input is-large"})
    info = StringField('', validators=[Length(0, 1000)], render_kw={"class": "input is-large", "placeholder": "Additional info"})

    submit = SubmitField('Upload', render_kw={"class": "button is-block is-info is-large is-fullwidth"})
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the institution field and projects
        form.institution.choices = institutions()
        form.project_id.choices = projects()
        return form