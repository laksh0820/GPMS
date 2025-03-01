from flask import Flask
import psycopg2
from datetime import timedelta
from Project.Admin.admin import admin_bp
from Project.Citizen.citizen import citizen_bp
from Project.Employee.employee import employee_bp
from Project.Government.government import government_bp
from Project.utils.db_utils import get_db_connection
from datetime import datetime

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
app.config['EXPLAIN_TEMPLATE_LOADING'] = False
app.config['DEBUG'] = True
app.config['TESTING'] = False

# Register Blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(citizen_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(government_bp)
    

# To Calculate Tax amount
def calculate_tax_amount(amount):
    return 0.2 * float(amount) # Apply 20% tax on the given amounts

# Helper function to calculate date after one month
def calculate_date(skip_month=1):
    today = datetime.today()
    
    if today.month == 12:
        one_month_later = today.replace(year=today.year + 1,month=1)
    else:
        one_month_later = today.replace(month=today.month + 1)
    
    return one_month_later.strftime('%Y-%m-01')

# Tax Generator Function
def tax_generate():
    with app.app_context():
        conn = get_db_connection()
        db = conn.cursor()
        
        current_year = datetime.today().year
        current_month = datetime.today().month
        db.execute("""
                SELECT tax_year,tax_month 
                from taxes;
                """)
        res = db.fetchall()
        
        is_available = 0
        for row in res:
            if row[0] == current_year and row[1] == current_month:
                is_available = 1    
        
        if is_available == 0:
            db.execute("""
                    SELECT citizen_id,income
                    from citizen;
                    """)
            res = db.fetchall()
            
            for row in res:
                db.execute("""
                        insert into taxes(citizen_id,type,tax_month,tax_year,amount_due,due_date,status)
                        values (%s,'Income Tax',%s,%s,%s,%s,'Unpaid');
                        """,[row[0],current_month,current_year,calculate_tax_amount(row[1]),calculate_date()])
            conn.commit()
        
        db.close()
        conn.close()

tax_generate()

from Project import routes