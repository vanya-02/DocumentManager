from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email

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
