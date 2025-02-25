import psycopg2

DB_NAME = "22CS10036"
DB_USER = "22CS10036"
DB_PASSWORD = "kmb2003"
DB_HOST = "10.5.18.70"

# Connect to database
try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host=DB_HOST)
    print("Database connected successfully")
except:
    print("Database not connected successfully")

# Creating a db
db = conn.db() 

# Creatign Tables

# Create Users Table
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(200) NOT NULL,
        role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'employee', 'citizen', 'government'))
    )
    """)

# Create 

# Create Agriculture Table
db.execute("""
    CREATE TABLE IF NOT EXISTS agriculture (
        id SERIAL PRIMARY KEY,
        year INT NOT NULL,
        crop_type VARCHAR(100) NOT NULL,
        production FLOAT NOT NULL
    )
    """)

# Create Health Table
db.execute("""
    CREATE TABLE IF NOT EXISTS health (
        id SERIAL PRIMARY KEY,
        facility_name VARCHAR(100) NOT NULL,
        services TEXT NOT NULL,
        patient_count INT NOT NULL
    )
    """)

# Create Education Table
db.execute("""
    CREATE TABLE IF NOT EXISTS education (
        id SERIAL PRIMARY KEY,
        school_name VARCHAR(100) NOT NULL,
        students_count INT NOT NULL
    )
    """)

# Create Welfare Table
db.execute("""
    CREATE TABLE IF NOT EXISTS welfare (
        id SERIAL PRIMARY KEY,
        scheme_name VARCHAR(100) NOT NULL,
        beneficiaries INT NOT NULL,
        amount FLOAT NOT NULL
    )
    """)

db.close()
conn.close()


