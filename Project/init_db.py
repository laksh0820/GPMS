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

# Create Household Table
db.execute("""
    CREATE TABLE IF NOT EXISTS Household (
        household_id INT,
        address VARCHAR(50),
        income DECIMAL(12,2),
        primary key (household_id)
    );
    """)

# Create Citizen Table
db.execute("""
    CREATE TABLE IF NOT EXISTS Citizen (
        citizen_id INT,
        name VARCHAR(50),
        gender VARCHAR(10),
        dob DATE,
        household_id INT,
        educational_qualification VARCHAR(20),
        primary key (citizen_id),
        foreign key (household_id) references Household
    );
    """)

# Create Users Table
db.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(100) NOT NULL,
        password VARCHAR(200) NOT NULL,
        citizen_id INT,
        role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'panchayat_employee', 'citizen', 'government')),
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
        tax_year INT,
        amount_due DECIMAL(12,2),
        due_data Date,
        status VARCHAR(20),
        foreign key (citizen_id) references Citizen
    );
    """)

# Create Asset Table
db.execute("""
    CREATE TABLE IF NOT EXISTS Asset (
        asset_id SERIAL PRIMARY KEY,
        employee_id INT,
        type VARCHAR(50),
        location VARCHAR(50),
        installation_date DATE,
        foreign key (employee_id) references Panchayat_Employee
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

# Create Vaccination Table
db.execute("""
    CREATE TABLE IF NOT EXISTS Vaccination (
        vaccination_id SERIAL PRIMARY KEY,
        citizen_id INT,
        vaccine_type VARCHAR(50),
        date_administered DATE,
        foreign key (citizen_id) references Citizen
    );
    """)

# Create Welfare-Scheme Table
db.execute("""
    CREATE TABLE IF NOT EXISTS Welfare_Scheme (
        scheme_id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        description VARCHAR(1000)
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
        household_id INT,
        citizen_id INT,
        event_type VARCHAR(50),
        event_date DATE,
        foreign key (household_id) references Household,
        foreign key (citizen_id) references Citizen
    );
    """)
conn.commit()

db.close()
conn.close()


