from flask import Flask
import psycopg2
from datetime import timedelta
from Project.Admin.admin import admin_bp
from Project.Citizen.citizen import citizen_bp
from Project.Employee.employee import employee_bp
from Project.Government.government import government_bp

DB_NAME = "22CS10036"
DB_USER = "22CS10036"
DB_PASSWORD = "kmb2003"
DB_HOST = "10.5.18.70"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'grampanchayatksdkar37ro8hf83fh3892hmfijw38fh'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=20)
app.config['DB_NAME'] = DB_NAME
app.config['DB_USER'] = DB_USER
app.config['DB_PASSWORD'] = DB_PASSWORD
app.config['DB_HOST'] = DB_HOST

# Register Blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(citizen_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(government_bp)

from Project import routes