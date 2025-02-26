from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField, PasswordField, SubmitField,TextAreaField,RadioField,BooleanField,DateField,FloatField
from wtforms.validators import DataRequired,EqualTo,Email,Length,Regexp
from wtforms.widgets import PasswordInput

MIN_PASSWORD_LEN = 8
MAX_PASSWORD_LEN = 12

class UserForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email(message="Invalid email address (should be of the form something@example.com)")])
    password = PasswordField("Password",validators=[DataRequired(),
                                        Length(min=MIN_PASSWORD_LEN,max=MAX_PASSWORD_LEN),
                                        EqualTo('confirm_password',message="Password does not match to Confirm Password. Please retype"),
                                        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@$!%*?&])[A-Za-z0-9@$!%*?&]",
                                        message="Password should contain atleast one lowercase character, one uppercase character,one number and one special character." )])
    confirm_password = PasswordField("Confirm-Password",validators=[DataRequired(),Length(min=MIN_PASSWORD_LEN,max=MAX_PASSWORD_LEN)])
    
class LogInForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email(message="Invalid email address (should be of the form something@example.com)")])
    password = PasswordField("Password",validators=[DataRequired()])
    role = RadioField("Role",validators=[DataRequired()],choices=[('citizen','citizen'),
                                                                  ('panchayat_employee','panchayat_employee'),
                                                                  ('government','government'),
                                                                  ('admin','admin')])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Submit")

class CitizenForm(UserForm):
    name = StringField("Username",validators=[DataRequired()])
    gender = RadioField("Gender",validators=[DataRequired()],choices=[('male','male'),('female','female')])
    dob = DateField("Date",validators=[DataRequired()],format='%Y-%m-%d')
    educational_qualification = StringField("Educational Qualification",validators=[DataRequired()])
    household_id = IntegerField("Household-ID",validators=[DataRequired()])
    address = StringField("Address",validators=[DataRequired()])
    income = FloatField("Income",validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class PanchayatEmployeeForm(UserForm):
    role = StringField("Role",validators=[DataRequired()])
    submit = SubmitField("Submit")

class GovernmentForm(UserForm):
    submit = SubmitField("Submit")

class AdminForm(UserForm):
    submit = SubmitField("Submit")