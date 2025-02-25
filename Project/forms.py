from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField, PasswordField, SubmitField,TextAreaField,RadioField,BooleanField
from wtforms.validators import DataRequired,EqualTo,Email,Length,Regexp
from wtforms.widgets import PasswordInput

MIN_PASSWORD_LEN = 8
MAX_PASSWORD_LEN = 12

class LogInForm(FlaskForm):
    UserID = IntegerField("User ID")
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Submit")
