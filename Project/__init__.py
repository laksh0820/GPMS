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
app.config['SECURITY_PASSWORD_SALT'] = 'GPMS//kSDfkuas_hufhasiughnahgav_uhrganuvrh_iuerghuvh//23jnrxnl4r'
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

# Define a function that requires the application context
def initialize_database():
    with app.app_context():
        # Perform database operations
        print("Initializing database...")
        
        conn = get_db_connection()
        db = conn.cursor()
        
        # Creating Tables
        
        # Create Citizen Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Citizen (
                citizen_id INT,
                name VARCHAR(100),
                gender VARCHAR(10),
                dob DATE,
                income DECIMAL(12,2),
                educational_qualification VARCHAR(100),
                primary key (citizen_id)
            );
            """)

        # Create Users Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(200) NOT NULL,
                citizen_id INT,
                role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'employee', 'citizen', 'government')),
                is_verified BOOLEAN NOT NULL DEFAULT FALSE,
                foreign key (citizen_id) references Citizen
            );
            """)

        # Create Panchayat Employee Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Panchayat_Employee (
                employee_id SERIAL PRIMARY KEY,
                citizen_id INT,
                role VARCHAR(100),
                foreign key (citizen_id) references Citizen
            );       
            """)

        # Create Taxes table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Taxes (
                tax_id SERIAL PRIMARY KEY,
                citizen_id INT,  
                type VARCHAR(100),
                tax_month INT CHECK (tax_month >= 1 AND tax_month <= 12), 
                tax_year INT,
                amount_due DECIMAL(12,2),
                due_date Date,
                status VARCHAR(20) NOT NULL CHECK (status IN ('Paid', 'Unpaid')),
                foreign key (citizen_id) references Citizen
            );
            """)

        # Create Asset Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Asset (
                asset_id SERIAL PRIMARY KEY,
                type VARCHAR(100) NOT NULL CHECK (type <> ''),
                location VARCHAR(500) NOT NULL CHECK (location <> ''),
                installation_date DATE NOT NULL
            );
            """)

        # Create Agriculture Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Land_Record (
                land_id SERIAL PRIMARY KEY,
                citizen_id INT,
                area_acres DECIMAL(10,4),
                crop_type VARCHAR(500),
                foreign key (citizen_id) references Citizen
            );
            """)

        # Create Vaccines Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Vaccines (
                vaccine_id SERIAL PRIMARY KEY,
                vaccine_type VARCHAR(100) NOT NULL CHECK (vaccine_type <> ''),
                centers VARCHAR(500) NOT NULL CHECK (centers <> '')
            );
            """)

        # Create Vaccination Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Vaccination (
                vaccination_id SERIAL PRIMARY KEY,
                citizen_id INT,
                vaccine_id INT,
                date_administered DATE,
                foreign key (citizen_id) references Citizen,
                foreign key (vaccine_id) references Vaccines
            );
            """)

        # Create Service Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Service (
                doc_id SERIAL PRIMARY KEY,
                doc_type VARCHAR(200) NOT NULL CHECK (doc_type <> ''),
                description VARCHAR(1000) NOT NULL CHECK (description <> '')
            );
            """)

        # Create Document Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Documents (
                issue_id SERIAL PRIMARY KEY,
                citizen_id INT,
                doc_id INT,
                issue_date DATE,
                foreign key (citizen_id) references Citizen,
                foreign key (doc_id) references Service 
            );
            """)

        # Create Expenditure Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Expenditures (
                bill_id SERIAL PRIMARY KEY,
                expense_type VARCHAR(200) NOT NULL CHECK (expense_type <> ''),
                description VARCHAR(1000) NOT NULL CHECK (description <> '')
            );
            """)

        # Create Environmental Data
        db.execute("""
            CREATE TABLE IF NOT EXISTS Environmental_Data (
                data_id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                air_quality_index INT NOT NULL,
                water_quality VARCHAR(200) NOT NULL CHECK (water_quality <> ''),
                sanitation VARCHAR(200) NOT NULL CHECK (sanitation <> '')   
            );
            """)

        # Create Welfare-Scheme Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Welfare_Scheme (
                scheme_id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL CHECK (name <> ''),
                description VARCHAR(1000) NOT NULL CHECK (description <> '')
            );
            """)

        # Create Scheme-Enrollment Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Scheme_Enrollment (
                enrollment_id SERIAL PRIMARY KEY,
                citizen_id INT,
                scheme_id INT,
                enrollment_date DATE,
                foreign key (citizen_id) references Citizen,
                foreign key (scheme_id) references Welfare_Scheme
            );
            """)

        # Create a Census Data Table
        db.execute("""
            CREATE TABLE IF NOT EXISTS Census_Data (
                data_id SERIAL PRIMARY KEY,
                year INT UNIQUE NOT NULL,
                population_male INT NOT NULL,
                population_female INT NOT NULL,
                births_male INT NOT NULL,
                births_female INT NOT NULL,
                deaths_male INT NOT NULL,
                deaths_female INT NOT NULL,
                marriages INT NOT NULL
            );
            """)

        conn.commit()
        db.close()
        conn.close()
        
initialize_database()
tax_generate()

from Project import routes