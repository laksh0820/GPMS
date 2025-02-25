from flask import Flask
import psycopg2
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'grampanchayatksdkar37ro8hf83fh3892hmfijw38fh'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=20)
app.config['SECURITY_PASSWORD_SALT']='email-confirmation-for-a-new-user//projectzetaX//23jnrxnl4r'
app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

DB_NAME = "22CS10036"
DB_USER = "22CS10036"
DB_PASSWORD = "kmb2003"
DB_HOST = "10.5.18.70"

# connect to database
try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host=DB_HOST)
    print("Database connected successfully")
except:
    print("Database not connected successfully")

# creating a cursor
db = conn.cursor() 

from Project import routes