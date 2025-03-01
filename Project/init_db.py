import psycopg2

DB_NAME = "22CS10036"
DB_USER = "22CS10036"
DB_PASSWORD = "kmb2003"
DB_HOST = "10.5.18.70"
DB_PORT = "5432"

# Connect to database
try:
    conn = psycopg2.connect(dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host=DB_HOST,
                            port=DB_PORT)
    print("Database connected successfully")
except:
    print("Database not connected successfully")

# Creating a db
db = conn.cursor() 

# Creating Tables

# Create Citizen Table
db.execute("""
    CREATE TABLE IF NOT EXISTS Citizen (
        citizen_id INT,
        name VARCHAR(50),
        gender VARCHAR(10),
        dob DATE,
        income DECIMAL(12,2),
        educational_qualification VARCHAR(20),
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
        role VARCHAR(50),
        foreign key (citizen_id) references Citizen
    );       
    """)

# Create Taxes table
db.execute("""
    CREATE TABLE IF NOT EXISTS Taxes (
        tax_id SERIAL PRIMARY KEY,
        citizen_id INT,  
        type VARCHAR(50),
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
        type VARCHAR(50) NOT NULL CHECK (type <> ''),
        location VARCHAR(50) NOT NULL CHECK (location <> ''),
        installation_date DATE NOT NULL CHECK (installation_date <> '')
    );
    """)

# Create Agriculture Table
db.execute("""
    CREATE TABLE IF NOT EXISTS Land_Record (
        land_id SERIAL PRIMARY KEY,
        citizen_id INT,
        area_acres DECIMAL(10,4),
        crop_type VARCHAR(50),
        foreign key (citizen_id) references Citizen
    );
    """)

# Create Vaccines Table
db.execute("""
    CREATE TABLE IF NOT EXISTS Vaccines (
        vaccine_id SERIAL PRIMARY KEY,
        vaccine_type VARCHAR(50) NOT NULL CHECK (vaccine_type <> ''),
        centers VARCHAR(50) NOT NULL CHECK (centers <> '')
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
        doc_type VARCHAR(100) NOT NULL CHECK (doc_type <> ''),
        description VARCHAR(100) NOT NULL CHECK (description <> '')
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
        expense_type VARCHAR(100) NOT NULL CHECK (expense_type <> ''),
        description VARCHAR(100) NOT NULL CHECK (description <> '')
    );
    """)

# Create Environmental Data
db.execute("""
    CREATE TABLE IF NOT EXISTS Environmental_Data (
        data_id SERIAL PRIMARY KEY,
        date DATE NOT NULL CHECK (date <> ''),
        air_quality_index INT NOT NULL CHECK (air_quality_index <> ''),
        water_quality VARCHAR(100) NOT NULL CHECK (water_quality <> ''),
        sanitation VARCHAR(100) NOT NULL CHECK (sanitation <> '')   
    );
    """)

# Create Welfare-Scheme Table
db.execute("""
    CREATE TABLE IF NOT EXISTS Welfare_Scheme (
        scheme_id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL CHECK (name <> ''),
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
        year INT UNIQUE NOT NULL CHECK (year <> ''),
        population_male INT NOT NULL CHECK (population_male <> ''),
        population_female INT NOT NULL CHECK (population_female <> ''),
        births_male INT NOT NULL CHECK (births_male <> ''),
        births_female INT NOT NULL CHECK (births_female <> ''),
        deaths_male INT NOT NULL CHECK (deaths_male <> ''),
        deaths_female INT NOT NULL CHECK (deaths_female <> ''),
        marriages INT NOT NULL CHECK (marriages <> '')
    );
    """)

conn.commit()
db.close()
conn.close()


